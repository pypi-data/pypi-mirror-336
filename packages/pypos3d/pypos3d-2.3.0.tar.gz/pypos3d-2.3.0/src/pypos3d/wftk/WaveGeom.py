# -*- coding: utf-8 -*-
# package: pypos3d.wftk
import sys
import os
import copy
import logging
import traceback
import array
import gzip
import bisect
from collections import namedtuple
import math
import numpy as np
from scipy import spatial

from langutil import C_OK, C_FAIL, C_UNKNOWN, C_ERROR, GetLowExt
from pypos3d.wftk import WFBasic 
from pypos3d.wftk.WFBasic import C_MISSING_FACEMAT, C_MISSING_MAT, FEPSILON, CoordSyst, FaceNormalOrder,\
  C_FACE_TEXTNORM, C_FACE_TEXT, C_FACE_MATMASK, C_FACE_NORM, C_AXIS_NONE
from pypos3d.wftk.WFBasic import LowestIdxPos, CreateLoop, FaceVisibility, get2DProjectedPoint
from pypos3d.wftk.WFBasic import TexCoord2f, Point3d, Vector3d, calcMLS, getOBJFile, Edge, IndexAdd, FaceCut, FaceSplit, CuttingData

from pypos3d.wftk.PoserFileParser import OBJ_FNAT, PoserFileParser
from pypos3d.wftk.Repere import Repere
from pypos3d.wftk.GeomGroup import GeomGroup, FaceAttr


WFColor = namedtuple('WFColor', [ 'r', 'g', 'b', 't', 'name'])
''' Basic 4 float color : rgb + t '''
WFColor.__new__.__defaults__ = (0.0, 0.0, 0.0, 1.0, None) 

class WFMat:
  ''' Simple WaveFront Material.
  Only diffuse three colors (Diffuse, A, S), a diffuse map and transparency are managed.
  '''
  
  def __init__(self, name, kd=WFColor(0.9, 0.9, 0.9), map_kd=None):
    self.name = name
    self.d = 1.0 # Opacity
    self.kd = kd if len(kd)==4 else kd + (self.d, )
    self.map_kd = map_kd
    self.ka = WFColor()
    self.ks = WFColor()
    # self.ke = (0.0, 0.0, 0.0)
    # self.illum = 2.0
    

  @classmethod
  def readMtl(cls, libMaterialName):
    '''Read a .mtl file and return a dictionary of WFMat.
    '''
    logging.info("Loading Material file:%s", libMaterialName)

    rin = open(libMaterialName, 'rt', errors='replace') 

    parser = PoserFileParser(rin)
    matDict = {}
    curMat = None
    
    while True:
      code,lw,rw = parser.getLine()
      lw = lw.lower()
      
      if code==PoserFileParser.TT_WORD:
        if lw=="newmtl": # New material
          curMat = WFMat(rw)
          matDict[rw] = curMat

        elif (lw=='ke') or (lw=='illum'):
          pass

        elif lw=="ka":
          tv = rw.split()
          curMat.ka = WFColor( float(tv[0]), float(tv[1]), float(tv[2]) )
        
        elif lw=="ks":
          tv = rw.split()
          curMat.ks = WFColor( float(tv[0]), float(tv[1]), float(tv[2]) )
        
        elif lw=="kd":
          tv = rw.split()
          curMat.kd = WFColor(float(tv[0]), float(tv[1]), float(tv[2]), curMat.d)

        elif lw=="d":
          curMat.d = float(rw)
          curMat.kd = WFColor(curMat.kd[0], curMat.kd[1], curMat.kd[2], curMat.d)

        elif lw=="map_kd":
          curMat.map_kd = rw
      elif code==PoserFileParser.TT_EOF:
        break
      else:
        raise Exception("L[%d] - Not Accepted : %s", parser.lineno(), lw)

    rin.close()

    return matDict

  


# =====================================================================================
class WaveGeom(object):
  '''WaveGeom class represent a WaveFront file and a geometric container for 3D objects
  This class represents a Geometry as it can be stored in a WaveFront file or
  embedded in Poser files.


  Design: (memory efficient)

    o-----------------------------------o
    | WaveGeom                          |
    +-----------------------------------+
    | coordList = list of Point3d       |
    |             Shared between groups |
    |                                   |
    | idem for texList and normList     |
    |                                   |     o--------------------------------------------------------o
    | groups = list of GeomGroup  ------|---> | GeomGroup                                              |
    |                                   |     +--------------------------------------------------------+
    o-----------------------------------o     | coordList, texList, normList point to WaveGeom ones    |
                                              |                                                        |
                                              | stripCount = list of int [ Nbface + 1 ]                |
                                              | o------------------------------------------------o     |
                                              | | 0  | 4  | ......                                     |
                                              | o------------------------------------------------o     |
                                              |   f0   f1                                              |
                                              |                                                        |
                                              | Face Attributs : TEXT|NORM (8bts) + material Index (24)|
                                              | matIdx = list of FaceAttr [ Nbface ]                   |
                                              | o------------------------------------------------o     |
                                              | | 0  | 3  | ......                                     |
                                              | o------------------------------------------------o     |
                                              |   f0   f1                                              |
                                              |                                                        |
                                              | vertIdx = list of int[] : Index of Vertex in coordList |
                                              | o------------------------------------------------o     |
                                              | | f0.0 | f0.1 | f0.2 | f0.3 | f1.0 | ....              |
                                              | o------------------------------------------------o     |
                                              |   Here: f0 has 4 vertex - Vertex order determines the  |
                                              |         face normal (ie direct order).                 |
                                              |                                                        |
                                              | tvertIdx and normIdx follow the same organization.     |
                                              | (They shall have the same length as vertIdx)           |
                                              |  if the GeomGroup has no texture or no normal)         |
                                              |                                                        |
                                              o--------------------------------------------------------o

  '''
  # Comparison constants
  VERTEX_EPS = 1e-6
  NORMAL_EPS = 1e-6
  TEX_EPS = 1e-6

  VERTEX_COUNT = 0x0001
  VERTEX_COORD = 0x0002
  TEXCOORD_COUNT = 0x0004
  TEXCOORD_COORD = 0x0008
  NORMAL_COUNT = 0x0010
  NORMAL_COORD = 0x0020
  GROUP_COUNT = 0x0040
  GROUP_NAME = 0x0080
  GROUP_NBFACE = 0x0100
  GROUP_STRIPIDX = 0x0200
  GROUP_NORMPRES = 0x0400
  GROUP_VERTIDX = 0x0800
  GROUP_TVERTIDX = 0x1000
  GROUP_NORMIDX = 0x2000
  MAT_COUNT = 0x4000
  MAT_NAMES = 0x8000


  def _selfInit(self):
    # Name of file
    self._name= ''

    #  The vertex list shared between groups
    self.coordList = []

    # The texture coordinates list
    self.texList = [ ] # public TexCoord2f[] 

    #   the normal list
    self.normList = []

    self.lstMat = [ ] # public List<String> ; // List of Material names

    self.curMatIdx = 0

    # Each face's & line's Geometry Group membership is kept here. . .
    # public List<GeomGroup> groups; // key = name of Group, value =
    self.groups = [ ]

    # Current group
    self.curGroup = None # protected AbsGeomGroup 

    self._curWriteMatIdx = 0

    # Name of optional Material file and associated dict of materials
    self._libMaterialName = ''
    self.libMat = {}

  def __init__(self, st=None, filename=None, usemtl=False, imgdirpath='.'):
    ''' Create a Wavefront geometry.
    Initialize temporary lists for reading operations.
    
    Parameters
    ----------
    st : optional input file 
      if None, Create an empty WaveGeom with a first default internal group 
      named "default".
      
    filename : optional, str, default is None
      file to set in 'Name' property. Not used for loading
      
    usemtl : optional, bool, default is False
      Indicate if material files (*.mtl) shall be read
      
    imgdirpath : optional, str, default is None
      list of directories separated by os.pathsep where to search
      texture files. (for usemtl = True)
      
    '''
    self._selfInit()
    self.setName(filename)
    
    self.curGroup = GeomGroup("default")
    self.curGroup.linkCoordList(self)
    self.usemtl = False
    self.imgdirpath = imgdirpath

    if st:
      self.usemtl = usemtl
      
      self.readInternal(st)
      
      if self.usemtl and self._libMaterialName:
        # Load the given .mtl File
        try:
          filedir = os.path.dirname(filename)
          
          self.libMat = WFMat.readMtl(os.path.join(filedir, self._libMaterialName))
          
          # TODO: Check Material usage in groups
        except FileNotFoundError:
          logging.warning("Material file read Error:%s", self._libMaterialName)
          
    if not self.lstMat:
      # When the WaveGeom is not created from a file 
      # a default material is required
      # FIX: Also required when the material list is empty at the end of the readInternal() call
      self.addMaterial("default") 
      

  def setName(self, n):
    self._name = n

  def getName(self): return self._name
  def getGroups(self): return self.groups
  def getMaterialList(self): return self.lstMat
  def getMaterialLibName(self): return self._libMaterialName  

  def setTexList(self, ntextab):
    self.texList = ntextab


  def copy(self, groups=None):
    ''' Return a deep copy of self, eventually restricted to given groups.
    Parameters
    ----------
      groups : List of GeomGroup or List of Group names or a GeomGroup or a GeomGroup name to keep
    '''
    wg = self.copyData()

    wg.setName(self._name)

    wg.texList = [ TexCoord2f(t) for t in self.texList ]

    wg.lstMat = [ s for s in self.lstMat ]
    wg._libMaterialName = self._libMaterialName

    lstGrps = []

    if groups:
      if isinstance(groups, str):
        lstGrps.append(self.getGroup(groups))
      elif isinstance(groups, GeomGroup):
        lstGrps.append(groups)
      else:
        lstGrps = [ (g if isinstance(g, GeomGroup) else self.getGroup(g)) for g in groups ]
      
    else:
      lstGrps = self.groups
      
    # Each face's Geometry Group membership is kept here. . .
    wg.groups = [ GeomGroup(src=ggd, inCoordList=wg.coordList) for ggd in lstGrps ]

    # Link correctly groups
    # FIX a major error
    wg.optimizeGroups()

    return wg

  def addMaterial(self, matName):
    ''' Add a material name to the list of materials.
    Search for existing material, if it already exists return the found index, 
    else add it at the end of the list.
    Set .curMatIdx to the new material index

    Parameters
    ----------
    matName : str
       Name of the material to add.
    Returns:
    int : The index of the material name in the list.
    '''
    try:
      i = self.lstMat.index(matName)
      self.curMatIdx = i

    except ValueError:
      self.lstMat.append(matName)
      self.curMatIdx = len(self.lstMat) - 1
      
    self.curGroup.setMaterialName(self.curMatIdx)

    return self.curMatIdx

  def selectMaterial(self, matName):
    ''' Select a material name as default current value (for read operation)
    Set .curMatIdx to the new material index

    Parameters
    ----------
    matName : str
       Name of the material to add.
    Returns:
    int : The index of the material name in the list.
    '''
    try:
      self.curMatIdx = self.lstMat.index(matName)

    except ValueError:
      self.curMatIdx = - 1
      
    self.curGroup.setMaterialName(self.curMatIdx)

    return self.curMatIdx


  def sanityCheck(self):
    ''' Check the consistency of a WaveGeom. '''
    
    gret = C_OK
    
    for grp in self.groups:
      print('Checking Group[{:s}]:'.format(grp.getName()))
      ret = grp.sanityCheck()
      if ret!=C_OK:
        print('Group has errors')
        gret = min(gret, ret)
        
    return gret





  def optimizeGroups(self, cleaning=False, radius=0.0):
    ''' Optimize the groups of this WaveGeom.
    Keep only Vertex, Texture coordinates and normal referenced (used) by faces.
    if a 'cleaning' is required, it also deduplicates vertex, using cleanDupVert method.
    
    After Vertex and texture coordinates are uniq.
    If cleaning is required a second optimization is performed to remove duplicated vertex 
    and duplicated faces
    
    Parameters
    ----------
    cleaning: boolean, optional, default False
      When true launch a cleanDupVert after the used vertex optimization
      
    radius: float, optional, default 0.0
      Maximum distance to fuse two vertexes
    
    Return
    ------
    int:
      C_OK if the vertex table has been reduced, else C_FAIL
    '''
    hasTexture = (self.texList!=None) and (len(self.texList) > 0)
    hasNormal  = (self.normList!=None) and (len(self.normList) > 0)
    nbInit = len(self.coordList)
    
    # Allocate mapping tables
    mapVert  = [-1] * nbInit
    mapTVert = [-1] * len(self.texList) #if hasTexture else None
    mapNVert = [-1] * len(self.normList) #if hasNormal else None
    
    for grp in self.groups:
      for vi in grp.vertIdx:
        # Just indicate that the vertex is used
        mapVert[vi] = 0
      
      for fao in grp.matIdx:
        if fao.fAttr & C_FACE_TEXT:
          for vti in fao.tvertIdx: # if i>=0 ]:
            mapTVert[vti] = 0
      
        if fao.fAttr & C_FACE_NORM:
          for vni in fao.normIdx: # if i>=0 ]:
            mapNVert[vni] = 0
        

    # Renumber vertex and filter the initial coord list
    nbVert = 0
    nCoordList = [ ]
    
    for i,vusage in enumerate(mapVert):
      if vusage==0:
        mapVert[i] = nbVert
        nCoordList.append(self.coordList[i])
        nbVert += 1

    for grp in self.groups:
      grp.vertIdx[:] = array.array('l', [ mapVert[vi] for vi in grp.vertIdx ])
    
    self.coordList = nCoordList
    logging.info("Unused Vertex Optimization=%d/%d", len(self.coordList), nbInit)
    
    # Optimize unused texture coordinates
    if hasTexture:
      nbInitTex = len(self.texList)
      nTexList = []
      nbTVert = 0
      for i,vusage in enumerate(mapTVert):
        if vusage==0:
          mapTVert[i] = nbTVert
          nTexList.append(self.texList[i])
          nbTVert += 1
  
      for grp in self.groups:
        for fao in grp.matIdx:
          if fao.fAttr & C_FACE_TEXT:
            fao.tvertIdx[:] = array.array('l',  [ mapTVert[vti] for vti in fao.tvertIdx ])        
        
      self.texList = nTexList
      logging.info("Unused Texture Optimization=%d/%d", len(self.texList), nbInitTex)
    
    # Optimize unused normals
    if hasNormal:
      nbInitNorm = len(self.normList)
      nNormList = []
      nbNVert = 0
      for i,vusage in enumerate(mapNVert):
        if vusage==0:
          mapNVert[i] = nbNVert
          nNormList.append(self.normList[i])
          nbNVert += 1
  
      for grp in self.groups:
        for fao in grp.matIdx:
          if fao.fAttr & C_FACE_NORM:
            fao.normIdx[:] = array.array('l', [ mapNVert[vti] for vti in fao.normIdx ])
        
      self.normList = nNormList
      logging.info("Unused Normal Optimization=%d/%d", len(self.normList), nbInitNorm)
    
    for gg in self.groups:
      gg.linkCoordList(self)

    if cleaning:
      self.cleanDupVert(radius, deDupFace=True)

    return C_OK if nbInit>len(self.coordList) else C_FAIL



  def cleanDupVert(self, radius=0.0, deDupFace=False):
    ''' Clean duplicated vertex, ie. merge vertex that are closer than 'radius'.
    Does not take into account whenever vertex are used or not.
    
    Parameters
    ----------
    radius: float, optional, default 0.0
      Maximum distance to fuse two vertexes
    
    deDupFace: bool, optional, default False
      Indicate do remove duplicated faces for deduplicated vertexes
    
    Return
    ------
    int:
      C_OK if the vertex table has been reduced, else C_FAIL
    '''
    nbsrc = len(self.coordList)

    logging.info("Start Cleaning for %s [%d vertex]", self.getName(), nbsrc)

    # Create a numpy table Nx3
    npTab = np.zeros( (nbsrc, 3) )
    for refNo, p in enumerate(self.coordList):
      npTab[refNo] = [ p.x, p.y, p.z ]

    # Create an KDtree with the numpy table
    tree = spatial.KDTree(npTab, leafsize=10 if nbsrc<10000 else 100)
      
    # Return the list of list of indexes of nearest neighboors
    mapVert = tree.query_ball_point(npTab, radius, return_sorted=True)

    # nCoordLst new list of deduplicated vertex
    nCoordLst = []
    nMapVert = [-1] * nbsrc
    curIdx = 0
    # Deduplicated vertex index list
    deDupIdx = [ ]
    
    for i,p in enumerate(self.coordList):
      if len(mapVert[i])==1: # No duplicated vertex
        nCoordLst.append(p)
        nMapVert[i] = curIdx
        curIdx += 1
        
      else: # The point is found more than once
        # The list of index is sorted, so the first index is the smallest
        # 2 cases : either the point has already been found or not
        if mapVert[i][0] == i:
          nCoordLst.append(p)
          nMapVert[i] = curIdx
          deDupIdx.append(curIdx)
          curIdx += 1
        else:
          # The index of the point is greater than a smallest
          # Use the mapping of the smallest
          nMapVert[i] = nMapVert[mapVert[i][0]]

    nbnew = len(nCoordLst)
    if nbnew == nbsrc:
      logging.info("No optimization")
      return C_FAIL
    
    for gg in self.groups:
      gg.vertIdx[:] = array.array('l', [ nMapVert[vi] for vi in gg.vertIdx ] )

    self.setCoordList(nCoordLst)

    logging.info("Optimized to %d vertex", nbnew)
    
    if deDupFace and deDupIdx:
      for gg in self.groups:
        prevNbFace = gg.getNbFace()
        
        for curIdx in deDupIdx:
          lstFaceCandidate = []
          for faceno in range(gg.getNbFace()):
            faceIndexes = gg.getFaceVertIdx(faceno)
            if curIdx in faceIndexes:
              # Rotate faceIndexes to have the smaller index first
              minIdx = min(faceIndexes)
              minPos = faceIndexes.index(minIdx)
              if minPos > 0:
                faceIndexes[:] = faceIndexes[minPos:] + faceIndexes[0:minPos]
              
              lstFaceCandidate.append( (faceno, faceIndexes) )
        
          # lstFace contains a list of (faceno, face vertex indexes) where curIdx vertex is used
          lstToRemove = []
          for i,fRef in enumerate(lstFaceCandidate):
            for fOther in lstFaceCandidate[i+1:]:
              if fOther[1] == fRef[1]:
                # Remove fOther[0] face
                lstToRemove.append(fOther[0])
        
          # Order face to remove in back order
          if lstToRemove:
            # Remove faces starting by the highest indexes
            # to prevent bad re-indexation
            lstToRemove.sort(reverse=True)
            for faceno in lstToRemove:
              gg.removeFace(faceno)
            
        logging.info("Group %s optimized from %d to %d faces", gg.getName(), prevNbFace, gg.getNbFace()) 
        
    return C_OK





  #
  #    * @see deyme.v3d.wf.WaveGeom#createGeomGroup(java.lang.String)
  #    
  def createGeomGroup(self, name):
    ''' Create a new GeomGroup in the WaveGeom.
    Return the already existing one if the same name exists.
    Parameters
    ----------
    name : str
      Name of the new GeomGroup
    '''
    gg = None
    #  Very rare : need to create a group with a name
    if name:
      gg = self.getGroup(name)
    else:
      no = 0
      while True:
        name = f'default{no}'
        gg = self.getGroup(name)
        no += 1
        if not gg:
          break

    if not gg:
      gg = GeomGroup(name)
      gg.linkCoordList(self)
      #  Bug found : 10FEV2008
      self.groups.append(gg)

    return gg


  def extractGeomGroup(self, grp, name, matidx):
    ''' Create a group within the current WaveGeom with the set of faces from 'grp' 
    group that have the given material index.
    
    Parameters
    ----------
    grp : GeomGroup
    The source group where to search faces
    
    name : str
    Name for the new group.
    
    matidx : integer
    Index of the material in the current WaveGeom material list
    
    Return
    ------
      GeomGroup : New group
    '''
    tmpGrp = self.createGeomGroup(name)
    tmpGrp.curMatIdx = matidx
    
    # Create a list that maps new group face indexes to orignal face indexes
    tmpGrp.origFaceLst = []
    for i,fao in enumerate(grp.matIdx):
      if fao.fAttr & C_FACE_MATMASK == matidx:
        # Add the face to the tmpGrp (fast)
        tmpGrp.addFace(grp.getFaceVertIdx(i), grp.getFaceTVertIdx(i), grp.getFaceNormIdx(i))
        
        # Record original face index
        tmpGrp.origFaceLst.append(i)
        
    return tmpGrp

  # public void readInternal(PoserFileParser st)
  def readInternal(self, st): # PoserFileParser st)
    ''' Internal WaveGeom reader '''
    numbVerts, numbTVerts, numbTSets, numbElems, numbSets = -1, -1, -1, -1, -1

    fin = False
    while not fin:
      code,lw,rw = st.getLine()
      
      if code == PoserFileParser.TT_WORD:
        if lw=="v":
          self.coordList.append(st.readVertex())
          continue

        if lw=="vt":
          self.texList.append(st.readTexture())
          continue

        if lw=="vn":
          self.normList.append(st.readNormal())
          continue

        if lw=="f" or lw=="fo": # Old keyword 'fo' to be manage as 'f' (Sepc OBJ v3.0)
          ret = self.readFace(st)
          if ret:
            logging.warning('Line[%d] Face has incorrect %s indexe(s)', st.lineno(), 'texture and normal' if ret==C_FACE_TEXTNORM else ('texture' if ret==C_FACE_TEXT else 'normal'))
          continue

        if lw=="l":
          self.readLine(st)
          continue

        if lw=="numbVerts":
          numbVerts = int(rw)
          continue

        if lw=="numbTVerts":
          numbTVerts = int(rw)
          continue

        if lw=="numbTSets":
          numbTSets = int(rw)
          continue

        if lw=="numbElems":
          numbElems = int(rw)
          continue

        if lw=="numbSets":
          numbSets = int(rw)
          continue

        if lw=='usemtl':
          # FIX 20110314-ODY: Material names could contain white chars and others (like #)
          self.addMaterial(rw)
          continue

        if lw=="s":
          continue

        if lw=="g":
          self.curGroup = self.createGeomGroup(rw)
          self.curGroup.setMaterialName(self.curMatIdx)
          continue

        # Record mtllibs that could be read and resolved later
        if lw=='mtllib': # rw should read a FILENAME
          if st.getFileNature()==OBJ_FNAT:
            self._libMaterialName = rw
          continue

        if (lw[0]=="g") and (len(st.sval) > 1):
          # Strange case where there's no space after 'g' (OBJ regular ??)
          self.curGroup = self.createGeomGroup(lw[1:])
          self.curGroup.setMaterialName(self.curMatIdx)
          continue

      elif (code==PoserFileParser.TT_RIGHTBRACKET) or (code==code==PoserFileParser.TT_EOF):
        fin = True
      else:
        # log.warning("L[" + st.lineno() + "] - Not Accepted :" + lw)
        raise Exception("L[%d] - Not Accepted : %s", st.lineno(), lw)

    # Ensure that the default group is kept (may append)
    if ((st.getFileNature() != OBJ_FNAT) and not self.groups) or \
        (not self.curGroup in self.groups):
      self.groups.append(self.curGroup)      

    # Relink Groups
    for gg in self.groups:
      gg.linkCoordList(self)

    # return a tuple of values (for Poser usage)
    return (numbVerts, numbTVerts, numbTSets, numbElems, numbSets)

    

  def readFace(self, st): # throws ParsingErrorException
    ''' Adds the indices of the current face to the arrays.
     
    ViewPoint files can have up to three arrays: Vertex Positions, Texture
    Coordinates, and Vertex Normals. Each vertex can contain indices into all
    three arrays.
    '''
    ret = C_OK
    vertIndex, texIndex, normIndex = 0, 0, 0
    coordIdxList, texIdxList, normIdxList = [ ], [ ], [ ]
     
    #   There are n vertices on each line. Each vertex is comprised
    #   of 1-3 numbers separated by slashes ('/'). The slashes may
    #   be omitted if there's only one number.

    line = st.rval

    tabVert = line.split(" ")

    if tabVert:
      for i in range( 0, len(tabVert)):
        sana = tabVert[i]
        posS1 = sana.find('/')
        vertIndex = int(sana[0:posS1] if (posS1 > 0) else sana) - 1

        if vertIndex < 0:
          # FIX 20081231 : when reading a file, the real coord list is unknown 
          # ==> Use the temporary list
          vertIndex += len(self.coordList) + 1

        coordIdxList.append(vertIndex)

        if posS1 > 0:
          posS2 = sana.find('/', posS1 + 1)

          if posS2 > 0:
            if (posS2 > posS1 + 1):
              texIndex = int(sana[posS1+1:posS2]) - 1
              if texIndex < 0:
                # FIX 20081231 : when reading a file, the real coord list is unknown 
                texIndex += len(self.texList) + 1

              if texIndex>=0 and texIndex<len(self.texList):
                texIdxList.append(texIndex)
              else: #print('Incorrect Texture index at line:{:d}'.format(st.lineno()))
                ret |= C_FACE_TEXT 

            if posS2 < len(sana) - 1:
              normIndex = int(sana[posS2 + 1:]) - 1
              if (normIndex < 0):
                # FIX 20081231 : when reading a file, the real coord list is unknown 
                normIndex += len(self.normList) + 1

              if normIndex>=0 and normIndex<len(self.normList):
                normIdxList.append(normIndex)
              else: # print('Incorrect Normal index at line:{:d}'.format(st.lineno()))
                ret |= C_FACE_NORM
                
          else:
            texIndex = int(sana[posS1 + 1:]) - 1
            if texIndex < 0:
              # FIX 20081231 : when reading a file, the real coord list is unknown 
              texIndex += len(self.texList) + 1

            if texIndex>=0 and texIndex<len(self.texList):
              texIdxList.append(texIndex)
            else: #print('Incorrect Texture index at line:{:d}'.format(st.lineno()))
              ret |= C_FACE_TEXT 

      # Add face to current groups
      self.curGroup.addFace(coordIdxList, texIdxList, normIdxList)
      
    return ret
    # // End of readFace

  def readLine(self, st):
    ''' Adds the indices of the current line to the arrays.
    ViewPoint files can have up to two arrays: Vertex Positions, Texture
    Coordinates. Each vertex can contain indices into all two arrays.
    '''
    ret = C_OK
    vertIndex, texIndex = 0,0
    coordIdxList, texIdxList = [ ], [ ]
    
    # There are n vertices on each line. Each vertex is comprised
    # of 1-2 numbers separated by slashes ('/'). The slashes may
    # be omitted if there's only one number.
    # st.getToken()
    line = st.rval
    tabVert = line.split(" ")

    if tabVert:
      for i in range( 0, len(tabVert)):
        sana = tabVert[i]
        posS1 = sana.find('/')
        vertIndex = int(sana[0:posS1] if (posS1 > 0) else sana) - 1

        if vertIndex < 0: # Relative Index
          vertIndex += len(self.coordList) + 1

        coordIdxList.append(vertIndex)

        if posS1 > 0:
          posS2 = sana.find('/', posS1 + 1)

          if posS2 > 0:
            if (posS2 > posS1 + 1):
              texIndex = int(sana[posS1+1:posS2]) - 1
              if texIndex < 0:
                texIndex += len(self.texList) + 1
                
              if texIndex>=0 and texIndex<len(self.texList):
                texIdxList.append(texIndex)
              else: #print('Incorrect Texture index at line:{:d}'.format(st.lineno()))
                ret |= C_FACE_TEXT 
      # End Of for

      # Add face to current groups
      self.curGroup.addLine(coordIdxList, texIdxList)
      return ret
    # End of readLine

  # FIXME: 20200713 def getTexListLength(self): return self.numbTVerts

  def getGroupName(self): 
    return self.groups[0]._name if len(self.groups) else None

  # public int getNbGroup() { return groups.size() } 

  # public GeomGroup getGroup(String name)
  def getGroup(self, name):
    ''' Retrieve a group by its name.
    For compatibility reason with Poser files, this function also searchs
    the name + ':1'
    Parameters
    ----------
    name : str
      Name of the GeomGroup
    ''' 
    idx = name.rfind(':')
    altname = name[0:idx] if idx >= 0 else name + ":1"

    lg = [ g for g in self.groups if (name==g._name) or (altname==g._name) ]

    return lg[0] if lg else None

  def getNbFace(self):
    nf = 0

    for grp in self.groups:
      nf += grp.getNbFace()

    return nf

  # public TexCoord2f getTexCoord(int idx) { return texList[idx] }


  # abstract public void writeFormattedVertex(PrintWriter fw, String nPfx, DecimalFormat fmt)
  # abstract public void writeFormattedNormal(PrintWriter fw, String nPfx, DecimalFormat fmt)
  # abstract public boolean hasNormals()
  def writeFormattedVertex(self, fw, nPfx):
    for p in self.coordList:
      fw.write(f"{nPfx}v {p.x: 11.8f} {p.y: 11.8f} {p.z: 11.8f}\n")
          
    fw.write('\n')

  def writeFormattedNormal(self, fw, nPfx):
    for vn in self.normList:
      fw.write(f"{nPfx}vn {vn.x: 11.8f} {vn.y: 11.8f} {vn.z: 11.8f}\n")
  

  def hasNormals(self):
    return self.normList != None and len(self.normList)



# TODO: Compute Normals if none and required
#     if self.hasNormal and not geom.normList:
#       nidx = 0 
#       for grp in geom.getGroups():
#         vertIdxTbl = grp.vertIdx
#         
#         for noface in range(0, grp.getNbFace()):
#           startIdx = grp.getFaceStartIdx(noface)
#           lastIdx = grp.getFaceLastIdx(noface)
#           argc = lastIdx - startIdx
#   
#           v0 = vertIdxTbl[startIdx]
#           v1 = vertIdxTbl[startIdx+1]
#           v2 = vertIdxTbl[startIdx+2]
# 
#           lv1 = geom.coordList[v0]     
#           a = Point3d(geom.coordList[v1]).sub(lv1)
#           b = Point3d(geom.coordList[v2]).sub(lv1)
#           n = a.cross(b)
#           n.normalize()
#           
#           geom.normList.append(n)
#           
#           # Give the same normal to each vertex (Ugly)
#           grp.normIdx.extend( [nidx] * argc )
# 
#           nidx += 1

  # public void writeVertex(PrintWriter fw, String nPfx, boolean writeNormals)
  def writeVertex(self, fw, nPfx, writeNormals): # PrintWriter fw, String nPfx, boolean writeNormals)
    # Print Vertex
    self.writeFormattedVertex(fw, nPfx)

    # Print Texture Vertex
    for tex in self.texList:
      fw.write(f"{nPfx}vt {tex.x: 11.8f} {tex.y: 11.8f}\n")

    fw.write('\n')

    if writeNormals:
      self.writeFormattedNormal(fw, nPfx)

  # private void writeFace(PrintWriter fw, String nPfx, String gn, AbsGeomGroup gg, boolean writeNormals)
  def writeFace(self, fw, nPfx, gn, gg, writeNormals):
    fw.write(f"{nPfx}g {gn}\n")

    for faceno,fao in enumerate(gg.matIdx):
      startIdx = gg.stripCount[faceno]
      lastIdx = gg.stripCount[faceno + 1]

      if self._curWriteMatIdx != fao.fAttr & C_FACE_MATMASK:
        self._curWriteMatIdx = fao.fAttr & C_FACE_MATMASK
        fw.write(f"\n{nPfx}usemtl {self.lstMat[self._curWriteMatIdx]}\n")
        
      fa = fao.fAttr & (C_FACE_TEXTNORM if writeNormals else C_FACE_TEXT)
      fw.write("\nf")
      vidx = gg.vertIdx
      if fa==0:
        for i in range(startIdx, lastIdx):
          fw.write(f" {vidx[i] + 1}")
      elif fa==C_FACE_TEXTNORM:
        for j,i in enumerate(range(startIdx, lastIdx)):
          fw.write(f" {vidx[i] + 1}/{fao.tvertIdx[j] + 1}/{fao.normIdx[j] + 1}")
      elif fa==C_FACE_TEXT:
        for j,i in enumerate(range(startIdx, lastIdx)):
          fw.write(f" {vidx[i] + 1}/{fao.tvertIdx[j] + 1}")
      else:
        for j,i in enumerate(range(startIdx, lastIdx)):
          fw.write(f" {vidx[i] + 1}//{fao.normIdx[j] + 1}")
       
    fw.write('\n')

  # private void writeLine(PrintWriter fw, String nPfx, String gn, AbsGeomGroup gg)
  def writeLine(self, fw, nPfx, gn, gg):

    for lineno, lao in enumerate(gg.matLineIdx):
      startIdx = gg.lineStripCount[lineno]
      lastIdx = gg.lineStripCount[lineno + 1]

      if self._curWriteMatIdx != lao.fAttr&C_FACE_MATMASK:
        self._curWriteMatIdx = lao.fAttr&C_FACE_MATMASK
        fw.write(f"{nPfx}usemtl {self.lstMat[self._curWriteMatIdx]}\n")

      fw.write(nPfx + "l")
      # FIX20160910 : Do not write false texture Id (make Poser9 KO)
      if lao.fAttr & C_FACE_TEXT:
        for i in range(startIdx, lastIdx):
          fw.write(f" {gg.vertLineIdx[i] + 1}/{gg.tvertLineIdx[i] + 1}")
      else:
        for i in range(startIdx, lastIdx):
          fw.write(f" {gg.vertLineIdx[i] + 1}")

      fw.write('\n')

  # public void writeGroups(PrintWriter fw, String nPfx, boolean writeNormals)
  def writeGroups(self, fw, nPfx, writeNormals, writeOBJName=False): 
    self._curWriteMatIdx = -1

    for gg in self.groups:
      if writeOBJName: # Should only append in 'real' .obj format
        fw.write(f"o {gg._name}\n")
        
      self.writeFace(fw, nPfx, gg._name, gg, writeNormals)
      self.writeLine(fw, nPfx, gg._name, gg)

  # public void writeInOBJ(PrintWriter fw, String nPfx)
  def writeInOBJ(self, fw, nPfx, writeOBJName=False):
    # self.writeConst(fw, "# " + nPfx, None)
    fw.write(f"{nPfx}# Generated by pypos3d\n")
    fw.write(f"{nPfx}mtllib default.mtl\n")
    self.writeVertex(fw, nPfx, True)
    self.writeGroups(fw, nPfx, True, writeOBJName=writeOBJName)

  def writeOBJ(self, fileName, writeOBJName=False):
    ''' Write the WaveGeom in a WaveFront format file (.obj) 
    Paramters
    ---------
    filename : str
      Path of the file to create.
    writeOBJName : bool, optional, default False
      if True the write operation create one 'o ObjetName' line for each group
      Not correctly supported by Poser
    Returns
    -------
    int : C_OK, C_ERROR
    '''
    ret = C_OK
    fout = None
    try:
      fout = open(fileName, 'w')
      self.writeInOBJ(fout, "", writeOBJName=writeOBJName)
      fout.close()

    except FileNotFoundError:
      if WFBasic.PYPOS3D_TRACE: print(f'File Not Found Error:{fileName}')
      ret = C_ERROR

    except OSError as e: # (IOException ioex)
      if WFBasic.PYPOS3D_TRACE: 
        traceback.print_last()
        print(f'Write Error:{e}')
      ret = C_ERROR
      
    finally:
      if fout:
        fout.close()

    return ret

  # public int writeOBZ(String fileName)
  def writeOBZ(self, fileName):
    ''' Write the WaveGeom in a compressed WaveFront format file (.obz = .obj + gzip) 
    Paramters
    ---------
    filename : str
      Path of the file to create.
    Returns
    -------
    int : C_OK, C_ERROR
    '''
    ret = C_OK
    fout = None
    try:
      fout = gzip.open(fileName, 'wt')
      self.writeInOBJ(fout, "")
      fout.close()

    except FileNotFoundError:
      if WFBasic.PYPOS3D_TRACE: print(f'File Not Found Error:{fileName}')
      ret = C_ERROR
      
    except OSError as e: # (IOException ioex)
      if WFBasic.PYPOS3D_TRACE: 
        traceback.print_last()
        print(f'Write Error:{e}')
      ret = C_ERROR
      
    finally:
      if fout:
        fout.close()

    return ret


  def save(self, fn, version=""):
    ''' Write a WaveFront file in text mode or in compressed mode.
    Use the extension to find the right mode.
    Set current object name to 'fn'
    
    Parameters
    ----------
    fn : str
      Full path name
      
    version : str, optional
      Unused parameter to have the same signature as PoserFile

    Returns
    -------
    int
      C_OK write without error, C_ERROR a write error has occurred
    '''
    if GetLowExt(fn)== 'obj': 
      ret = self.writeOBJ(fn)
    else:
      ret = self.writeOBZ(fn)

    self.setName(fn)

    return ret




  # Find the Egde vextex based on 'findEdges' method.
  # Group is supposed to be alone in the GeomCustom.
  #   
  # @return the table of index of the edge vertex
  #
  #  public int[] findEdgeCoord()
  # def findEdgeCoord(self):
  #   gName = self.getGroupName()
  #   ng = self.getGroup(gName)
  #   return ng.findEdgeCoord()


  #  public int[] extractSortJonction(String pBasName, String pHautName)
  def extractSortJonction(self, pBasName, pHautName):
    ''' Return the list of  ... internal stuff '''
    gBas = self.getGroup(pBasName)
    if not gBas:
      logging.warning("Groupe Bas[%s] NO faces", pBasName )
      return None

    logging.info("Groupe Bas[%s]: %d faces", pBasName, gBas.getNbFace())

    gHaut = self.getGroup(pHautName)
    if not gHaut:
      logging.warning("Groupe Bas[%s] NO faces", pHautName )
      return None

    logging.info("Groupe Haut[%s]: %d faces", pHautName, gHaut.getNbFace()) 

    # Find common vertex index and sort them : comCoordOrig = findCommonPoints(gBas.vertIdx, gHaut.vertIdx)
    comCoordOrig = list(set(gBas.vertIdx) & set(gHaut.vertIdx))
    comCoordOrig.sort()

    logging.info("ComPoints[]: %d points", len(comCoordOrig))

    
    comCoord = None

    if comCoordOrig:
      logging.info("Extracting Jonction : %s/%s", pBasName, pHautName)
      grp = self.getGroup(pBasName)
      nVertIdx = self.calcGroupVertIndex(grp)
      comCoord = [ nVertIdx.index(vi) for vi in comCoordOrig ]

    return comCoord

  #  public void copyMat(AbsWaveGeom src) : Dangerous because of the default material name
  #def copyMat(self, src):
  #  self.lstMat += src.lstMat


  # Calculate for a Group the mapping table for Vertex 
  # beween group index and global GeomCustom index.
  #@return    the mapping table. 
  #           res[i] is the index in the GeomCustom vertex table.
  #  public int[] calcGroupVertIndex(GeomGroup g)
  def calcGroupVertIndex(self, grp):
    svi = set( grp.vertIdx )
    nVertIdx = list(svi)
    nVertIdx.sort()
    return nVertIdx

  # Calculate for a Group the mapping table for Texture Coordinates 
  # between group index and global GeomCustom index.
  #
  # @return    the mapping table. 
  #            res[i] is the index in the GeomCustom vertex table.
  #  public int[] calcGroupTVertIndex(GeomGroup g)
  def calcGroupTVertIndex(self, grp):
    # FIX 20101002 : If geom has no texture - fill the TVertIndex with "0"
    if not self.texList:
      return [ ] # * len(grp.tvertIdx)

    stvertidx = set( [ vti for fao in grp.matIdx for vti in fao.tvertIdx if fao.fAttr & C_FACE_TEXT ] )
    nTvertIdx = list(stvertidx)

    nTvertIdx.sort()
    return nTvertIdx

  #
  #
  #  public int[] calcGroupNormIndex(GeomGroup g)
  def calcGroupNormIndex(self, grp):
    # A group without normals in a global geom that contains some normals 
    if not self.normList:
      return [ ]
    
    snvertidx = set( [ vti for fao in grp.matIdx for vti in fao.normIdx if fao.fAttr & C_FACE_NORM  ] )

    nNormIdx = list(snvertidx)

    nNormIdx.sort()
    return nNormIdx

  #----------------------------------------------------------------------
  #  public WaveGeom extractSortGeom(String groupName)
  def extractSortGeom(self, groupName):
    ''' Extract the group of the given name and create a new WaveGeom
    that contains a <u>deep copy</u> of the original data.
    
    Parameters
    ----------
    groupName : str

    Returns
    -------
    WaveGeom : a new optimized WaveGeom
    '''
    logging.info('Extracting :%s', groupName)
    grp = self.getGroup(groupName)
    if not grp:
      return None

    gc = WaveGeom()
    gc.lstMat = copy.copy(self.lstMat)

    ngrp = gc.createGeomGroup(groupName if (grp.getName()==None) else grp.getName())
        
    nbInit = len(self.coordList)
    
    nTexList, nNormList = [], []
    
    # A sort on vertex indexes is required (by Poser Morphs)
    sidx = set(grp.vertIdx)
    lidx = list(sidx)
    lidx.sort()
    ngrp.vertIdx = array.array('l', [ bisect.bisect(lidx, vi)-1 for vi in grp.vertIdx ])
    nCoordList = [ Point3d(self.coordList[vi]) for vi in lidx ]
    
    # Remap Texture Coordinates          
    mapTVert = [-1] * len(self.texList)
    mapNVert = [-1] * len(self.normList)
    
    for fao in grp.matIdx:      
      nfao = FaceAttr(fao)
      ngrp.matIdx.append(nfao)
      
      if fao.fAttr & C_FACE_TEXT:
        for i, vti in enumerate(fao.tvertIdx):
          nvti = mapTVert[vti]
          if nvti<0:
            nvti = len(nTexList)
            nTexList.append(TexCoord2f(self.texList[vti]))
            mapTVert[vti] = nvti
        
          nfao.tvertIdx[i] = nvti

      if fao.fAttr & C_FACE_NORM:
        # Remap Normal Coordinates          
        for i, vti in enumerate(fao.normIdx):
          nvti = mapNVert[vti]
          if nvti<0:
            nvti = len(nNormList)
            nNormList.append(Vector3d(self.normList[vti]))
            mapNVert[vti] = nvti
      
          nfao.normIdx[i] = nvti

    gc.coordList = nCoordList
    gc.texList   = nTexList
    gc.normList  = nNormList
    
    ngrp.linkCoordList(gc)
    ngrp.setMaterialName(grp.curMatIdx)
    
    
    # Copy the faces 
    ngrp.stripCount = copy.copy(grp.stripCount) # [:-1] + [ sc+vertpos for sc in angrp.stripCount ]
    
    logging.info("End Result [%s:%d faces, %d Vx, %d Tx]", ngrp.getName(), ngrp.getNbFace(), len(nCoordList), len(nTexList))
    
    logging.info("End with Vertex Optimization=%d/%d", len(nCoordList), nbInit)

    return gc

  

  #  public int findMinDist(Point3d p, int noMax, double treshhold)
  def findMinDist(self, p, noMax=-1, treshhold=FEPSILON):
    idx = -1
    minDist = sys.float_info.max
    noMax = len(self.coordList) if noMax==-1 else min(noMax, len(self.coordList))
    for i in range(0, noMax):
      pe = self.coordList[i]
      d = p.distance(pe)
      if ((d < treshhold) and (d < minDist)):
        minDist = d
        idx = i

    return idx

  #  (non-Javadoc)
  #    * @see deyme.v3d.wf.WaveGeom#scale(double, double, double)
  #    
  def scale(self, ex, ey, ez):
    ''' Scale all vertex along axis '''
    for p in self.coordList:
      p.x *= ex
      p.y *= ey
      p.z *= ez

  def translate(self, tx, ty, tz):
    ''' Translate all vertex '''
    for p in self.coordList:
      p.x += tx
      p.y += ty
      p.z += tz

  #  def centerGeom(self, tx, ty, tz, rx, ry, rz):
#   def centerGeom(self, tx, ty, tz, rx, ry, rz):
#     raise RuntimeError('Not Implemented')
#      self.translate(-tx, -ty, -tz)
#      matRz = Matrix3d([None]*)
#      i = 0
#      while i < getCoordListLength():
#          matRz.transform(getPoint(i))
#          i += 1
#      matRx = Matrix3d([None]*)
#      i = 0
#      while i < getCoordListLength():
#          matRx.transform(getPoint(i))
#          i += 1
#      matRy = Matrix3d([None]*)
#      i = 0
#      while i < getCoordListLength():
#          matRy.transform(getPoint(i))
#          i += 1

  def getCoordListLength(self):
    ''' Return the size of the vertex list. '''
    return len(self.coordList)

  def getCoordList(self):
    ''' Return a deep copy of the vertex list (.coordList) '''
    return [ Point3d(p) for p in self.coordList ]

  # Return a copy of the Texutre List
  def getTexList(self):
    ''' Return a deep copy of the texture list (.texList) '''
    return [ TexCoord2f(p) for p in self.texList ]

  # Return a copy of the normal list
  def getNormList(self):
    ''' Return a deep copy of the normal list (.normList) '''
    return [ Vector3d(p) for p in self.normList ]

  def setCoordList(self, cl):
    self.coordList = cl
    for gg in self.groups:
      gg.linkCoordList(self)

  #
  def applySymZY(self):
    ''' Apply an Oyz symetry. '''
    for p in self.coordList:
      p.x = -p.x

    for gg in self.groups:
      gg.invertFaceOrder()



  def fusion(self, inLst, outMapLst=None):
    ''' Fusion the current WaveGeom with a list of other WaveGeoms.
    Parameters
    ----------
    inLst : list of WaveGeom
      The List of WaveGeom to insert in self. (Not modified??)
    outMapLst : None or empty list
      Out data : returns for each WaveGeom the mapping of vertex between it
      and the fusioned WaveGeom (required by morph update) 
    '''
    logging.info("Start Fusion for %s", self.getName())
    nbMaxVerts = len(self.coordList)
    nbMaxTVerts = len(self.texList)
    nbMaxFaces = self.getNbFace()

    # Prepare the temporary list of vertex
    for curGeom in inLst:
      nbMaxVerts += len(curGeom.coordList)
      nbMaxTVerts += len(curGeom.texList)
      nbMaxFaces += curGeom.getNbFace()

    # Copy original data
    tmpCoordList = copy.copy(self.coordList)
    tmpTexList = copy.copy(self.texList)
    logging.info("Temporary List created : %d/%d", nbMaxVerts, nbMaxTVerts)

    # Prepare the face deduplication data
    tabHshFace = [ ] # [None]*nbMaxFaces
    tabFaceIdx = [ ] # [None]*nbMaxFaces
    nbTotFace = 0
    for curGrp in self.groups:
      nbTotFace = curGrp.fillDedupFace(nbTotFace, tabHshFace, tabFaceIdx)
    logging.info("Init Dedup Face table with : %d/%d", nbTotFace, nbMaxFaces)

    # For each incomming GeomCustom
    for curGeom in inLst:
      # Create a mapping table for Vertex of that GeomCustom
      mapVert = [ ]
      #prevMax = len(tmpCoordList)

      # Record the mapping table for external usage
      if outMapLst:
        outMapLst.append(mapVert)

      nbsrc = len(tmpCoordList)
      npTab = np.zeros( (nbsrc, 3) )
      for pNo, p in enumerate(tmpCoordList):
        npTab[pNo] = [ p.x, p.y, p.z ]
    
      # Create an KDTree with the 'known Vertex' in a "global" np.array
      tree = spatial.KDTree(npTab, leafsize=10 if nbsrc<10000 else 100)

      svect = np.zeros((1,3))
      prevNbCoord = nbsrc

      # For each Vertex of the current incomming Geom
      for curPt in curGeom.coordList:
        # Search in KDTtree
        svect[0] = [ curPt.x, curPt.y, curPt.z ]
        rest, resIdx = tree.query(svect)

        # if found (not too far) ==> Put it in a tmp table
        if rest[0]<2.0e-6:
          # Use an existing vertex
          newIdx = resIdx[0]
        else:
          # Add a new vertex to the global list
          newIdx = nbsrc
          nbsrc+=1
          tmpCoordList.append(curPt)

        #mapVert[noVert] = newIdx
        mapVert.append(newIdx)

      # Extend the np.array with the new Vertex
      npTabExt = np.zeros( (nbsrc-prevNbCoord, 3) )
      for pNo,p in enumerate(tmpCoordList[prevNbCoord:nbsrc]):
        npTabExt[pNo] = [ p.x, p.y, p.z ]
      npTab = np.vstack((npTab,npTabExt))

      # Create a mapping table for TVertex of that GeomCustom
      nbtv = len(curGeom.texList)
      mapTVert = [ nbtv+i for i in range(0,nbtv) ]
      # Add all the Texture vertex to the global list
      tmpTexList += curGeom.texList

      # Copy the faces taking into account the mapping table
      for curGrp in curGeom.groups:
        
        # Remap vertex indexes
        for i in range(0, len(curGrp.vertIdx)):
          curGrp.vertIdx[i] = mapVert[curGrp.vertIdx[i]]
          
        # Deduplicate faces
        tabKeptFace = [ False ] * curGrp.getNbFace()
        nbKeptFace = 0
        idxFirstFace = nbTotFace

        for faceno in range(curGrp.getNbFace()):
          startIdx = curGrp.stripCount[faceno]
          lastIdx = curGrp.stripCount[faceno+1]
          idxTab = curGrp.vertIdx[startIdx:lastIdx]
          nbv = lastIdx - startIdx
          # Find lowest index
          lowestIdx = LowestIdxPos(idxTab)
          finalIdxTab = [ idxTab[(i + lowestIdx) % nbv] for i in range(0, nbv) ]

          hashVal = sum(finalIdxTab)
          i = 0
          while i < nbTotFace:
            if (tabHshFace[i]==hashVal) and finalIdxTab==tabFaceIdx[i]:
              # The face already exists in the fusioned geom
              break
            i += 1

          # The face has not been found : add it
          if i==nbTotFace:
            tabHshFace.append(hashVal)
            tabFaceIdx.append(finalIdxTab)
            nbTotFace += 1
            nbKeptFace += 1
            tabKeptFace[faceno] = True
          else:
            tabKeptFace[faceno] = False
        # End for faceno

        # Rebuild the group data
        newStripCount = [0] * (nbKeptFace+1)

        # First : Count the number of vertex of kept faces : Useless in Python
        curGrp_vertIdx = [ ]  # new int[l];
        #curGrp_tvertIdx = [ ] # new int[l];
        curGrp_matIdx = [] # array.array('L')   # new int[nbKeptFace];
        
        # Copy the vertex indexes of kept faces
        prev_nfn = curGrp.getNbFace()
        nfn = 0
        for faceno in range(0, curGrp.getNbFace()):
          if tabKeptFace[faceno]:
            fao = curGrp.matIdx[faceno]
            
            nbv = len(tabFaceIdx[idxFirstFace + nfn])

            # System.arraycopy(tabFaceIdx[idxFirstFace + nfn], 0, curGrp_vertIdx, nnfn, nbv)
            curGrp_vertIdx += tabFaceIdx[idxFirstFace + nfn]

            # System.arraycopy(tabTVertIdx, 0, curGrp_tvertIdx, nnfn, nbv)
            startIdx = curGrp.stripCount[faceno]
            lastIdx = curGrp.stripCount[faceno+1]
            curGrp_matIdx.append(fao)
            # Remap texture indexes
            if fao.fAttr & C_FACE_TEXT:
              for i,vti in enumerate(fao.tvertIdx):
                fao.tvertIdx[i] = mapTVert[vti]

            nfn += 1
            newStripCount[nfn] = newStripCount[nfn - 1] + nbv


        curGrp.stripCount = newStripCount
        curGrp.vertIdx = curGrp_vertIdx
        curGrp.matIdx = curGrp_matIdx
        self.groups.append(curGrp)
        curGrp.linkCoordList(None)
        logging.info("Group:%s merged with %d faces on %d", curGrp.getName(), nfn, prev_nfn)


    # Finalisation : Convert Lists 
    self.coordList = tmpCoordList
    self.texList = tmpTexList

    # Link Groups
    for gg in self.groups:
      gg.linkCoordList(self)

    # Fusion of material List
    for curGeom in inLst:
      nbmat = len(curGeom.getMaterialList())
      mapMat = [0] * nbmat
      for i,mn in enumerate(curGeom.getMaterialList()):
        mapMat[i] = self.addMaterial(mn)

      # Change material indexes in any groups
      for gg in curGeom.groups:
        for faceno in range(0, gg.getNbFace()):
          gg.setMatIdx(faceno, mapMat[gg.getMatIdx(faceno)])



  def addGroup(self, ngrp):
    ''' Add a group to the current WaveGeom. The group may belong to different WaveGeom

    Parameters
    ----------
    ngrp : GeomGroup
      Group to add
    '''

    # Create an empty new Group in the current WaveGeom
    internGrp = GeomGroup()
    internGrp.setName(ngrp.getName())
    self.groups.append(internGrp)
    internGrp.linkCoordList(self)
    
    # Fusion the incomming group with the new internal empty group
    internGrp.fusion(ngrp)
    return internGrp




  def removeGroup(self, grp, cleaning=False):
    ''' Remove a group from the current WaveGeom '''
    ret = C_OK    
    gg = grp if isinstance(grp, GeomGroup) else self.getGroup(grp)

    try:
      self.groups.remove(gg)
      if cleaning and self.groups:
        self.optimizeGroups(cleaning=True)
      
    except ValueError:
      logging.info("Group:%s not found", gg.getName() if gg else 'Null group')
      ret = C_FAIL

    return ret
    

#    def compareVertexList(self, wg, accuracy, complete):
#        """ generated source for method compareVertexList """
#        wg3d = wg
#        d = 0.0
#        dmax = 0.0
#        i = 0
#        while i < self.getCoordListLength():
#            d = self.coordList[i].distanceLinf(wg3d.coordList[i])
#            if d > accuracy:
#                dmax = d
#                if not complete:
#                    return dmax
#            i += 1
#        return dmax
#
#    def compareNormalList(self, wg, accuracy, complete):
#        """ generated source for method compareNormalList """
#        wg3d = wg
#        d = 0.0
#        dmax = 0.0
#        dv = Vector3d()
#        i = 0
#        while i < self.getNormListLength():
#            dv.sub(self.normList[i], wg3d.normList[i])
#            d = dv.lengthSquared()
#            if d > accuracy:
#                dmax = d
#                if not complete:
#                    return dmax
#            i += 1
#        return dmax
#
  def copyData(self):
    ng = WaveGeom()
    ng.coordList = self.getCoordList()
    if self.normList:
      ng.normList = self.getNormList()
    return ng


  # This method refers GeomGroup methods and should be implemented elsewhere
  def createPlaneDef(self, planeName, orientation='XZY'):
    ''' Find the center of the plane and the two vectors that define the plane '''
    plane = self.getGroup(planeName)
    vxtab = plane.getFaceVertex(0)
    eu = Vector3d( vxtab[3].x - vxtab[0].x, vxtab[3].y - vxtab[0].y, vxtab[3].z - vxtab[0].z).normalize()
    ev = Vector3d( vxtab[1].x - vxtab[0].x, vxtab[1].y - vxtab[0].y, vxtab[1].z - vxtab[0].z).normalize()       
    center = Point3d(vxtab[3].x + vxtab[1].x, vxtab[3].y + vxtab[1].y, vxtab[3].z + vxtab[1].z).scale(0.5)
  
    return center, eu, ev

  def copyGroups(self, srcWg=None, srcGrpOrNameOrLst=None, centerOrRepOrPlane=None, eu=None, ev=None, destGrpNames=None):
    ''' Perform a copy of a set of groups.
     
    Parameters
    ----------
    srcGrpOrNameOrLst  : str or GeomGroup or a list of str or GeomGroup
      Groups or Groups name where unmapped faces are located. 
      All groups of the source WaveGeom are used if None.
       
    centerOrRepOrPlane : Point3d OR CoordSyst OR GeomGroup
      When this parameter is used, the vertex of each groups will be mirrored along the normal of the plane.
      When this parameter is a Point3d, it defines the center of the coordinate system. 
      In such case, the two next arguments eu, ev are mandatory  
      When this parameter is a CoordSyst, it defines the cutting coordinate system
      When this parameter is a GeomGroup, the cutting coordinate system is computed with the center
      of the first face and the eu, ev are deduced from this first face (supposed square)

    eu : Vector3d, optional
      First vector of the coordinate system

    ev : Vector3d, optional
      Second vector of the coordinate system

    destGrpNames : str or list of str
      Optional new groups' names
      if none original names are kept
   
    Returns
    -------
    int
       Result Code. 
       C_OK when no problem has occured
       C_FAIL when the mapping generates a "null" area
       C_ERROR when (at least) one group does to belong to the current WaveGeom
    '''
    if not srcWg:
      srcWg = self
    
    # Retrieve groups 
    ret, lstGrp =   srcWg.findGroupList(srcGrpOrNameOrLst)
    if ret==C_ERROR:
      return ret

    # Prepare new names
    if isinstance(destGrpNames, str):
      destGrpNames = [ destGrpNames, ]
    elif not destGrpNames:
      destGrpNames = [ g.getName() for g in lstGrp ]

    # Check if we have the same of number of target names
    if len(destGrpNames)!=len(lstGrp):
      return C_FAIL
      
    if srcWg==self: # Internal copy
      # Copy the groups with new data
      for name,g in zip(destGrpNames, lstGrp):
        ng = GeomGroup(src=g, duplicateData=True)
        ng.setName(name)
        # Add the new group to the geometry
        self.groups.append(ng)
        # Mirror it if required
        if centerOrRepOrPlane:
          ng.mirror(centerOrRepOrPlane, eu, ev, duplicateData=False)

    else:
      # Import of groups
      for name,g in zip(destGrpNames, lstGrp):
        ng = self.createGeomGroup(name)
        # Import the group into the geometry
        ng.fusion(g)
        # Mirror it if required
        if centerOrRepOrPlane:
          ng.mirror(centerOrRepOrPlane, eu, ev, duplicateData=False)

    return ret

  def mergeGroups(self, srcWg=None, srcGrpOrNameOrLst=None, centerOrRepOrPlane=None, eu=None, ev=None, \
                  destGrpName="default", deleteInternal=True, radius=0.0):
    ''' Merge a set of groups into a single one and optionaly mirror the result.
     
    Parameters
    ----------
    srcGrpOrNameOrLst  : str or GeomGroup or a list of str or GeomGroup
      Groups or Groups name where unmapped faces are located. 
      All groups of the source WaveGeom are used if None.
       
    centerOrRepOrPlane : Point3d OR CoordSyst OR GeomGroup
      When this parameter is used, the vertex of each groups will be mirrored along the normal of the plane.
      When this parameter is a Point3d, it defines the center of the coordinate system. 
      In such case, the two next arguments eu, ev are mandatory  
      When this parameter is a CoordSyst, it defines the cutting coordinate system
      When this parameter is a GeomGroup, the cutting coordinate system is computed with the center
      of the first face and the eu, ev are deduced from this first face (supposed square)

    eu : Vector3d, optional
      First vector of the coordinate system

    ev : Vector3d, optional
      Second vector of the coordinate system

    destGrpName : str
      Name of the (new) group
   
    deleteInternal : boolean, optional, default is True
      Delete original groups when self is the source of GeomGroups
    
    radius : float, optional, default 0.0
      Maximum distance of two vertex for data optimization
    
    Returns
    -------
    int
       Result Code. 
       C_OK when no problem has occured
       C_ERROR when (at least) one group does to belong to the current WaveGeom
    '''
    if not srcWg:
      isInternal = True
      srcWg = self
    else:
      isInternal = (self==srcWg)
    
    # Check if optim is required
    optimReq = False
    
    # Retrieve groups 
    ret, lstGrp = srcWg.findGroupList(srcGrpOrNameOrLst)
    if ret!=C_OK:
      return ret

    # Create or Retrieve the destination group
    ng = self.createGeomGroup(destGrpName)

    # Import of groups
    for g in lstGrp:
      ng.fusion(g)
      if deleteInternal and isInternal:
        self.removeGroup(g)
        optimReq = True

    if centerOrRepOrPlane:
      ng.mirror(centerOrRepOrPlane, eu, ev, duplicateData=True)

    # Optimize the result
    if optimReq:
      self.optimizeGroups(cleaning=True, radius=radius)

    return C_OK


  def fillHole(self, srcGrpOrName, srcMatName, destGrpName, destMatName, mergeGrp=True, nbLoop=2, alpha=0.0625, createCenter=True):
    ''' Fill a hole in the geometry with the MLS method.
    Hole sampling created with a "SPIDER NET" algo of mine.
    AS described by document http://www.inf.ufrgs.br/~oliveira/pubs_files/WangJ_OliveiraM_Hole_Filling.pdf
    Title : A Hole-Filling Strategy for Reconstruction of Smooth Surfaces in Range Images
    Written by JIANNING WANG &  MANUEL M. OLIVEIRA
    
    The hole is identified by a material and searched in the srcGrpName group.
    A new group named destGrpName is created using a destMaterialName.
    
    Parameters
    ----------
    srcGrpName  : str or GeomGroup
      Group or Group name where unmapped faces are located. Default group used if None.
    srcMatName  : str 
      Material name affected to the hole.
    destGrpName : str 
      Group name to be created.
    destMatName : str 
      Material name affected to the new group.
    mergeGrp    : boolean, optional, default is True 
      Indicate if the new group is to be merged with the initial group.
    nbLoop      : int, optional, default = 2
      Number of Edge loops to consider. Default should be 2. 
    alpha       : float, optional default 0.0625 
      Influence of distant point (less than one).
    createCenter: boolean, optional, default is True
      when true the center vertex of the spider mesh is created
      
    Returns
    -------
    int
       Result Code. C_OK when no problem has occured.
       C_MISSING_MAT : The source meterial for the hole has not been found

    '''
    res = C_OK
    i,j,k = 0,0,0
    lstmat = self.getMaterialList()
    try:
      matidx = lstmat.index(srcMatName)
    except ValueError:
      logging.warning("Material[%s] is missing", srcMatName )
      return C_MISSING_MAT

    # Get default group
    grp = srcGrpOrName if isinstance(srcGrpOrName, GeomGroup) else self.getGroup(self.getGroupName()) if not srcGrpOrName else self.getGroup(srcGrpOrName)

    # Get the first face with the given material
    holefaceno = grp.findFace(matidx)
    if holefaceno == -1:
      logging.warning("In Group[%s] - No face with Material [%s] is missing", grp.getName(), srcMatName )
      return C_MISSING_FACEMAT

    # Get the vertex that compose the "hole face"
    edgePt = grp.getFaceVertex(holefaceno)
    edgePtIdx = grp.getFaceVertIdx(holefaceno)
    nbEdgePt = len(edgePt)
    nbEdgePt_f = float(nbEdgePt)
    logging.info("Edge contains %d points", nbEdgePt)

    # Calculate 'nnLoop' loops Vicinity
    edgeLoopPtIdx =  copy.copy(edgePtIdx)

    # First Loop Vicinity
    grp.extendLoopVicinity(edgePtIdx, edgeLoopPtIdx)
    nbLoopPt = len(edgeLoopPtIdx)
    logging.info("Edge Loop 1 contains %d points", nbLoopPt)

    for i in range(1, nbLoop):
      tmpIdx = edgeLoopPtIdx[0:nbLoopPt]

      grp.extendLoopVicinity(tmpIdx, edgeLoopPtIdx)
      nbLoopPt = len(edgeLoopPtIdx)
      logging.info("Edge Loop %d contains %d points", (i + 1), nbLoopPt)


    # Compute projection Repere with SVD matrix decomposition
    repUVN = Repere(nbLoopPt, edgeLoopPtIdx, self.coordList)
    tabproj = repUVN.project(0, 0, nbLoopPt, edgeLoopPtIdx, self.coordList, None)

    # Determine G the isobarycenter and the average length of edges 
    isoG = Point3d()
    avgEdgeLength = 0.0
    # Limited to the first points that are the edge vertex
    for i,p in enumerate(tabproj[:nbEdgePt]):
      isoG.add(p)
      avgEdgeLength += p.dXY(tabproj[(i + 1) % nbEdgePt])

    isoG.scale(1.0 / nbEdgePt_f)
    isoG.z = 0.0
    avgEdgeLength /= nbEdgePt_f
    
    # Determine the maximum distance between edges and G
    maxLength2Edges = sys.float_info.min
    for p in tabproj[:nbEdgePt]:
      d = isoG.dXY(p)
      if d > maxLength2Edges:
        maxLength2Edges = d

    # Determine the number of segment on a pseudo-radius
    # Each pseudo-radius will contain nbSeg-1 new points
    nbSeg = (1 + int((maxLength2Edges / avgEdgeLength))) >> 1
    if nbSeg < 2:
      nbSeg = 2

    # Number of new created points. +1 for the center isoG
    nbNewPt = nbEdgePt * (nbSeg - 1) + 1
    sampPt = [None]*nbNewPt  # of Point3d
    v = Vector3d()
    sampPt[0] = isoG
    for i,p in enumerate(tabproj[:nbEdgePt]): #    for i in range(nbEdgePt): # Limited to the first points that are the edge vertex
      k = i * (nbSeg - 1) + 1
      for j in range(1, nbSeg):
        v.sub(isoG, p)
        v.scale(float(j) / float(nbSeg))
        sampPt[k] = Point3d(p)
        sampPt[k].z = 0.0
        sampPt[k].add(v)
        k += 1

    # Calculate Texture Coord of G and Texture Index of edge points
    uvmap = grp.matIdx[holefaceno].fAttr & C_FACE_TEXT # Check if the face is textured
    if uvmap:
      edgeSampTextIdx = grp.getFaceTVertIdx(holefaceno)
      tx,ty = 0.0, 0.0

      for vti in edgeSampTextIdx:
        tx += self.texList[vti].x
        ty += self.texList[vti].y

      texG = TexCoord2f( (tx / nbEdgePt_f), (ty / nbEdgePt_f) )

      # Extend texList
      # Allocate new texture index at the end of the current table of the geometry
      lastno = len(self.texList)
      edgeSampTextIdx += array.array('l', [ lastno+i-nbEdgePt for i in range(nbEdgePt, nbEdgePt + nbNewPt) ])

      vtex = TexCoord2f()
      ntexList = copy.copy(self.texList) # [ None ] * (self.getTexListLength() + nbNewPt) # of TexCoord2f

      # ntexList[self.getTexListLength() + 0] = texG 
      ntexList.append( texG )
      for i in range(nbEdgePt):
        k = len(self.texList) + i * (nbSeg - 1) + 1
        for j in range(1, nbSeg):
          vtex.sub(texG, self.texList[edgeSampTextIdx[i]])
          vtex.scale(float(j) / float(nbSeg))
          ntexList.append(TexCoord2f(self.texList[edgeSampTextIdx[i]]).add(vtex))
          ntexList[k]

      self.setTexList(ntexList)
    else:
      logging.warning("No UV Map for %s", grp.getName())

    # Create a raster with edge Vertex and Sampled Vertex
    edgeSamp = tabproj[0:nbEdgePt] + sampPt

    # Allocate new vertex index at the end of the current table of the geometry
    lastno = self.getCoordListLength()
    edgeSampIdx = edgePtIdx + array.array('l', [ idx+lastno for idx in range(0, nbNewPt) ])
    logging.info("Meshed Size=%d", len(edgeSamp))

    # Calculate Point Altitudes
    calcMLS(edgeSamp, nbEdgePt, len(edgeSamp), tabproj, alpha)

    # Save Result in a new GeomGroup
    ngrp = self.createGeomGroup(destGrpName)

    ncl = repUVN.reserveProject(nbEdgePt, self.getCoordListLength(), nbNewPt, edgeSamp)
    #System_arraycopy(self.getCoordList(), 0, ncl, 0, self.getCoordListLength())
    ncl[0:self.getCoordListLength()] = self.getCoordList()[0:self.getCoordListLength()]
    self.setCoordList(ncl)
    if destMatName:
      self.addMaterial(destMatName)
      ngrp.setMaterialName(self.curMatIdx)

    lstFacevIdx = []
    lstFacevtIdx = []

    normIdx = [ ]
    for i in range(nbEdgePt):
      isuiv = (i + 1) % nbEdgePt
      i1 = nbEdgePt + i * (nbSeg - 1) + 1
      i2 = nbEdgePt + isuiv * (nbSeg - 1) + 1

      # Create first Quad face
      coordIdx = [ edgeSampIdx[i], edgeSampIdx[isuiv], edgeSampIdx[i2], edgeSampIdx[i1] ]
      texIdx = [ edgeSampTextIdx[i], edgeSampTextIdx[isuiv], edgeSampTextIdx[i2], edgeSampTextIdx[i1] ] if uvmap else [ ]
      ngrp.addFace(coordIdx, texIdx, normIdx)
        
      # Create other Quad faces
      for j in range(1, nbSeg - 1):
        coordIdx = [ edgeSampIdx[i1 + j - 1], edgeSampIdx[i2 + j - 1], edgeSampIdx[i2 + j], edgeSampIdx[i1 + j] ]
        texIdx = [ edgeSampTextIdx[i1 + j - 1], edgeSampTextIdx[i2 + j - 1], edgeSampTextIdx[i2 + j], edgeSampTextIdx[i1 + j] ] if uvmap else [ ]
        ngrp.addFace(coordIdx, texIdx, normIdx)

      # Create last Triangular face
      if createCenter:
        coordIdx = [ edgeSampIdx[i1 + nbSeg - 2], edgeSampIdx[i2 + nbSeg - 2], edgeSampIdx[nbEdgePt] ]
        texIdx = [ edgeSampTextIdx[i1 + nbSeg - 2], edgeSampTextIdx[i2 + nbSeg - 2], edgeSampTextIdx[nbEdgePt] ] if uvmap else [ ]
        ngrp.addFace(coordIdx, texIdx, normIdx)
      else:
        lstFacevIdx.append(edgeSampIdx[i1 + nbSeg - 2])
        if uvmap:
          lstFacevtIdx.append(edgeSampTextIdx[i1 + nbSeg - 2])


    # Create a centrale face (if center triangles have not been inserted)
    if not createCenter:
      ngrp.addFace(lstFacevIdx, lstFacevtIdx, normIdx)
      

    # Merge New group with intial one and Remove the hole face
    if mergeGrp:
      grp.removeFace(holefaceno)
      grp.fusion(ngrp)
      self.groups.remove(ngrp)
    return res
  
  
  def unTriangularize(self, lstGrp=None, maxsin=FEPSILON, algo=0, surfaceThreshold=0.1):
    ''' Untriangularize the current geometry (inplace).
    Triangular faces are merged when:
    * They have the same material
    * They have a common edge
    * The sinus of their normals (angle) is smaller than 'maxsin'
    
    Parameters
    ----------
    lstGrp: list of GeomGroup or String, Optional, default = None
      List of group to 'un-triangularize'
      If none, all groups are treated
      else the set of groups are treated. 
    
    maxsin: float, Optional, default = FEPSILON
      Maximal value for the sinus of the angle of both
      normal to permit a merge
      
    algo: bitmask for algorithm selection, default = C_FACE_NONE
      Add C_FACE_SURF for relative surface filtering. 
      
      Add either C_FACE_ORDER_LENGTH, C_FACE_ORDER_ANGLE or C_FACE_ORDER_SURF for surface choice ordering
      The ordering is used to choose the merged triangle between the 3 neighbours of a destination triangle.
      C_FACE_ORDER_LENGTH: The triangle with the greastest common edge is merged
      C_FACE_ORDER_ANGLE: The triangle with the smallest angle is merged
      C_FACE_ORDER_SURF: The triangle with the greatest relative surface is merged
      
    surfaceThreshold: float, default=0.1
      Threshold used by the surface filtering to keep a triangle as a merging candidate.
      The candidat is kept is its surface will represent more than 'surfaceThreshold' of the
      merged quad surface.
      
    Return
    ------
    int : 
      >=0 : Number of faces in the result geometry
      <0 : Error or warning
    
    '''
    initNbFace = self.getNbFace()
    logging.info("Start with %d faces", initNbFace)
    
    ret = C_OK
    
    if lstGrp==None:
      lgrp = self.getGroups()
    else:
      lgrp = [ ]
      for gd in lstGrp:
        if isinstance(gd, str): # Input is a group Name
          g = self.getGroup(gd)
          if g:
            lgrp.append(g)
          else:
            logging.warning('Unknown group:%s', gd)
            ret = min(ret, C_UNKNOWN)
        elif isinstance(gd, GeomGroup):
          lgrp.append(gd)
        else:
          logging.warning('Unknown group identification:%s', str(gd))
          ret = min(ret, C_ERROR)
    
    for g in lgrp:
      nb = g.getNbFace()
      r = g.unTriangularize(maxsin=maxsin, algo=algo, surfaceThreshold=surfaceThreshold)
      if r<C_OK:
        logging.info("Untriangularization of [%s] : %d faces not changed", g.getName(), nb)
      else:
        logging.info("Untriangularization of [%s] : %d --> %d faces", g.getName(), nb, r)
    
    logging.info("End with %d faces", self.getNbFace())

    return self.getNbFace() if ret>=0 else ret
  

  
  def remapUVArea(self, srcGrpOrName, srcMatName, destMatName=None):
    ''' Remap (UV mapping) a set of faces, supposing edge vertex are correctly mapped.
     Used to fix a 3D model error without remapping the full object.
     
    Parameters
    ----------
    srcGrpName  : str or GeomGroup
      Group or Group name where unmapped faces are located. Default group used if None.
      
    srcMatName  : str 
      Material name affected to the unmapped faces.
    destMatName : str 
      Optional Material name for the newly mapped faces.
   
    Return
    ------
    int
       Result Code. C_OK when no problem has occured.
       C_MISSING_MAT : The source meterial has not been found
   '''
    ret = C_OK
    i,k = 0,0
    logging.info("Group[%s] mapping mat[%s]", srcGrpOrName, srcMatName)
    lTexList = len(self.texList)
    lstmat = self.getMaterialList()
    try:
      matidx = lstmat.index(srcMatName)
    except ValueError:
      logging.warning("Material[%s] is missing", srcMatName )
      return C_MISSING_MAT

    # Get default group
    grp = srcGrpOrName if isinstance(srcGrpOrName, GeomGroup) else self.getGroup(self.getGroupName()) if not srcGrpOrName else self.getGroup(srcGrpOrName)

    # Create a temporary group within the current WaveGeom
    tmpGrp = self.extractGeomGroup(grp, 'tmpReMapGrp', matidx)

    # Compute the list of edge vertex Edge(p0, p1, idx0, idx1)
    # Where points (p0,p1) are new and potentially textured
    edges = tmpGrp.findEdges()
    nbLoopPt = len(edges)
    logging.info("Edge contains %d points", nbLoopPt)
    
    # For each edge vertex, find textures attributes from non target material
    # We only need to do that for edge first vertex
    for e in edges:
      for faceno in range(0, len(grp.stripCount) - 1):
        startIdx = grp.stripCount[faceno]
        fao = grp.matIdx[faceno]
        if fao.fAttr & C_FACE_TEXT and \
           fao.fAttr & C_FACE_MATMASK != matidx:
          
          try:
            pos = grp.vertIdx[startIdx:grp.stripCount[faceno + 1]].index(e.idx0)
            e.p0.texture = self.texList[ fao.tvertIdx[pos] ]
            break
          except ValueError:
            pass

    tabEdgeVertex = [ e.p0 for e in edges ]
    edgeLoopPtIdx = [ e.idx0 for e in edges ]
        
    # Prepare the list of target vertex
    tabIntVertex = [ ] # List of internal faces' vertex
    tabFaceIdx   = [ ] # List of vertex indexes in the global tabEdgeVertex+tabIntVertex list
    for faceno in range(tmpGrp.getNbFace()):
      lstPt = tmpGrp.getFaceVertex(faceno)
      tabFaceIdx.append( [ ] )
      
      for i,p in enumerate(lstPt):
        if p in tabEdgeVertex:
          pos = tabEdgeVertex.index(p)
          tabFaceIdx[faceno].append(pos)
          
        elif p in tabIntVertex:
          pos = tabIntVertex.index(p)
          tabFaceIdx[faceno].append(pos + nbLoopPt)
          
        else:
          p.texture = TexCoord2f()
          tabFaceIdx[faceno].append(len(tabIntVertex) + nbLoopPt)
          tabIntVertex.append(p)
    
    # Number of vertex of the sample
    tabVertex = tabEdgeVertex + tabIntVertex
    nbSamp = len(tabVertex)
          
    # Compute projection Repere with SVD matrix decomposition
    repUVN = Repere(nbLoopPt, edgeLoopPtIdx, self.coordList)
    
    # Project on UV plane
    tabSamp = repUVN.project(0, 0, nbSamp, range(nbSamp), tabVertex, None)
    
    # Copy Texture attributes into the new projected Point3d
    for pproj,psrc in zip(tabSamp, tabVertex):
      pproj.texture = psrc.texture

    # Compute Texture x Coordinates for each target vertex
    sampEdge = tabSamp[:nbLoopPt] # Isolate UVN projected Edges vertex
    sampInt  = tabSamp[nbLoopPt:] # Isolate UVN projected target vertex
    for p in sampInt:
      # Find Closest Segment to p
      dmin0 = sys.float_info.max
      p0, p1 = None, None
      for i,psrc0 in enumerate(sampEdge[:-1]):
        for psrc1 in sampEdge[i+1:]:
          # Compute Projection of p on P0,psrc  line
          pp,k = get2DProjectedPoint(psrc0, psrc1, p)
          if k>=0.0 and k<=1.0:
            d = p.distance(pp)
            if d<dmin0:
              p0,p1 = psrc0,psrc1
              dmin0 = d
              ksol = k

      # Interpolate taking into account 'u', 'v' relative positions
      p.texture.x = p0.texture.x + ksol * (p1.texture.x - p0.texture.x)
      p.texture.y = p0.texture.y + ksol * (p1.texture.y - p0.texture.y)
      
      
    # Set new textures indexes on original faces
    if destMatName:
      curMatIdx = self.addMaterial(destMatName)

    for faceno in range(tmpGrp.getNbFace()):
      origFaceIdx = tmpGrp.origFaceLst[faceno]

      # Retrieve original face vertex 
      lstPt = grp.getFaceVertex(origFaceIdx)

      # Create the texture coordinate table for this face
      tabTxCoord = [ tabSamp[i].texture for i in tabFaceIdx[faceno] ]

      # Set the texture coord to the current face
      grp.setFaceTex(origFaceIdx, tabTxCoord)
      
      if destMatName:
        grp.setFaceMat(origFaceIdx, curMatIdx)
   
    # Remove Temporary group
    self.removeGroup(tmpGrp)
    
    logging.info("Group[%s]: %d texture coordinates added", srcGrpOrName, len(self.texList) - lTexList)
    
    return ret
  
  
  
  def _findMaterialList(self, srcMatNameOrLst):
    ret = C_OK
    
    lstmat = self.getMaterialList()
    lstMatIdx = []
    matidx = C_MISSING_MAT
    
    if not srcMatNameOrLst:
      # Map all Materials 
      lstMatIdx = None
    elif isinstance(srcMatNameOrLst, list):
      for srcMatName in srcMatNameOrLst:
        try:
          matidx = lstmat.index(srcMatName)
          lstMatIdx.append(matidx)
        except ValueError:
          # Ignore this material
          logging.info(f'Material[{srcMatName}] not found working on all faces of Group[{srcMatName}] : Ignored in a list of materials')
          ret = C_FAIL
          
    else:
      try:
        matidx = lstmat.index(srcMatNameOrLst)
        lstMatIdx.append(matidx)
      except ValueError:
        # Consider to remap all materials of the selected groups
        logging.info(f'Material[{srcMatNameOrLst}] not found: Working on all faces')
        
    return ret, lstMatIdx
  
  
  
  
  def findGroupList(self, srcGrpOrNameOrLst):
    ''' Retrieve groups from a list of names or group.
    
    Parameters:
    -----------
    srcGrpOrNameOrLst : str, GeomGroup or list of str or GeomGroup
      groups to find
      
    Return:
    -------
    ret, lsgGrp:
      ret is the status
        C_OK: All groups have been found
        C_FAIL: At least one group is missing. But the full input list has been checked
        C_ERROR: One group does not belong to the same WaveGeom
        
      lstGrp the list of found groups in the WaveGeom
    ''' 
    ret = C_OK
    lstGrp = []
    if not srcGrpOrNameOrLst: 
      # Add all groups
      lstGrp = self.getGroups()
    elif isinstance(srcGrpOrNameOrLst, list):
      for srcGrpOrName in srcGrpOrNameOrLst:
        grp = srcGrpOrName if isinstance(srcGrpOrName, GeomGroup) else self.getGroup(srcGrpOrName) if srcGrpOrName else None
        if grp:
          if self==grp.geom:
            lstGrp.append(grp)    
          else:
            # The group does not belong to the current WaveGeom ==> Forbidden
            logging.warn(f'Group[{srcGrpOrName}] is not in current WaveGeom [{self.getName()}]')
            return C_ERROR, None
          
        else: # Group not found is ignored
          logging.info(f'Group[{srcGrpOrName}] not found: Ignored')
          ret = C_FAIL
        
    else:
      grp = srcGrpOrNameOrLst if isinstance(srcGrpOrNameOrLst, GeomGroup) else self.getGroup(self.getGroupName()) if not srcGrpOrNameOrLst else self.getGroup(srcGrpOrNameOrLst)
      if grp:
        if self==grp.geom:
          lstGrp.append(grp)    
        else:
          # The group does not belong to the current WaveGeom ==> Forbidden
          logging.warn(f'Group[{srcGrpOrNameOrLst}] is not in current WaveGeom [{self.getName()}]')
          return C_ERROR, None
        
      else: # Group not found is ignored
        logging.info(f'Group[{srcGrpOrNameOrLst}] not found: Ignored')
        ret = C_FAIL

    return ret, lstGrp
  
  
  def _findGroupFaceList(self, srcGrpOrNameOrLst, srcMatNameOrLst):
    # Build the material list (as integer)
    ret, lstMatIdx = self._findMaterialList(srcMatNameOrLst)
    
    # Retrieve groups 
    r2, lstGrp =   self.findGroupList(srcGrpOrNameOrLst)
    if r2==C_ERROR:
      return r2, None
    else:
      ret = min(ret, r2)
    
    # Prepare the list of Interest tuple (group, Faces Indexes)
    lstGrpFaceLst = []
    for g in lstGrp:
      if not lstMatIdx:
        origFaceLst = [ i for i in range(g.getNbFace()) ]
      else:
        origFaceLst = []
        for matidx in lstMatIdx:
          origFaceLst += [ i for i,fao in enumerate(g.matIdx) if fao.fAttr & C_FACE_MATMASK == matidx ]
          
      lstGrpFaceLst.append( (g, origFaceLst) )
      
    return ret, lstGrpFaceLst
  
  
  def __scaleAdapt(self, txmin, txmax, tymin, tymax, lstGrpFaceLst):  
    # Rescale Texture Coordinates  in [0 .. 1]x[0 .. 1]
    # Compute an homogeneous scale
    ret = C_OK
    maxExtend = max(tymax-tymin, txmax-txmin)
    if math.fabs(maxExtend)>FEPSILON:
      nscale = 1.0/maxExtend
      
      for (grp, origFaceLst) in lstGrpFaceLst:
        for faceno in origFaceLst:
          for tx in  [ grp.texList[i] for i in grp.getFaceTVertIdx(faceno) ] :
            tx.x = (tx.x - txmin) * nscale
            tx.y = (tx.y - tymin) * nscale
    else:
      logging.warning("Group[%s]: final scaling impossible - Null mapped area")
      ret = C_FAIL

    return ret
  
  
  def cylindricalUVMap(self, srcGrpOrNameOrLst, centerOrRepOrPlane, eu=None, ev=None, srcMatNameOrLst=None, destMatName=None):
    ''' Performe a UV mapping with a cylindrical development.
     
    Parameters
    ----------
    srcGrpOrNameOrLst  : str or GeomGroup or a list of str or GeomGroup
      Groups or Groups name where unmapped faces are located. 
      All groups of the WaveGeom are used if None.
       
    centerOrRepOrPlane : Point3d OR CoordSyst OR GeomGroup
      When this parameter is a Point3d, it defines the center of the coordinate system. 
      In such case, the two next arguments eu, ev are mandatory  
      When this parameter is a CoordSyst, it defines the cutting coordinate system
      When this parameter is a GeomGroup, the cutting coordinate system is computed with the center
      of the first face and the eu, ev are deduced from this first face (supposed square)

    eu : Vector3d, optional
      First vector of the coordinate system

    ev : Vector3d, optional
      Second vector of the coordinate system

    srcMatNameOrLst  : str or list of str
      Optional Material name affected to the unmapped faces.
      if None all faces are considered
      
    destMatName : str 
      Optional Material name for the newly mapped faces.
   
    Returns
    -------
    int
       Result Code. 
       C_OK when no problem has occured
       C_FAIL when the mapping generates a "null" area
       C_ERROR when (at least) one group does to belong to the current WaveGeom
    '''
    # ret = C_OK
    logging.info("Group[%s] mapping mat[%s]", srcGrpOrNameOrLst, srcMatNameOrLst)
    lTexList = len(self.texList)
    
    # Build a list of tuples (group, [ face indexes ])
    ret, lstGrpFaceLst = self._findGroupFaceList(srcGrpOrNameOrLst, srcMatNameOrLst)
    if ret==C_ERROR:
      return ret
              
    # Compute projection Repere in the Cylindrical Frame
    rep = GeomGroup.getCoordSyst(centerOrRepOrPlane, eu, ev)

    # Convert All input group coordinates in center+(eu,ev,ew) system
    # Optim: Usually mapping all points
    tabSamp = rep.To(self.coordList)
        
    # Compute tabSamp in Cylindrical Coordinates
    for p in tabSamp:
      p.r = math.sqrt(p.x*p.x + p.y*p.y)
      p.theta = round(math.atan2(p.y, p.x), 6)        
           
    # Set new textures indexes on original faces
    if destMatName:
      curMatIdx = self.addMaterial(destMatName)
      
    # Texture Min/Max values
    txmin, tymin = sys.float_info.max, sys.float_info.max
    txmax, tymax = -txmin, -tymin
    math2PI = 2.0*math.pi

    # for each selected tuple (group, [face indexes]) 
    for (grp, origFaceLst) in lstGrpFaceLst:
      # For each face of the current group
      for faceno in origFaceLst:
        # Get vertex indexes of the face
        tabFaceIdx = grp.getFaceVertIdx(faceno)
  
        # Retrieve transformed face vertex 
        lstPt = [ tabSamp[i] for i in tabFaceIdx ] 
  
        # Search the first point of the face : the minimal theta but greater than -pi
        thetamin  = sys.float_info.max
        zmin      = sys.float_info.max
        firstPtNo = 0
        for i,p in enumerate(lstPt):
          if p.theta <= -math.pi:
            continue
          
          rt = round(p.theta, 6)
          if rt<=thetamin:
            if rt<thetamin:
              thetamin  = rt
              zmin      = p.z
              firstPtNo = i
            elif p.z<zmin:
              thetamin  = rt
              zmin      = p.z
              firstPtNo = i
            
        if firstPtNo>0:
          lstPt = lstPt[firstPtNo:] + lstPt[0:firstPtNo]
  
        # Consider face to be mapped
        pprev      = lstPt[0]
        prevtheta  = pprev.theta
        prevSign   = 1 if pprev.theta >= 0.0 else -1
        txx = pprev.r * prevtheta 
        txy = pprev.z
        tabTxCoord = [ TexCoord2f(txx, txy), ]
  
        if txx > txmax:
          txmax = txx
        elif txx < txmin:
          txmin = txx
  
        if txy > tymax:
          tymax = txy
        elif txy < tymin:
          tymin = txy
          
        for p in lstPt[1:]:
          ddtheta = math.fabs(p.theta - prevtheta)
          prevtheta = p.theta
          if math.fabs(ddtheta-math.pi)>FEPSILON and ddtheta>math.pi:
            prevtheta += math2PI if prevSign==1 else -math2PI
          
          txx = p.r * prevtheta 
          txy = p.z
  
          if txx > txmax:
            txmax = txx
          elif txx < txmin:
            txmin = txx
    
          if txy > tymax:
            tymax = txy
          elif txy < tymin:
            tymin = txy
          
          # Swap previous point and assign final texture  
          pprev = p
          prevSign = 1 if prevtheta >= 0.0 else -1
          tabTxCoord.append(TexCoord2f(txx, txy))
        # End for p
        
        # Reordinate the final textures table
        if firstPtNo>0:
          tabTxCoord = tabTxCoord[len(tabTxCoord)-firstPtNo:] + tabTxCoord[0:len(tabTxCoord)-firstPtNo]
        
        # Set the texture coord to the original face
        grp.setFaceTex(faceno, tabTxCoord)
        
        if destMatName:
          grp.setFaceMat(faceno, curMatIdx)
        # End for faces
        
    # Homogenous Rescale Texture Coordinates  in [0 .. 1]x[0 .. 1]
    ret = min(ret, self.__scaleAdapt(txmin, txmax, tymin, tymax, lstGrpFaceLst))
      
    logging.info("Group[%s]: [%d] texture coordinates added", srcGrpOrNameOrLst, len(self.texList) - lTexList)    
    return ret


  def planarUVMap(self, srcGrpOrNameOrLst, centerOrRepOrPlane, eu=None, ev=None, srcMatNameOrLst=None, destMatName=None):
    ''' Performe a planar UV mapping on a given plane.
     
    Parameters
    ----------
    srcGrpOrNameOrLst  : str or GeomGroup or a list of str or GeomGroup
      Groups or Groups name where unmapped faces are located. 
      All groups of the WaveGeom are used if None.
      
    centerOrRepOrPlane : Point3d OR CoordSyst OR GeomGroup
      When this parameter is a Point3d, it defines the center of the coordinate system. 
      In such case, the two next arguments eu, ev are mandatory  
      When this parameter is a CoordSyst, it defines the cutting coordinate system
      When this parameter is a GeomGroup, the cutting coordinate system is computed with the center
      of the first face and the eu, ev are deduced from this first face (supposed square)

    eu : Vector3d, optional
      First vector of the coordinate system

    ev : Vector3d, optional
      Second vector of the coordinate system

    srcMatNameOrLst  : str or list of str
      Optional Material name affected to the unmapped faces.
      if None all faces are considered
      
    destMatName : str 
      Optional Material name for the newly mapped faces.
   
    Returns
    -------
    int
       Result Code. 
       C_OK when no problem has occured
       C_FAIL when the mapping generates a "null" area
       C_ERROR when (at least) one group does to belong to the current WaveGeom
    '''
    #ret = C_OK
    logging.info("Group[%s] mapping mat[%s]", srcGrpOrNameOrLst, srcMatNameOrLst)
    lTexList = len(self.texList)
                   
    # Build a list of tuples (group, [ face indexes ])
    ret, lstGrpFaceLst = self._findGroupFaceList(srcGrpOrNameOrLst, srcMatNameOrLst)
    if ret==C_ERROR:
      return ret
              
    # Compute projection Repere in the Cylindrical Frame
    rep = GeomGroup.getCoordSyst(centerOrRepOrPlane, eu, ev)
      
    # Set new textures indexes on original faces
    if destMatName:
      curMatIdx = self.addMaterial(destMatName)

    # Convert All input group coordinates in center+(eu,ev,ew) system
    tabSamp = rep.To(self.coordList)
        
    # Texture Min/Max values
    txmin, tymin = sys.float_info.max, sys.float_info.max
    txmax, tymax = -txmin, -tymin

    # for each selected tuple (group, [face indexes]) 
    for (grp, origFaceLst) in lstGrpFaceLst:
      # for face to map
      for faceno in origFaceLst:
        tabFaceIdx = grp.getFaceVertIdx(faceno)
  
        # Retrieve transformed face vertex 
        lstPt = [ tabSamp[i] for i in tabFaceIdx ]
        tabTxCoord = [ ]
  
        for p in lstPt:
          txx = p.x
          txy = p.y
  
          if txx > txmax:
            txmax = txx
          if txx < txmin:
            txmin = txx
    
          if txy > tymax:
            tymax = txy
          if txy < tymin:
            tymin = txy
          
          tabTxCoord.append(TexCoord2f(txx, txy))
        # End for p
        
        # Set the texture coord to the original face
        grp.setFaceTex(faceno, tabTxCoord)
        
        if destMatName:
          grp.setFaceMat(faceno, curMatIdx)
        # End for faces
        
    # Homogenous Rescale Texture Coordinates  in [0 .. 1]x[0 .. 1]
    ret = min(ret, self.__scaleAdapt(txmin, txmax, tymin, tymax, lstGrpFaceLst))
   
    logging.info("Group[%s]: %d texture coordinates added", srcGrpOrNameOrLst, len(self.texList) - lTexList)    
    return ret


  def transformUVMap(self, srcGrpOrNameOrLst, srcMatNameOrLst=None, scaleX=1.0, scaleY=None, \
                     transX=0.0, transY=0.0, rotate=0.0, adaptScale=C_AXIS_NONE, destMatName=None):
    ''' Perform a set of geometrical transform on an UV map.
    
    Operation order is:
    1) Rescale
    2) Translate
    3) Rotate
    4) Optionaly adapt on X axis, Y axis or both homogeneously
     
    Parameters
    ----------
    srcGrpOrNameOrLst  : str or GeomGroup or a list of str or GeomGroup
      Groups or Groups name where unmapped faces are located. 
      All groups of the WaveGeom are used if None.
     
    srcMatNameOrLst  : str or list of str
      Optional Material name affected to the unmapped faces.
      if None all faces are considered

    destMatName : str 
      Optional Material name for the newly mapped faces.
      
    Returns
    -------
    int
       Result Code. C_OK when no problem has occured.
       C_FAIL : When the scale adapt generate a null scale
    '''
    # Extract Texture coordinate (uniq in table)
    logging.info("Group[%s] mat[%s]", srcGrpOrNameOrLst, srcMatNameOrLst)
    
    ret, lstMatIdx = self._findMaterialList(srcMatNameOrLst)

    # Retrieve groups 
    r2, lstGrp =   self.findGroupList(srcGrpOrNameOrLst)
    if r2==C_ERROR:
      return r2
    else:
      ret = min(ret, r2)
      
    # Prepare a set of unique texture indexes
    sTexIdx = set()
    nbFace = 0
    for grp in lstGrp:
      for fao in grp.matIdx:
        if not lstMatIdx or ( (fao.fAttr & C_FACE_TEXT) and ( (fao.fAttr & C_FACE_MATMASK) in lstMatIdx) ):
          sTexIdx |= set( fao.tvertIdx )
          nbFace+=1

    texTab = [ self.texList[i] for i in sTexIdx ]

    logging.warning("Group[%s] Modifying [%d] texture coords in [%d] faces", srcGrpOrNameOrLst, len(texTab), nbFace)

    # Transform
    txmin, txmax, tymin, tymax = TexCoord2f.transform(texTab, scaleX, scaleY, transX, transY, rotate) 

    # Final scaling to enter the [0..1]x[0..1] square 
    ret = min(ret, TexCoord2f.adaptScale(texTab, transX, transY, txmin, txmax, tymin, tymax, adaptScale))
    if ret==C_FAIL:
      logging.warning("Null Scale for Group[%s] mat[%s] : Consider translating", srcGrpOrNameOrLst, srcMatNameOrLst)

    # Optional Material change
    if destMatName:
      curMatIdx = self.addMaterial(destMatName)
      for grp in lstGrp:
        for faceno,fao in enumerate(grp.matIdx):
          if not lstMatIdx or ( (fao.fAttr & C_FACE_TEXT) and ( (fao.fAttr & C_FACE_MATMASK) in lstMatIdx) ):
            grp.setFaceMat(faceno, curMatIdx)

    return ret

# ==============================================================================
#  End Of WaveGeom
# ==============================================================================





# ------------------------------------------------------------------------------
def readGeom(fn, usemtl=False, imgdirpath=''):
  ''' Read a .OBJ (or .OBZ compressed) file and return a WaveGeom.
  
  Parameters
  ----------
  fn  : str
    Filename of the .OBJ (or.obz) file

  Returns
  -------
  WaveGeom 
    the read geometry (None in case of FileNotFoundError)
  '''
  gm = None

  try:
    # Read full body geometry
    rin = getOBJFile(fn)

    pfr = PoserFileParser(rin, OBJ_FNAT)
    gm = WaveGeom(st=pfr, filename=fn, usemtl=usemtl, imgdirpath=imgdirpath)

    rin.close()

  except FileNotFoundError as e:
    if WFBasic.PYPOS3D_TRACE: print(f'File({fn} - Read Error {e.args}')

  return gm
 


# ----------------------------------------------------------------------------
def PlaneCut(target, centerOrRepOrPlane, eu=None, ev=None, materialName='SectionMat', \
             slicing=False, radialLimit=0.0, radialScale=0.0): 
  ''' Cut target group along the normal vector of the input plan (or the third vector of the Coordinate System).
  Create a new WaveGeom with one group :
    default : the result geometry does not contain cut faces
  Hyp:
  - Cutting plane defined by a point and a set of non co-linear vectors
  - Does not modify the plane nor the input 'target'
  - Create the closing faces if materialName not null
  - By default remove the cut faces (slice=False), else just create the new edges and faces
 
  Perform a Radial Scale on the closing face, if radialScale>0.0
 
  Parameters
  ----------
  target : GeomGroup
    GeomGroup to cut

  centerOrRepOrPlane : Point3d OR CoordSyst OR GeomGroup
    When this parameter is a Point3d, it defines the center of the coordinate system. 
      In such case, the two next arguments eu, ev are mandatory  
    When this parameter is a CoordSyst, it defines the cutting coordinate system
    When this parameter is a GeomGroup, the cutting coordinate system is computed with the center
      of the first face and the eu, ev are deduced from this first face (supposed square)

  eu : Vector3d, optional
    First vector of the coordinate system

  ev : Vector3d, optional
    Second vector of the coordinate system

  materialName : str, optional, default='SectionMat'
    Name of the material of the closing face.
    if None, the closing face is not inserted in the result geometry

  slicing : bool, optional, default=False
    When slicing is True , the result geometry contains all geometries with 'sliced' faces along the plane
    defined by (center, eu, ev)
   

  radialLimit : float, optional, default 0.0
     if radialLimit is 0.0 : Cut along an infinite plan
     For any positive value - The cut faces shall be enclosed in the circle defined
                  by the 'center' and the "radialLimit'
  radialScale : float, optional, default 0.0
    For any positive value, the closing face is scaled with this value (central homothetie)

  Returns
  -------
  WaveGeom, CuttingData :
    a new WaveGeom with a single new GeomGroup
    the CuttingData object
  '''
  logging.info("Start for %s", target.getName())

  nwg = WaveGeom()
  nwg.lstMat = copy.copy(target.lstMat)
  
  nwg.texList = copy.copy(target.texList)
  hasFoundTexture = True

  # Compute the Cutting axis and the transformation matrix
  rep = GeomGroup.getCoordSyst(centerOrRepOrPlane, eu, ev)

  # Convert All input group coordinates in center+(eu,ev,ew) system
  nwg.coordList = rep.To(target.coordList)

  ngrp =  nwg.createGeomGroup(target.getName() + 'cut')

  # Create a new face list (defined by Vertex)
  nFaceList = [ ]
  
  # List of attributs and mat indexes to apply (or restore) to the faces
  nMatList = []
  
  closingFaceVx = [ ]
  # The Closing face has texture if all splited faces have texture
  closingFaceText = True 

  # In the cutting plan coord. syst, the cutting vector is Oz
  cuttingVect = Vector3d(0.0,0.0,1.0) 

  radialLimit2 = radialLimit*radialLimit

  # For each target face
  for faceno,fao in enumerate(target.matIdx):
    startidx = target.getFaceStartIdx(faceno)
    lastidx = target.getFaceLastIdx(faceno)
                        
    # if lastidx-startidx<3:
    #   if WFBasic.PYPOS3D_TRACE: print(f'  PlaneCut[{target.getName()}] ignoring face: {faceno}')
    #   continue
    
    # Retrieve the face attributs (Text,Norm, material) of the face to cut
    fattr = fao.fAttr
    hasTexture = (fattr & C_FACE_TEXT)!=0
    hasFoundTexture |= hasTexture
    
    # Intersect with plane

    # Compute the list of enhanced Vertex, without aligned ones
    # We have at least 3 points
    prevPt = Point3d(nwg.coordList[target.vertIdx[startidx]])
    if hasTexture:
      prevPt.texture = nwg.texList[fao.tvertIdx[0]]
    vxtab = [ prevPt, ]
    nextPt, e0, e1 = None, None, None

    for i in range(startidx+1, lastidx-1):
      if nextPt:
        np = nextPt
        e0 = e1
      else:
        np = Point3d(nwg.coordList[target.vertIdx[i]]) 
        if hasTexture:
          np.texture = nwg.texList[fao.tvertIdx[i-startidx]]
        e0 = Edge(prevPt, np)

      nextPt = Point3d(nwg.coordList[target.vertIdx[i+1]]) 
      if hasTexture:
        nextPt.texture = nwg.texList[fao.tvertIdx[i+1-startidx]]

      e1 = Edge(np, nextPt)
      if e0.isAligned(e1): # Elimintate np and grow e1 segment
        e1 = Edge(prevPt, nextPt)
      else:
        vxtab.append(np)

    # Add the last point
    vxtab.append(nextPt)
 

    # Prepare the list of face edges
    lstEdgeVx = [ (vxtab[i], vxtab[i+1]) for i in range(0, len(vxtab)-1) ] + [ (vxtab[-1], vxtab[0]), ]

    if len(vxtab)<3:
      if WFBasic.PYPOS3D_TRACE: print(f'  PlaneCut[{target.getName()}] ignoring cleaned face: {faceno}')
      
      # Determine if the face shall be kept
      v = FaceVisibility(lstEdgeVx, cuttingVect)
      if v>FEPSILON or \
         ((radialLimit2!=0.0) and (min( v[0].x*v[0].x+v[0].y*v[0].y for v in lstEdgeVx ) > radialLimit2)): 

        lstNewFaceVx = [ v[0] for v in lstEdgeVx ]
        nFaceList.append(lstNewFaceVx)
        nMatList.append(fattr)
      continue

    # Now the plan is the origin of the coordinate sytem, the Normal vector is enough to cut
    lstNewFaceVx, lstNewEdges, multiple = FaceCut(lstEdgeVx, cuttingVect, hasTexture, slicing, radialLimit2)
 
    # Add the face to the face list of the new geometry
    if lstNewFaceVx:
        
      if multiple: # In such case, lstNewFaceVx is a list of list of Vertex
        if WFBasic.PYPOS3D_TRACE: 
          print(f'  PlaneCut[{target.getName()}].Cutting[{faceno}]: {len(lstNewFaceVx)} faces')
        nFaceList += lstNewFaceVx
        nMatList  += [ fattr ] * len(lstNewFaceVx)
      else:
        if WFBasic.PYPOS3D_TRACE: print(f'  PlaneCut[{target.getName()}].Cutting[{faceno}]: {len(lstNewFaceVx)} vertex')
        nFaceList.append(lstNewFaceVx)
        nMatList.append(fattr)
        
    
      # Add the new Edges to the closing Face
      if lstNewEdges:
        closingFaceVx += [ Edge(e[0], e[1]) for e in lstNewEdges ]
        closingFaceText &= hasTexture

  
  # Finish the group's creation
  # Add each face to the group
  ngrp.addFacesByVertex(nFaceList, nMatList)
    
  # Add the closing face to the list of faces to keep
  if materialName:
    lstFacesIdx, nbFaces, cl = ngrp.addFaceByEdges(closingFaceVx, closingFaceText, materialName)
  else:
    lstFacesIdx, nbFaces, cl = None, 0, []
    # Create a local list of the cut points
    if radialScale>0.0:
      for edge in closingFaceVx:      
        IndexAdd(cl, edge[0])
        IndexAdd(cl, edge[1])

  if radialScale>0.0:
    for p in cl:
      p.x *= radialScale
      p.y *= radialScale

  nwg.coordList = rep.From(nwg.coordList)
  # Just because we've change the coordList pointer!
  for gg in nwg.groups:
    gg.linkCoordList(nwg)

  # 20210609: This 'hasTexture' is not relevant anymore
  cd = CuttingData(ngrp, None, rep, lstFacesIdx, nbFaces, hasFoundTexture)
  
  logging.info("End for %s: Top=[%s with %d faces]", target.getName(), ngrp.getName(), ngrp.getNbFace())

  return nwg, cd

# ----------------------------------------------------------------------------
def PlaneSplit(target, centerOrRepOrPlane, eu=None, ev=None, radialLimit=0.0, materialName='SectionMat'):
  ''' Split target group along the third vector of the input plan. 
  Create a new GeomGroup with the two cut groups.

  Hyp:
  - Cutting plane defined by a point and a set of non co-linear vectors
  - Does not modify the plane nor the input 'target'
  - Create the closing faces if materialName not null in both groups
 
  Parameters
  ----------
  target : GeomGroup
    GeomGroup to cut

  centerOrRepOrPlane : Point3d OR CoordSyst OR GeomGroup
    When this parameter is a Point3d, it defines the center of the coordinate system. 
      In such case, the two next arguments eu, ev are mandatory  
    When this parameter is a CoordSyst, it defines the cutting coordinate system
    When this parameter is a GeomGroup, the cutting coordinate system is computed with the center
      of the first face and the eu, ev are deduced from this first face (supposed square)

  eu : Vector3d, optional
    First vector of the coordinate system

  ev : Vector3d, optional
    Second vector of the coordinate system

  materialName : str, optional, default='SectionMat'
    Name of the material of the closing face.
    if None, the closing face is not inserted in the result geometry

  radialLimit : float, optional, default 0.0
     if radialLimit is 0.0 : Cut along an infinite plan
     For any positive value - The cut faces shall be enclosed in the circle defined
                  by the 'center' and the "radialLimit'

  Returns
  -------
  WaveGeom, CuttingData :
    a new WaveGeom with two new GeomGroup(s)
    the CuttingData object
  ''' 
  logging.info("Start for %s", target.getName())

  nwg = WaveGeom()
  nwg.lstMat = copy.copy(target.lstMat)
  nwg.texList = copy.copy(target.texList)
  hasFoundTexture = True

  # Compute the Cutting axis and the transformation matrix
  rep = GeomGroup.getCoordSyst(centerOrRepOrPlane, eu, ev)

  # Convert All input geometry coordinates in center+(eu,ev,ew) system
  nwg.coordList = rep.To(target.coordList)

  # Create a new face lists (defined by Vertex)
  nTopFaceList, nBotFaceList = [], []
    
  # List of mat indexes to apply (or restore) to the faces
  nTopMatList, nBotMatList = [], []
  
  closingFaceVx = [ ]
  # The Closing face has texture if all splited faces have texture
  closingFaceText = True 
  
  # In the cutting plan coord. syst, the cutting vector is Oz
  cuttingVect = Vector3d(0.0,0.0,1.0) 

  radialLimit2 = radialLimit*radialLimit

  # For each target face
  for faceno,fao in enumerate(target.matIdx):
    startidx = target.getFaceStartIdx(faceno)
    lastidx = target.getFaceLastIdx(faceno)
                        
    # if lastidx-startidx<3:
    #   if WFBasic.PYPOS3D_TRACE: print(f'  [{target.getName()}] ignoring face: {faceno}')
    #   continue
    
    # Retrieve the material and the attributs of the face to cut
    fattr = fao.fAttr
    hasTexture = (fattr & C_FACE_TEXT)!=0
    hasFoundTexture |= hasTexture
    
    # Intersect with plane

    # Compute the list of enhanced Vertex, without aligned ones
    # We have at least 3 points
    prevPt = Point3d(nwg.coordList[target.vertIdx[startidx]])
    if hasTexture:
      prevPt.texture = nwg.texList[fao.tvertIdx[0]]
    vxtab = [ prevPt, ]
    nextPt, e0, e1 = None, None, None

    for i in range(startidx+1, lastidx-1):
      if nextPt:
        np = nextPt
        e0 = e1
      else:
        np = Point3d(nwg.coordList[target.vertIdx[i]]) 
        if hasTexture:
          np.texture = nwg.texList[fao.tvertIdx[i-startidx]]
        e0 = Edge(prevPt, np)

      nextPt = Point3d(nwg.coordList[target.vertIdx[i+1]]) 
      if hasTexture:
        nextPt.texture = nwg.texList[fao.tvertIdx[i+1-startidx]]

      e1 = Edge(np, nextPt)
      if e0.isAligned(e1): # Elimintate np and grow e1 segment
        e1 = Edge(prevPt, nextPt)
      else:
        vxtab.append(np)

    # Add the last point
    vxtab.append(nextPt)
 

    # Prepare the list of face edges
    lstEdgeVx = [ (vxtab[i], vxtab[i+1]) for i in range(0, len(vxtab)-1) ] + [ (vxtab[-1], vxtab[0]), ]

    if len(vxtab)<3:
      if WFBasic.PYPOS3D_TRACE: print(f'  [{target.getName()}] ignoring cleaned face : {faceno}')
      
      lstNewFaceVx = [ v[0] for v in lstEdgeVx ]

      v = FaceVisibility(lstEdgeVx, cuttingVect)
      # Determine in which group the face shall be kept
      if (v>FEPSILON) or \
         ((radialLimit2!=0.0) and (min( v[0].x*v[0].x+v[0].y*v[0].y for v in lstEdgeVx ) > radialLimit2)):
        nTopFaceList.append(lstNewFaceVx)
        nTopMatList.append(fattr)
      else:
        nBotFaceList.append(lstNewFaceVx)
        nBotMatList.append(fattr)

      continue

    # Now the plan is the origin of the coordinate sytem, the Normal vector is enough to cut
    lstTopFacesVx, lstBotFacesVx, lstNewEdges = FaceSplit(lstEdgeVx, cuttingVect, hasTexture, radialLimit2)
 
    # Add the face(s) to the face list of the new geometry
    if lstTopFacesVx: # lstTopFacesVx is a list of list of Vertex
      nTopFaceList += lstTopFacesVx
      nTopMatList +=  [ fattr ] * len(lstTopFacesVx)
    
    if lstBotFacesVx: # lstTopFacesVx is a list of list of Vertex
      nBotFaceList += lstBotFacesVx
      nBotMatList += [ fattr ] * len(lstBotFacesVx)
    
    # Add the new Edges to the closing Face
    if lstNewEdges:
      closingFaceVx += [ Edge(e[0], e[1]) for e in lstNewEdges ]
      closingFaceText &= hasTexture

  # Finish the group's creation : Add each face to the group
  topGrp = nwg.createGeomGroup(target.getName() + 'cutTop')
  botGrp = nwg.createGeomGroup(target.getName() + 'cutBot')

  logging.info("Adding Top Faces in %s: [%s with %d faces]", target.getName(), topGrp.getName(), len(nTopFaceList))
  topGrp.addFacesByVertex(nTopFaceList, nTopMatList)

  logging.info("Adding Bottom Faces in %s: [%s with %d faces]", target.getName(), botGrp.getName(), len(nBotFaceList))
  botGrp.addFacesByVertex(nBotFaceList, nBotMatList)
    
  # Add the closing face to the list of faces to keep
  logging.info("Creating ClosingFace in %s:%d edges", topGrp.getName(), len(closingFaceVx))
  #Plot(closingFaceVx,None)
  
  if materialName:    
    lstFacesIdx, nbFaces, _ = topGrp.addFaceByEdges(closingFaceVx, closingFaceText, materialName, refNorm=Vector3d(cuttingVect).neg())
  else:
    lstFacesIdx, nbFaces  = None, 0

  nwg.coordList = rep.From(nwg.coordList)
  # Relink groups, just because we've change the coordList pointer!
  for gg in nwg.groups:
    gg.linkCoordList(nwg)

  cd = CuttingData(topGrp, botGrp, rep, lstFacesIdx, nbFaces, hasFoundTexture)

  logging.info("End for %s: Top=[%s with %d faces] Bottom=[%s with %d faces]", target.getName(), topGrp.getName(), topGrp.getNbFace(), botGrp.getName(), botGrp.getNbFace())

  return nwg, cd



  


# ----------------------------------------------------------------------------
# TODO: Output to rethink - Could return all the closing faces (we have them)
#
def PlaneSlice(target, centerOrRepOrPlane, eu=None, ev=None, cutFaceMatLst=None, radialLimit=0.0, radialScale=0.0, minLength=0.0): 
  ''' Compute the slice of a given GeomGroup.
  Hyp:
  - Cutting plane defined by a point and a set of non co-linear vectors
  - Does not modify the plane
 
  Parameters
  ----------
  target : GeomGroup
    GeomGroup to cut

  centerOrRepOrPlane : Point3d OR CoordSyst OR GeomGroup
    When this parameter is a Point3d, it defines the center of the coordinate system. 
      In such case, the two next arguments eu, ev are mandatory  
    When this parameter is a CoordSyst, it defines the cutting coordinate system
    When this parameter is a GeomGroup, the cutting coordinate system is computed with the center
      of the first face and the eu, ev are deduced from this first face (supposed square)

  eu : Vector3d, optional
    First vector of the coordinate system

  ev : Vector3d, optional
    Second vector of the coordinate system

  cutFaceMatLst : list, optional, default=None, out
    When not null, this list is filled with the list of the material indexes of cut faces

  radialLimit : float, optional, default 0.0
     if radialLimit is 0.0 : Cut along an infinite plan
     For any positive value - The cut faces shall be enclosed in the circle defined
                  by the 'center' and the "radialLimit'

  radialScale : float, optional, default 0.0
    For any positive value, the closing face is scaled with this value (central homothetie)

  minLength : float, optional, default 0.0
    When not null, created egdes shall be longuer than minLength

  Returns
  -------
  list of Edge()
    With list of edges that represents the first closing face of the cut.
    Edges are containing new Point3d (carrying texture if any)
  ''' 
  logging.info("Start for %s", target.getName())

  keepMaterial = (cutFaceMatLst!=None)

  texList = copy.copy(target.texList)

  # Compute the Cutting axis and the transformation matrix
  rep = GeomGroup.getCoordSyst(centerOrRepOrPlane, eu, ev)

  # Convert All input group coordinates in center+(eu,ev,ew) system
  coordList = rep.To(target.coordList)

  closingFaceVx = [ ]

  # In the cutting plan coord. syst, the cutting vector is Oz
  cuttingVect = Vector3d(0.0,0.0,1.0) 
  
  radialLimit2 = radialLimit*radialLimit

  # For each target face
  for faceno,fao in enumerate(target.matIdx):
    startidx = target.getFaceStartIdx(faceno)
    lastidx = target.getFaceLastIdx(faceno)

    fattr = fao.fAttr
    hasTexture = (fattr & C_FACE_TEXT)!=0
    
    # Compute the list of enhanced Vertex, without aligned ones
    # We have at least 3 points
    prevPt = Point3d(coordList[target.vertIdx[startidx]])
    if hasTexture:
      prevPt.texture = texList[fao.tvertIdx[0]]
    vxtab = [ prevPt, ]
    nextPt, e0, e1 = None, None, None

    for i in range(startidx+1, lastidx-1):
      if nextPt:
        np = nextPt
        e0 = e1
      else:
        np = Point3d(coordList[target.vertIdx[i]]) 
        if hasTexture:
          np.texture = texList[fao.tvertIdx[i-startidx]]
        e0 = Edge(prevPt, np)

      nextPt = Point3d(coordList[target.vertIdx[i+1]]) 
      if hasTexture:
        nextPt.texture = texList[fao.tvertIdx[i+1-startidx]]

      e1 = Edge(np, nextPt)
      if e0.isAligned(e1): # Elimintate np and grow e1 segment
        e1 = Edge(prevPt, nextPt)
      else:
        vxtab.append(np)

    # Add the last point
    vxtab.append(nextPt)
 
    if len(vxtab)<3:
      if WFBasic.PYPOS3D_TRACE: print(f'  PlaneSlice[{target.getName()}] ignoring cleaned face: {faceno}')
      continue

    
    # Prepare the list of face edges
    lstEdgeVx = [ (vxtab[i], vxtab[i+1]) for i in range(0, len(vxtab)-1) ] + [ (vxtab[-1], vxtab[0]), ]

    # Now the plan is at the origin - The Normal is enough to cut
    _, lstNewEdges, _ = FaceCut(lstEdgeVx, cuttingVect, hasTexture, True, radialLimit2)
 
    # Add the new Edges to the closing Face
    if lstNewEdges:
      closingFaceVx += [ Edge(e[0], e[1]) for e in lstNewEdges ]
      if keepMaterial:
        cutFaceMatLst.append(fattr & C_FACE_MATMASK)
      
  
  # Compute the closing face(s) and keep the first one
  lstEdgesList, loccl, _  = CreateLoop(closingFaceVx)
  lstEdges = lstEdgesList[0] if lstEdgesList else [ ]

  # Scale if required 
  if radialScale>0.0:
    for p in loccl:
      p.x *= radialScale
      p.y *= radialScale
    
  # Eliminate too short edges, if required
  if minLength>0.0:
    
    for i,e in enumerate(lstEdges):
      if e.norme()<minLength:
        # Remove this edge  
        # Compute the 'mid' point with a bspline cubic algo
        pmid = Point3d(e.p0).add(e.p1).scale(0.5)
        loccl.append(pmid)
        
        # Compute potential texture coordinate
        if hasTexture:
          pmid.texture = TexCoord2f(TexCoord2f(e.p0.texture).add(e.p1.texture).scale(0.5))
        
        l = len(lstEdges)
        # Change points in previous and next edge
        lstEdges[i-1] = Edge(lstEdges[i-1].p0, pmid)
        lstEdges[(i+1)%l] = Edge(pmid, lstEdges[(i+1)%l].p1)
      
        del lstEdges[i]
      
  # Return to initial coordinate system
  rep.inFrom(loccl)
    
  logging.info("End for %s: List of Edges=[%d edges]", target.getName(), len(lstEdges))

  return lstEdges


#
# Compute the vertex indexes (and TexVert) into final coord List indexes
# Change the coordinate system to the 'image' one
# Return a list of loops defined by indexes in the final coord list
#
def __prepareForMeshing(coordList, Loops, botFaceNorm):
  LoopsIdx = [ ]
    
  for loop in Loops:
    loopIdx = [ ]
    
    for noedge, ed in enumerate(loop):
      idx0 = IndexAdd(coordList, Point3d(ed.p0))
      idx1 = IndexAdd(coordList, Point3d(ed.p1))
      loopIdx.append(idx0)
      loop[noedge] = Edge(ed.p0, ed.p1, idx0, idx1, ed.hasTexture)
  
    LoopsIdx.append(loopIdx)
  
  # Check Rotation orders to be aligned with the bottom face normal
  for loop in Loops[1:]:
    FaceNormalOrder(loop, botFaceNorm)

  return LoopsIdx



# -----------------------------------------------------------------------------
# TODO: Rework output (Cutting Data)
# TODO: Add a fillHole to the top part
def RadialScaleRemesh(target, centerOrRepOrPlane, eu=None, ev=None, dh=0.0, ds=0.0, repOrtopPlane=None, \
                      nbSlice=5, radialLimit=0.0, minLength=0.0, tabScale=None, reScale=False, \
                      reMesh=False, cutTop=False, cutBottom=True, \
                      fillHole=True, filledHoleMat='Extremity', \
                      alpha=0.0625):
  ''' RadialScaleRemesh is an high level function to rework a part of a geometry while preserving the extremities.
  - Cut target into 3 groups according to the first coord syst (centerOrRepPlane) 
    and the second coord syst defined eicher by a coord sys or a plane or a distance 
    from the first coord system along Oz axis.
  - Optionaly Remesh the central part
  - Optionaly perform a hole filling on the bottom face
  - Optionaly rescale the central part (quadric or spline defined by a tab of scales)
  
  Parameters
  ----------
  target : GeomGroup
    GeomGroup to rework

  centerOrRepOrPlane : Point3d OR CoordSyst OR GeomGroup
    When this parameter is a Point3d, it defines the center of the coordinate system. 
      In such case, the two next arguments eu, ev are mandatory  
    When this parameter is a CoordSyst, it defines the cutting coordinate system
    When this parameter is a GeomGroup, the cutting coordinate system is computed with the center
      of the first face and the eu, ev are deduced from this first face (supposed square)

  eu : Vector3d, optional
    First vector of the coordinate system

  ev : Vector3d, optional
    Second vector of the coordinate system
 
  dh : float, optional, default 0.0
    Distance between the bottom plane and to top plane along the normal vector of the bottom plane.
    When dh=0.0, repOrTopPlane arg shall be given

  ds : float, optional, default 0.0
    Scaling agrument. Distance between the bottom plane and the bottom of the parabol for scaling options.
    Refer to GeomGroup.RadialScale for detailed explanations

  repOrtopPlane : CoordSyst OR GeomGroup
    When this parameter is a CoordSyst, it defines the top cutting coordinate system
    When this parameter is a GeomGroup, the cutting coordinate system is computed with the center
      of the first face and the eu, ev are deduced from this first face (supposed square)

  nbSlice : int, optional, default 5
    Remesh argument. Number of slices of the remeshed central zone

  radialLimit : float, optional, default 0.0
     if radialLimit is 0.0 : Cut along an infinite plan
     For any positive value - The cut faces shall be enclosed in the circle defined
                  by the 'center' and the "radialLimit'

  minLength : float, optional, default 0.0
    When not null, created egdes shall be longuer than minLength


  tabScale : list of float, optional, default None
    Scaling argument.
    if tabScale not null, it must contain nbSlice+1 float. a Null float value means no radial scaling
      tabScale[0] is at bottom
      tabScale[nbSlice] is at top
    Refer to CoordSyst.RadialSplineScaling for details

   reScale : bool, optional, default False
     Ask for a scaling of the central part

   reMesh : bool, optional, default False
     Ask for a remesh of the central part

   cutTop : bool, optional, default False
     True : The result WaveGeom does not contain any group for the cut part
     False : The result WaveGeom contains a group for the cut part

   cutBottom : bool, optional, default True
     True : The result WaveGeom does not contain any group for the cut part
     False : The result WaveGeom contains a group for the cut part

   fillHole : bool, optional, default True
     Ask for a hole filling operation on the bottom face. Usually with cutBottom=True

   filledHoleMat : str, optional, default='Extremity'
     Material name to give to the faces created by the fill hole option
     or
     Material name to give to the closing face of the bottom
     or
     When set to None : No closing face is created

   alpha : float, optional, default = 0.0625
     fillHole coef (refer to WaveGeom.fillHole


  Returns
  -------
  WaveGeom, CuttingData :
    a new WaveGeom with 1 to 3 GeomGroups
    The cutting data where topGrp is cd.grp and the central part is cd.ogrp 

  '''
  logging.info("Start for %s", target.getName())

  # Validate inputs
  if reScale and dh==0.0 and not tabScale:
    logging.warning('  ({0:s})-dh and tabScale are null: No Scaling allowed'.format(target.getName()))

  if fillHole and not cutBottom:
    logging.warning('  ({0:s})-Hole filling requires to CutBottom=True: ERROR'.format(target.getName()))
    return None, C_ERROR

  # Compute the Cutting axis and the transformation matrix of the reference plan (the bottom Plan)
  repBottom = GeomGroup.getCoordSyst(centerOrRepOrPlane, eu, ev)
  center = repBottom.center

  # Determine top cutting plane
  # Create a coordinate system for the cut of the top faces
  if isinstance(repOrtopPlane, CoordSyst):
    repTop = repOrtopPlane
  else:
    topPlane = repOrtopPlane
    repTop = topPlane.calcCoordSyst() if topPlane else CoordSyst(Point3d(center).add(Vector3d(0.0, 0.0, dh).inLin33(repBottom.MT)), repBottom.eu, repBottom.ev)

  # Slice the objet in three groups (bottom group is tmpCd.ogrp)
  _, tmpCd = PlaneSplit(target, repBottom, materialName='bottomTmpFace', radialLimit=radialLimit)

  if tmpCd.nbFaces!=1:
    logging.warning('  ({0:s})-Bottom Extremity slice does not contain one face but:{1:d}'.format(target.getName(), tmpCd.nbFaces))
    return None, tmpCd

  # Slice along the top plane : topGrp is cd.grp and the central part is cd.ogrp 
  nwg, cd = PlaneSplit(tmpCd.grp, repTop, materialName='topTmpFace', radialLimit=radialLimit)

  if cd.nbFaces!=1:
    logging.warning('  ({0:s})-Top Extremity slice does not contain one face but:{1:d}'.format(target.getName(), cd.nbFaces))
    return None, cd

  topGrp = cd.grp

  # Add the bottom group to the final WaveGeom
  bottomGrp = nwg.addGroup(tmpCd.ogrp)

  # Create the list of Edges with new vertex and potential texture attributes
  bottomLoop = tmpCd.grp.getFaceLoop('bottomTmpFace')

  # Create the list of Edges with new vertex and potential texture attributes
  topLoop = topGrp.getFaceLoop('topTmpFace')
    
  # The working group
  target = cd.ogrp

  # Remesh if required
  if reMesh:
    # Create loop of edges for each slicing position (along Oz)
    Loops = [ bottomLoop, ] if bottomLoop  else [ ]
    Reps = [ repBottom, ] if bottomLoop  else [ ]
    
    faceMatLst = []
    c0cn = Point3d(repTop.center).sub(center)

    logging.info("ReMesh [%s]: %d loops", target.getName(), len(Loops))    
    
    # For each slice
    for islice in range(1, nbSlice):
      k = float(islice)/float(nbSlice)
      centers = Point3d(center).add(Vector3d(c0cn).scale(k))
      evk = Vector3d(repBottom.ev).scale(1.0-k).add(Vector3d(repTop.ev).scale(k)).normalize()
      euk = Vector3d(repBottom.eu).scale(1.0-k).add(Vector3d(repTop.eu).scale(k)).normalize()
      repk = CoordSyst(centers, euk, evk)
      Reps.append(repk)

      # Loops[islice] = Plane Slice 'only' 
      nLoop = PlaneSlice(target, centers, euk, evk, cutFaceMatLst=faceMatLst, \
                         radialLimit=radialLimit, minLength=minLength)
      Loops.append(nLoop)
    
    #if topLoop:
    Loops.append(topLoop)
    Reps.append(repTop)
    
    # Create a regular Mesh with the loops
    ngrp = nwg.createGeomGroup(target.getName() + '_remeshed')    
    ngrp.curMatIdx = faceMatLst[0] & C_FACE_MATMASK
  
    # Record Vertex and Texture in the WaveGeom (new Point3d(s)) - Compute Final indexes
    # Convert Edges' points into the repBottom coordinate system
    LoopsIdx = __prepareForMeshing(ngrp.coordList, Loops, Vector3d(repBottom.ew).neg())
  
    for noloop, loop in enumerate(Loops[:-1]):
      ngrp.createStrip(loop, Loops[noloop+1], Reps[noloop], Reps[noloop+1])

    logging.info("ReMesh-finish [%s]: %d loops", target.getName(), len(Loops))    

    # Perform the scaling, Only available with reMesh
    if reScale and tabScale:
      for noloop, loop in enumerate(Loops):
        Reps[noloop].RadialScalePoint([ nwg.coordList[idx] for idx in LoopsIdx[noloop] ], tabScale[noloop])
      # FIX: Avoid a double scaling in case of parameter mix
      reScale = False

    # Put back the top group (they belong the same WaveGeom)
    # So Vertex Indexes have not been changed
    if not cutTop:
      ngrp.fusion(topGrp)

    # Rebuild the bottom face if fillHole required
    if fillHole or filledHoleMat:
      # Rebuild the bottomLoop 
      vxtab = [ nwg.coordList[idx] for idx in LoopsIdx[0] ]
      
      hasTexture = min( [ e.hasTexture for e in Loops[0] ] )
      
      if hasTexture: # Texture Coord were kept in the original copy of the bottom loop
        for i,p in enumerate(vxtab):
          p.texture = Loops[0][i].p0.texture
      
      # Create this face by changing its order
      Loop0 = [ Edge(vxtab[i], vxtab[(i+1)%len(vxtab)]) for i in range(0, len(vxtab)) ] # + [ Edge(vxtab[0], vxtab[-1]), ]
      ngrp.addFaceByEdges(Loop0, hasTexture, 'bottomTmpFace')

    # Remove the old middle part
    nwg.removeGroup(target)

  else: # No meshing : Must retrieve the central part
    logging.info("Finish [%s]", target.getName())    

    ngrp = target
    if not cutTop:
      ngrp.fusion(topGrp)

  if not cutBottom:
    ngrp.fusion(bottomGrp)

  # Remove Useless groups
  nwg.removeGroup(topGrp)
  nwg.removeGroup(bottomGrp)

  # Remove the topTmpFace
  ngrp.removeFace(materialName='topTmpFace')

  # Do Quadratic Radial scaling, if not already done by the tabScale param
  # With dh<>0, tabScale should be null
  if reScale and dh>0.0 and not tabScale:
    R = repTop.calcXYRadius( [ e.p0 for e in topLoop ] )
    repBottom.RadialQuadraticScaling(nwg.coordList, R, dh, ds, repTop, radialLimit)
  elif reScale and dh>0.0 and tabScale:
    R = repTop.calcXYRadius( [ e.p0 for e in topLoop ] )
    repBottom.RadialSplineScaling(nwg.coordList, R, dh, ds, repTop, radialLimit, tabScale)
    
  # Do a hole filling on the fusioned face
  if fillHole:
    # Fusion (if needed) the Cutting face
    ngrp.FaceFusion(prevMatName='bottomTmpFace', newMatName='Hole')    
    nwg.fillHole(ngrp, 'Hole', 'embout', filledHoleMat, True, 2, alpha, createCenter=False)
  elif filledHoleMat:
    ngrp.FaceFusion(prevMatName='bottomTmpFace', newMatName=filledHoleMat)    

  # Optimze final WaveGeom and clean unused vertex
  nwg.optimizeGroups(cleaning=True)
 
  return nwg, cd





