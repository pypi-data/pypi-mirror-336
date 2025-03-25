# -*- coding: utf-8 -*-
# package: pypos3d.wftk
import sys, copy
import logging
import math
import array
import numpy as np
from scipy import spatial

from langutil import C_FAIL, C_ERROR , C_OK

from pypos3d.wftk import WFBasic
from pypos3d.wftk.WFBasic import COUNT, FEPSILON, C_FACE_NORM, \
  C_FACE_TEXT, TexCoord2f, CoordSyst, C_FACE_MATMASK, C_FACE_TEXTNORM, FEPSILON2, C_FACE_SURF, \
  C_FACE_ORDER_ANGLE, C_FACE_ORDER_SURF, C_FACE_NONE
from pypos3d.wftk.WFBasic import LowestIdxPos, CreateLoop, FaceNormalOrder
from pypos3d.wftk.WFBasic import Point3d, Vector3d, Edge, Regularity, IndexAdd, CreateTransform, MxProd
from pypos3d.wftk.PaveList2D import PaveList2D


class FaceAttr:
  ''' This class represent Face attributs.
  In a GeomGroup each face has its own FaceAttr to store:
  - fAttr (integer):
    - Material index (reached by C_FACE_MATMASK)
    - Flags : C_FACE_TEXT | C_FACE_NORM
  
  - tvertIdx : An array of 32bits integer to store texture indexes (if any else None)
  - normIdx : An array of 32bits integer to store normal indexes (if any else None)
  '''
  def __init__(self, fAttrOrSrc:'int or FaceAttr'=None, tvertIdx=None, normIdx=None):
    if isinstance(fAttrOrSrc, FaceAttr):
      self.fAttr = fAttrOrSrc.fAttr
      self.tvertIdx = copy.copy(fAttrOrSrc.tvertIdx) if fAttrOrSrc.tvertIdx else None
      self.normIdx = copy.copy(fAttrOrSrc.normIdx) if fAttrOrSrc.normIdx else None
    else:
      self.fAttr = fAttrOrSrc
      self.tvertIdx = tvertIdx if isinstance(tvertIdx, array.array) else (array.array('l', tvertIdx) if tvertIdx else None)
      self.normIdx = normIdx if isinstance(normIdx, array.array) else (array.array('l', normIdx) if normIdx else None)

  def __str__(self):
    return str(self.fAttr)

  def setMatIdx(self, idx):
    self.fAttr = (self.fAttr & C_FACE_TEXTNORM) + (idx & C_FACE_MATMASK)



class GeomGroup(object):
  ''' GeomGroup represents a Geometrical group of faces and lines (3D).  
  New implementation based on array.array on Long (32bits)
  '''

  def __init__(self, name='', src=None, inCoordList=None, duplicateData=False):
    ''' Create a GeomGroup.
    When using 'src', the result group is a copy of 'src' group, using the same tables 
    of Vertex, TexCoordinates, Normals and Materials.
    
    Parameters
    ----------
    name : str
      Name of the GeomGroup

    src : GeomGroup
      Source for the GeomGroup (copy constructor)

    inCoordList : list of Point3d
      List of 3D vertex to initialize the GeomGroup
      
    duplicateData : boolean, optional, default False
      When True, all Vertex, Normals and texture coordinates are duplicated.
    '''
    #  Pointer to the coordinate table of the whole object
    self.coordList = src.coordList if src else (inCoordList if inCoordList else [])
    self.texList   = src.texList   if src else [ ]
    self.normList  = src.normList  if src else [ ]

    # Pointer to the WaveGeom
    self.geom = src.geom if src else None

    # group name. Multiple group names are not managed as defined in OBJ format
    self._name = src._name if src else name

    # Contains the index of the first element of vertIdx that defines a face
    # Length > 1
    self.stripCount = copy.copy(src.stripCount) if src else array.array('l', [ 0, ])
    
    # Contains the index of the first element of vertIdx that defines a line
    # Null if no line OR Length > 1
    self.lineStripCount = copy.copy(src.lineStripCount) if src else array.array('l', [ 0, ])

    if duplicateData and src:
      nextVi = len(self.coordList)
      nextTvi = len(self.texList)
      nextNi = len(self.normList)
      
      vertIdxCvt  = [ -1 ] * nextVi
      tvertIdxCvt = [ -1 ] * nextTvi
      normIdxCvt  = [ -1 ] * nextNi
      
      # For each face create new vertex indexes
      for faceno, fao in enumerate(src.matIdx):
        for i in src.getFaceVertIdx(faceno):
          if vertIdxCvt[i]==-1:
            vertIdxCvt[i] = nextVi
            nextVi +=1
            self.coordList.append(Point3d(self.coordList[i]))
            
        if fao.fAttr & C_FACE_TEXT:
          for i in fao.tvertIdx:
            if tvertIdxCvt[i]==-1:
              tvertIdxCvt[i] = nextTvi
              nextTvi +=1
              self.texList.append(TexCoord2f(self.texList[i]))

        if fao.fAttr & C_FACE_NORM:
          for i in fao.normIdx:
            if normIdxCvt[i]==-1:
              normIdxCvt[i] = nextNi
              nextNi +=1
              self.normList.append(Vector3d(self.normList[i]))

      # For each line create new vertex indexes
      for faceno, fao in enumerate(src.matLineIdx):
        for i in src.vertLineIdx[ src.lineStripCount[faceno]:src.lineStripCount[faceno+1] ]:
          if vertIdxCvt[i]==-1:
            vertIdxCvt[i] = nextVi
            nextVi +=1
            self.coordList.append(Point3d(self.coordList[i]))
            
        if fao.fAttr & C_FACE_TEXT:
          for i in fao.tvertIdx:
            if tvertIdxCvt[i]==-1:
              tvertIdxCvt[i] = nextTvi
              nextTvi +=1
              self.texList.append(TexCoord2f(self.texList[i]))
            
            
      # Remap Indexes of Vertex that compose each face
      self.vertIdx = array.array('l', [ vertIdxCvt[vi] for vi in src.vertIdx ] )

      # Create the list of Face attributes with texture indexes
      self.matIdx = [ FaceAttr(fao.fAttr, tvertIdx = [  tvertIdxCvt[i] for i in fao.tvertIdx ] if fao.fAttr & C_FACE_TEXT else None,  \
                               normIdx = [  normIdxCvt[i] for i in fao.normIdx ] if fao.fAttr & C_FACE_NORM else None ) \
                      for fao in src.matIdx ]

      # Remap Indexes of Vertex that compose each line
      self.vertLineIdx =  array.array('l', [ vertIdxCvt[vi] for vi in src.vertLineIdx ] )

      # Create the list of Face attributes with texture indexes
      self.matLineIdx = [ FaceAttr(fao.fAttr, tvertIdx = [  tvertIdxCvt[i] for i in src.matLineIdx.tvertIdx ] if fao.fAttr & C_FACE_TEXT else None) \
                      for fao in src.matLineIdx ]
      
    else:
      # Declare Faces attributs (C_FACE_NONE, C_FACE_TEXT, C_FACE_NORM, C_FACE_TEXTNORM, C_FACE_MATMSASK)
      # As of now, each face may have independent textures or normals 
      self.matIdx = copy.deepcopy(src.matIdx) if src else [ ]
  
      # Indexes of Vertex that compose each face
      self.vertIdx =  copy.copy(src.vertIdx) if src else array.array('l')
  
      # Indexes of Vertex that compose each line
      self.vertLineIdx =  copy.copy(src.vertLineIdx) if src else array.array('l')
      
      # Declare Lines attributs (C_FACE_NONE, C_FACE_TEXT, C_FACE_MATMSASK)
      # As of now, each line may have independently textures
      self.matLineIdx = copy.deepcopy(src.matLineIdx) if src else [ ]


    self._bestCrit = src._bestCrit if src else 0.0
    self.curMatIdx = src.curMatIdx if src else 0
    self.lstMat = src.lstMat if src else None

  def __str__(self):
    return f'GeomGroup[{self._name}]: {self.getNbFace()} faces'


  def getNbFace(self):
    ''' Returns the number of faces '''
    return len(self.stripCount) - 1

  def getNbLine(self):
    ''' Returns the number of lines '''
    return len(self.lineStripCount) - 1

  def getName(self):  return self._name

  def setName(self, n):
    self._name = n

  def getFaceStartIdx(self, noface):
    return self.stripCount[noface]

  def getFaceLastIdx(self, noface):
    return self.stripCount[noface + 1]

  def getMatIdx(self, noface):
    return self.matIdx[noface].fAttr & C_FACE_MATMASK

  def setMatIdx(self, noface, idx):
    self.matIdx[noface].setMatIdx(idx)

  # public int[] getFaceVertIdx(int noface, int[] restab)
  def getFaceVertIdx(self, noface):
    ''' Return the list of index of the Vertex of the given face. '''
    return self.vertIdx[self.stripCount[noface]:self.stripCount[noface + 1]] 

  # public int[] getFaceTVertIdx(int noface)
  def getFaceTVertIdx(self, noface):
    ''' Return the list of index of the texture coordinates of the given face.
    Return None if the face has no texture
    '''
    return self.matIdx[noface].tvertIdx

  def getFaceNormIdx(self, noface):
    ''' Return the list of index of the normals (Vector3d) of the given face.
    Return None if the face has no normal
    '''
    return self.matIdx[noface].normIdx 


  def getFaceVertex(self, noface, copyPoint=False, restab=None):
    ''' Return the list of Vertex of given face.
    Parameters
    ----------
    noface : int
      Face number [0 .. NbFace[
    copyPoint : bool
      if true, new Point3d are created.
      By default, this method return a pointers to the existing Point3d (in CoordList)
    restab : list
      Use restab to populate the result, else create a new list

    Returns
    -------
    list of Point3d
    '''
    startIdx = self.getFaceStartIdx(noface)
    lastIdx = self.getFaceLastIdx(noface)
    
    if restab:
      restab[:] = [ Point3d(self.coordList[j]) for j in self.vertIdx[startIdx:lastIdx] ] if copyPoint else [ self.coordList[j] for j in self.vertIdx[startIdx:lastIdx] ]
      return restab

    return [ Point3d(self.coordList[j]) for j in self.vertIdx[startIdx:lastIdx] ] if copyPoint else [ self.coordList[j] for j in self.vertIdx[startIdx:lastIdx] ]


  def getFaceVertexBy(self, matName, raiseExcept=True):
    ''' Return the list of Vertex of faces with the given material name.
    When raiseExcept is True:
      Raise ValueError when the material does not exist or the list is empty
    Else return an empty list
    
    Parameters
    ----------
    matName : str
      Material Name
      
    raiseExcept : bool, optional, default True
      if true, raise a ValueError
      else may return a None list

    Returns
    -------
    list of Point3d
    '''
    try:
      matidx = self.lstMat.index(matName)
      lstFaceNo = [ fi for fi in range(0, self.getNbFace()) if (self.matIdx[fi].fAttr&C_FACE_MATMASK)==matidx ]    
      
      if lstFaceNo:
        return [ self.coordList[j] for j in set(i for faceno in lstFaceNo for i in self.vertIdx[self.stripCount[faceno]:self.stripCount[faceno+1]]) ]
      
    except ValueError:
      pass

    if raiseExcept:
      raise ValueError('No face for '+matName)      
    else:
      return None

  #
  #
  def getFaceLoop(self, faceDescr, invertNorm=False):
    ''' Returns an (eventually) textured set of Edges
    Point3d are copied from the coordList and muted with a .texture attr if the face
    is textured

    Parameters
    ----------
    faceDescr : int or str
      if faceDescr is a str, it is considered as a Material Name. The selected face, is the first 
      with this material
      if faceDescr is an int,it should be a valid faceno
    invertNorm : bool
      if true the face order is reverted
    
    Returns
    -------
    list of Edge
    '''
    faceno = self.findFace(self.geom.lstMat.index(faceDescr)) if isinstance(faceDescr, str) else int(faceDescr)

    # Create the list of edges with new vertex with potential textures 
    startidx = self.getFaceStartIdx(faceno)
    lastidx = self.getFaceLastIdx(faceno)
    
    # Use new points with previous face definition
    vxtab = [ Point3d(self.coordList[self.vertIdx[i]]) for i in range(startidx, lastidx) ]

    if invertNorm:
      vxtab.reverse()

    fao = self.matIdx[faceno]
    hasTexture = fao.fAttr & C_FACE_TEXT != 0 
    if hasTexture: # Mutate the Point3d, so that they contain the associated texture coordinates
      for i, p in enumerate(vxtab):
        p.texture = self.texList[fao.tvertIdx[i]]
  
    # Return the list of face edges
    return [ Edge(vxtab[i], vxtab[i+1], -1, -1, hasTexture) for i in range(0, len(vxtab)-1) ] + [ Edge(vxtab[-1], vxtab[0]), ]


  # REMOVING USELESS NOT WORKING METHOD
  # def findTVertIdx(self, ptIdx):
  #   ''' Find the first face that refers to <code>vertIdx</code> and return the associated texture index.

  def addFace(self, coordIdx, texIdx, normIdx):
    ''' Add a face defined by indexes of Vertex, Texture Coords and normals if any.
  
    Return the origin coordIdx for convenience
    '''
    if len(coordIdx)<3:
      logging.warning(f'Face {len(self.stripCount)} rejected')
      return coordIdx
    
    if not isinstance(coordIdx, array.array):
      coordIdx = array.array('l', coordIdx)

    if texIdx and not isinstance(texIdx, array.array):
      texIdx = array.array('l', texIdx)

    if normIdx and not isinstance(normIdx, array.array):
      normIdx = array.array('l', normIdx)
    
    self.vertIdx += coordIdx
    self.stripCount.append(len(self.vertIdx))
    fao = FaceAttr(self.curMatIdx | (C_FACE_TEXT if texIdx else 0) | (C_FACE_NORM if normIdx else 0), texIdx, normIdx)
    self.matIdx.append(fao)
        
    return coordIdx


  def addLine(self, coordIdx, texIdx): # List<Integer> coordIdx, List<Integer> texIdx)
    ''' Add a line defined by indexes of Vertex, Texture Coords and normals if any.
  
    Return the origin coordIdx for convenience
    '''   
    if not isinstance(coordIdx, array.array):
      coordIdx = array.array('l', coordIdx)

    if not isinstance(texIdx, array.array):
      texIdx = array.array('l', texIdx)

    self.vertLineIdx += coordIdx
    self.lineStripCount.append(len(self.vertLineIdx))
    lao = FaceAttr(self.curMatIdx | (C_FACE_TEXT if texIdx else 0))
    self.matLineIdx.append(lao)
    return coordIdx
    
  def addFaceByEdges(self, lstEdges, hasTexture, materialName, refNorm=None):
    ''' Create the closing face(s) and add it(them) to the list of faces of the group.
    This method uses the CreateLoop function based on a min/max tree search with 
    alpha-beta prune. 

    Parameters
    ----------
    lstEdges : list of Edge(s)
      List of Edges where faces will be search
    hasTexture : bool
      Indicates that the face has texture coordinates
    materialName : str
      Material to assign to the created face(s)
    refNorm : Vector3d
      if not null used to reorganize faces so that their normals are aligned with the reference one

    Returns
    -------
    list of face indexes, number of faces, list of Point3d
    '''
    wg = self.geom
    self.curMatIdx = wg.addMaterial(materialName)
    
    lstFacesIdx = [ ]
  
    FaceLst, coordList, *_ = CreateLoop([ e for e in lstEdges if e])
    logging.info('Loop %d faces created', len(FaceLst))
    # Warning: Face edges' order my be mixed
    for f in FaceLst:
      
      if refNorm and f: # Check face definition : Counter clock shall match refNorm
        FaceNormalOrder(f, refNorm)
      
      coordIdx = array.array('l', [ IndexAdd(wg.coordList, e.p0) for e in f ])
      lstFacesIdx += coordIdx
      texIdx = array.array('l', [ IndexAdd(wg.texList, e.p0.texture) for e in f ] if hasTexture else [ ] )
        
      self.addFace(coordIdx, texIdx, [ ])
  
    return lstFacesIdx, len(FaceLst), coordList


  def addFacesByVertexO2(self, nFaceList, nMatList):
    ''' Add a list of faces defined by a list of vertex.
    O(n2) algorithm
    nFaceList : array of array of Point3d
    nMatList : array of Long
    '''    
    for faceno, f in enumerate(nFaceList):
      coordIdx, texIdx  = [], [] # array.array('l'), array.array('l')
      
      # Protect from "None" faces with Slice Option
      if not f: continue
      
      for p in f:
        try:
          idx = self.coordList.index(p)
        except:
          idx = len(self.coordList)
          self.coordList.append(p)
          
        coordIdx.append(idx)
        
        if nMatList[faceno] & C_FACE_TEXT:
          try:
            idx = self.texList.index(p.texture)
          except:
            idx = len(self.texList)
            self.texList.append(p.texture)
            
          texIdx.append(idx)  
          
      # Take into account original Material of the face
      self.curMatIdx = nMatList[faceno] & C_FACE_MATMASK
      self.addFace(coordIdx, texIdx, [ ])



  
  def addFacesByVertex(self, nFaceList, nMatList, doLogMethod=False):
    ''' Add a list of faces defined by a list of vertex.
    Octree (scipy.spatial.KDTree) algorithm
    nFaceList : array of array of Point3d
    nMatList : array of Long
    '''    
    # List of new points
    tmpCoordList = [ ]
    nbMaxVerts = len(self.coordList)
    nbMaxTVerts = len(self.texList)
    
    if (nbMaxVerts<1000) and (nbMaxTVerts<1000):
      if doLogMethod:
        logging.info("Using O(n2) method: %d", nbMaxVerts)
      return self.addFacesByVertexO2(nFaceList, nMatList)
    
    if doLogMethod:
      logging.info("Init CoordList/TexList: %d/%d", nbMaxVerts, nbMaxTVerts)
 
    nbsrc = len(self.coordList)
    npTab = np.zeros( (nbsrc, 3) )
    for pNo, p in enumerate(self.coordList):
      npTab[pNo] = [ p.x, p.y, p.z ]
    
    # Create an KDTree with the 'known Vertex' in a "global" np.array
    tree = spatial.KDTree(npTab, leafsize=10 if nbsrc<10000 else 100)
    svect = np.zeros((1,3))
    
    # Create a PaveList with the 'known Texture coords' in a "global" np.array
    pl = PaveList2D(n=32, texList=self.texList)
    
    for faceno, f in enumerate(nFaceList):
      coordIdx, texIdx = [], [] # array.array('l'), array.array('l')
      
      # Protect from "None" faces with Slice Option
      if not f: continue
      
      for p in f:
        # Search in KDTtree
        svect[0] = [ p.x, p.y, p.z ]
        rest, resIdx = tree.query(svect)

        # if found (not too far) ==> Put it in a tmp table
        if rest[0]<FEPSILON:
          # Use an existing vertex
          idx = resIdx[0]
        else:
          # Add a new vertex to the local list of new Vertex
          try:
            idx = tmpCoordList.index(p)
          except:
            idx = len(tmpCoordList)
            tmpCoordList.append(p)

          # New Points are comming after the existing ones
          idx+=nbsrc          

        coordIdx.append(idx)
        
        if nMatList[faceno] & C_FACE_TEXT:
          idx = pl.IndexAdd(p.texture)
          texIdx.append(idx)  
          
      # Take into account original Material of the face
      self.curMatIdx = nMatList[faceno] & C_FACE_MATMASK
      self.addFace(coordIdx, texIdx, [ ])
    #End for faceno 

    # Update the Global CoordList
    self.coordList += tmpCoordList



  # public int fillDedupFace(int nbFace, int[] tabHshFace, int[][] tabFaceIdx)
  def fillDedupFace(self, nbFace, tabHshFace, tabFaceIdx):
    ''' Copy strip data to deduplication tables '''
    for faceno in range(0, len(self.stripCount) -1):
      startIdx = self.stripCount[faceno]
      lastIdx = self.stripCount[faceno+1]
      idxTab = self.vertIdx[startIdx:lastIdx]
      nbv = lastIdx - startIdx

      # Find lowest index
      lowestIdx = LowestIdxPos(idxTab)
      finalIdxTab = [ idxTab[(i + lowestIdx) % nbv] for i in range(0, nbv) ]
      tabHshFace.append( sum(finalIdxTab) )
      tabFaceIdx.append( finalIdxTab )
      nbFace+=1

    return nbFace

  def extendLoopVicinity(self, edgePtIdx, edgeLoopPtIdx):
    '''Extends edgeLoopPtIdx with vertex of faces that are using vertex of edgePtIdx tab.
     As of 23-May-2020 : edgeLoopPtIdx does not need to be initialized. It'll grow 
     @param edgePtIdx       Initial table of vertex
     @param edgeLoopPtIdx   Table to extends.
    '''

    # For each point of existing loop
    for vi in edgePtIdx:
      # Search for faces that contains the current vertex
      for fno in range(0, self.getNbFace()):
        staIdx = self.stripCount[fno]
        lstIdx = self.stripCount[fno+1]

        if vi in self.vertIdx[staIdx:lstIdx]:
          # Add all vertex of the face to the target Loop if the new vertex is not already in it
          for nvertidx in self.vertIdx[staIdx:lstIdx]:
            if not nvertidx in edgeLoopPtIdx:
              edgeLoopPtIdx.append(nvertidx)


#  public long[] buildVectors()
  def buildVectors(self, geomcond=None):
    vectTbl = [ ]

    for faceno in range(0, len(self.stripCount) - 1):
      startIdx = self.stripCount[faceno]
      lastIdx = self.stripCount[faceno + 1] - 1
      
      fao = self.matIdx[faceno]
      hasTexture = fao.fAttr & C_FACE_TEXT
      
      for i in range(startIdx, lastIdx):
        idx0 = self.vertIdx[i]
        idx1 = self.vertIdx[i + 1]
        p0 = Point3d(self.coordList[idx0])
        p1 = Point3d(self.coordList[idx1])

        if not geomcond or (geomcond(p0) and geomcond(p1)):
          if hasTexture:
            p0.texture = self.texList[fao.tvertIdx[i-startIdx]]
            p1.texture = self.texList[fao.tvertIdx[i+1-startIdx]]
          vectTbl.append(Edge(p0, p1, idx0, idx1))

      # To close the loop
      idx0 = self.vertIdx[lastIdx]
      idx1 = self.vertIdx[startIdx]
      p0 = Point3d(self.coordList[idx0])
      p1 = Point3d(self.coordList[idx1])
      if not geomcond or (geomcond(p0) and geomcond(p1)):
        if hasTexture:
          p0.texture = self.texList[fao.tvertIdx[lastIdx-startIdx]]
          p1.texture = self.texList[fao.tvertIdx[0]]
        vectTbl.append(Edge(p0, p1, idx0, idx1))

    # Sort the Vector table to keep only lonely vectors
    return sorted(vectTbl, key=Edge.hashCode)


  def findEdges(self, geomcond=None):
    ''' Find a set of edges (according geomcond on Point3d)
    Edge are containg a copy of each source point (with a .texture attribut if any)
    '''
    logging.info("Group[%s]: %d faces", self._name , self.getNbFace())
    vectTbl = self.buildVectors(geomcond=geomcond) # Edge[] 
    logging.info("Group[%s]: %d vectors", self._name, len(vectTbl))

    vectno = 0

    # Edge[] edgeVect
    edgeVect = [ ]

    lenin = len(vectTbl)
    while vectno < lenin:
      curVect = vectTbl[vectno]
      vectno+=1

      nbocc = 1
      while (vectno < lenin) and (curVect==vectTbl[vectno]):
        vectno+=1
        nbocc+=1

      if nbocc==1:
        edgeVect.append(curVect)

    logging.info("Group[" + self._name + "]: " + str(len(edgeVect)) + " edge vectors deduced")

    return edgeVect

  def findFace(self, matidx):
    ''' Return the first faceno using the given material (by index) '''
    for i,fao in enumerate(self.matIdx):
      if fao.fAttr & C_FACE_MATMASK == matidx:
        return i
       
    return -1

  def setBestCrit(self, crit):
    self._bestCrit = crit

  def setMaterialName(self, matIdx):
    self.curMatIdx = matIdx

  def setFaceMat(self, faceno, madIdx):
    ''' Set the face material indice to a face '''
    fao = self.matIdx[faceno]
    fao.fAttr = madIdx | (fao.fAttr & (~ C_FACE_MATMASK))
    
    
  def setFaceTex(self, faceno, lstTx):
    ''' Set texture coordinates of the 'faceno' face.
    
    Parameters
    ----------
    faceno : int
      Index of the face in the face list (0 based)
    lstTx  : list of TexCoord2f
      list of texture coordinates associated to each vertex of the face
      
    Return
    ------
    int
      C_OK : No error
      C_FAIL : The number of texture coordinates does not match the 
               number of vertex
    '''
    lstIdx = self.getFaceVertIdx(faceno)
    nbTx = len(lstTx)
    if len(lstIdx)!=nbTx:
      # Error, the number of texture coordinate shall be equal to the number of vertex of the face
      logging.warning(f"Face {faceno} table as a unmatching vertex/textures {len(lstIdx)}/{nbTx}")
      return C_FAIL
    
    # Allocate TexCoord in the texture coord list of the group
    startIdx = len(self.texList)
    self.texList += lstTx
    fao = self.matIdx[faceno]
    fao.tvertIdx = array.array('l', range(startIdx, startIdx+nbTx))
    fao.fAttr |= C_FACE_TEXT
  
    return C_OK
    

  def invertFaceOrder(self):
    ''' Invert all faces order (ie. revert 'auto' normals)
    
    Return
    ------
    self for convenience
    '''
    tmpVert = [] # array.array('l')

    for faceno in range( 0, self.getNbFace()):
      fvi = self.getFaceVertIdx(faceno)
      fvi.reverse()
      tmpVert += fvi
      
      fao = self.matIdx[faceno]
      if fao.fAttr & C_FACE_TEXT:
        fao.tvertIdx.reverse()
        
    self.vertIdx[:] = array.array('l', tmpVert)
      
    return self

    


                         
    
  # -----------------------------------------------------------------------------
  def sanityCheck(self):
    ''' Check the consistency of a group. '''
    res = C_OK
    name = self.getName() if self.getName() else "NoName"
    
    sizeVertexList = len(self.geom.coordList)
    sizeTexList = len(self.geom.texList)
    sizeNormList = len(self.geom.normList)
    
    # Verify Vertex indexes
    for vi in self.vertIdx:
      if (vi<0) or (vi>=sizeVertexList):
        print(f'Group[{name}] Bad Vertex Index: {vi}')
        res = C_ERROR
        
    # Check faces counts
    nbf3, nbf4, nbfo = 0,0,0
    for faceno in range(0,self.getNbFace()):
      #startIdx, endIdx = self.getFaceLastIdx(faceno), self.getFaceStartIdx(faceno)
      fao = self.matIdx[faceno]
      # Check Texture coordinates
      if fao.fAttr & C_FACE_TEXT:
        for vti in fao.tvertIdx: # [startIdx:endIdx]:
          if (vti<0) or (vti>=sizeTexList):
            print(f'Group[{name}].face[{faceno}] Bad Texture Index List: {vti}')
            res = C_ERROR

      if fao.fAttr & C_FACE_NORM:
        for vti in fao.normIdx: #[startIdx:endIdx]:
          if (vti<0) or (vti>=sizeNormList):
            print(f'Group[{name}].face[{faceno}] Bad Normal Index: {vti}')
            res = C_ERROR
      
      nbv = self.getFaceLastIdx(faceno) - self.getFaceStartIdx(faceno)
      if nbv==3: 
        nbf3+=1
      elif nbv==4:
        nbf4+=1
      else:
        nbfo+=1

    print(f'Group[{name}] has {nbf3} Triangles, {nbf4} Quad, {nbf4} others')
    
    return res
    
  # -----------------------------------------------------------------------------
  def calcXYRadius(self, lstVxIdx):
    ''' Compute the Maximum Radius on Oxy plan of a list of vertex indices fo this group. '''
    rmax = sys.float_info.min
  
    for p in [ self.coordList[i] for i in lstVxIdx ]:
      r = p.x*p.x + p.y*p.y
      if r>rmax:
        rmax = r
  
    return math.sqrt(rmax)
  
  # -----------------------------------------------------------------------------
  def removeFace(self, faceno=-1, materialName=None):
    ''' Remove a face from a group.
    Enhancement: a more pythonic way (instead the copy of the java code)
    
    Parameters
    ----------
    faceno : int
      Face to remove (if >0)

    materialName : str
      Name of the material. Remove the first face with this material

    Returns
    -------
    int
      C_OK : Success
      C_ERROR : faceno==-1 and materialName not found
    '''
    if faceno==-1:
      if materialName:
        try:
          matidx = self.lstMat.index(materialName)
          faceno = self.findFace(matidx)
          if faceno<0:
            return C_FAIL
        except ValueError:
          return C_FAIL
      else:
        return C_ERROR
      
    startidx = self.getFaceStartIdx(faceno)
    lastidx = self.getFaceLastIdx(faceno)
    delta = lastidx - startidx

    del self.matIdx[faceno]
    del self.vertIdx[startidx:lastidx]
      
    debsc = self.stripCount[:faceno] # if faceno>0 else [ ]
    finsc = array.array('l', [ sc-delta for sc in self.stripCount[faceno+1:] ])
    self.stripCount[:] = debsc + finsc
    
    return C_OK

  # -----------------------------------------------------------------------------
  def removeFaces(self, lstFaceNo=None, materialName=None):
    ''' Remove a set of faces given by their face numbers or a materialName. '''
    nbface = self.getNbFace()
    if not lstFaceNo:
      matidx = self.lstMat.index(materialName)
      lstFaceNo = [ fi for fi in range(0, nbface) if self.matIdx[fi].fAttr & C_FACE_MATMASK==matidx ]
      
    nstripcount = [] # array.array('l')
    nvertidx = [] # array.array('l')
    nmatIdx = [] # array.array('L')
      
    for fi in range(0,len(self.stripCount)-1):
      stidx = self.stripCount[fi]
      lastidx = self.stripCount[fi+1]
      
      if not fi in lstFaceNo:
        nstripcount.append(len(nvertidx))
        nmatIdx.append(self.matIdx[fi])
        nvertidx += self.vertIdx[stidx:lastidx]
            
    nstripcount.append(len(nvertidx))
    self.stripCount = array.array('l', nstripcount)
    self.matIdx = nmatIdx
    self.vertIdx = array.array('l', nvertidx)
  
  def extractFaces(self, destName=None, materialName=None, inGeom=True):
    ''' Extract from the current group, the faces that match the condition
    Create a new group
    if inGeom is False: Create a new geometry
    else add the new group to the geometry of the current group
    '''    
    wg = self.geom if inGeom else self.geom.copy()
    matidx, destIdx = -1,-1
    try:
      matidx = self.lstMat.index(materialName)
    except ValueError:
      logging.warning('Source Material[%s] not found', materialName)
      return None
    
    try:
      if destName:
        destIdx = self.lstMat.index(destName)
    except ValueError:
      logging.warning('Destination Material[%s] not found', destName)
      return None
      
    ngrp = wg.createGeomGroup(destName if destName else self.getName()+'_extracted_' + materialName)
    
    if inGeom:
      nStripCount = [0, ]
      nVertIdx = [ ]
      
      for faceno, fao in enumerate(self.matIdx):
        if fao.fAttr & C_FACE_MATMASK==matidx:
          nVertIdx += self.getFaceVertIdx(faceno)
          nStripCount.append(len(nVertIdx))
          nfao = FaceAttr(fao)
          if destName:
            nfao.setMatIdx(destIdx)
          ngrp.matIdx.append(nfao)
          
      ngrp.stripCount = array.array('l', nStripCount)
      ngrp.vertIdx = array.array('l', nVertIdx)
                
    else:
      print('extractFaces not inGeom : NOT IMPLEMENTED YET')
      return None
    
    # Remove extracted faces
    self.removeFaces(materialName=materialName)
    
    return ngrp
    
    
      
  
  def FaceFusion(self, prevMatName, newMatName):  
    ''' Fusion of the faces with prevMatName into a single face with newMatName.
    If the faces are not connex, it may generate several faces.
    Texture coordinates are lost
    '''
    #Ensure the new Material exists
    self.geom.addMaterial(newMatName)
    
    matidx = self.lstMat.index(prevMatName)
    lstFacesNo, lstFacesIdx = [ ], []
    for faceno,fao in enumerate(self.matIdx):
      #fao = self.matIdx[faceno]
      if fao.fAttr & C_FACE_MATMASK==matidx:
        lstFacesIdx.append(self.getFaceVertIdx(faceno))
        lstFacesNo.append(faceno) 
    
    if len(lstFacesNo)==1:
      # No Fusion required - Just change Mat name
      self.setMatIdx(lstFacesNo[0], self.lstMat.index(newMatName))
      return
    
    # Create a dictionnary of unoriented edges
    #   dict of [ idx0, idx1, List of nextEdgeIdx Ptr=[], used=False, code, count, tidx0, tidx1 ]
    edgeDict = { }
    bigFaceText = True

    for i,f in enumerate(lstFacesIdx):
      
      # Compute Best case for texture presence
      bigFaceText &= (self.matIdx[lstFacesNo[i]].fAttr & C_FACE_TEXT)!=0
      
      if bigFaceText:
        lt = self.getFaceTVertIdx(lstFacesNo[i])
        LstTegde = [ (lt[i], lt[i+1]) for i in range(0, len(lt)-1) ] + [ (lt[-1], lt[0]), ]
        
      # For Each Edge
      for edgeno, edge in enumerate([ (f[i], f[i+1]) for i in range(0, len(f)-1) ] + [ (f[-1], f[0]), ]):
        code = (min(edge) << 32) | max(edge)
        try:
          edgeDesc = edgeDict[code]
          edgeDesc[COUNT] += 1
        except KeyError:
          if bigFaceText:
            edgeDesc = [ edge[0], edge[1], [], False, code, 1, LstTegde[edgeno][0], LstTegde[edgeno][1] ]
          else:
            edgeDesc = [ edge[0], edge[1], [], False, code, 1 ]
            
          edgeDict[code] = edgeDesc
          
    bigFace = []
    
    # For Each Face
    for i,f in enumerate(lstFacesIdx):
      
      # For Each Edge
      for edge in [ (f[i], f[i+1]) for i in range(0, len(f)-1) ] + [ (f[-1], f[0]), ]:
        # if Edge is exterior (not shared) Add it to the new edge list
        code = (min(edge) << 32) | max(edge)
        edgeDesc = edgeDict[code]
        if edgeDesc[COUNT]==1:
          p0 = self.coordList[edge[0]]
          p1 = self.coordList[edge[1]]
          if bigFaceText: # Since bigFaceText is a best case, we add all or none texture coordinates
            p0.texture = self.texList[edgeDesc[6]]
            p1.texture = self.texList[edgeDesc[7]]
          bigFace.append( Edge(p0, p1) )
    
    self.addFaceByEdges(bigFace, bigFaceText, newMatName)
    # Remove old faces
    self.removeFaces(materialName=prevMatName)
  
  


  # -----------------------------------------------------------------------------
  def fusion(self, angrp):
    ''' Fusion 'angrp' GeomGroup into self group.
    Both groups may belong to different WaveGeom

    Parameters
    ----------
    angrp : GeomGroup
      Group to add.
    '''
    logging.info("Start [%s:%d faces, %d Vx, %d Tx] <- [%s:%d faces, %d Vx, %d Tx]", self.getName(), self.getNbFace(), \
                 len(self.coordList), len(self.texList), \
                 angrp.getName(), angrp.getNbFace(), len(angrp.coordList),len(angrp.texList))
    
    if self.geom!=angrp.geom:
      # They belong to different WaveGeom
      # the destination WaveGeom must be upgraded with missing Vertex, TVertex and Norms
      # All indexes must me remapped
      
      # Copy the added group
      ngrp = GeomGroup(src=angrp)
      
      nbInit = len(ngrp.coordList)      
      nbMaxVerts = len(self.coordList)      

      if nbMaxVerts<1000: # and (nbMaxTVerts<1000):        
        # Case of empty dest list (append few times)
        if nbMaxVerts==0: # Dest group is empty : Vertex Mapping are already copied and correct
          logging.info("Direct Copy of %d vertex", len(ngrp.coordList))
          self.geom.coordList[:] = ngrp.geom.getCoordList()

          #logging.info("Direct Copy of %d Texture coords", len(ngrp.texList))
          self.geom.texList[:] = ngrp.geom.getTexList()

          #logging.info("Direct Copy of %d normals", len(ngrp.normList))
          self.geom.normList[:] = ngrp.geom.getNormList()
        else:
          logging.info("Using O(n2) method: %d", nbMaxVerts)
          # Create an empty mapping tables
          mapVert  = [-2] * nbInit
          mapTVert = [-2] * len(ngrp.texList)
          mapNorm  = [-2] * len(ngrp.normList)
          
          for i,vi in enumerate(ngrp.vertIdx):
            nvi = mapVert[vi]
            if nvi<0:
              nvi = IndexAdd(self.coordList, Point3d(ngrp.coordList[vi]))
              mapVert[vi] = nvi
              
            ngrp.vertIdx[i] = nvi

          for fao in ngrp.matIdx:
            if fao.fAttr & C_FACE_TEXT:
              for i,vti in enumerate(fao.tvertIdx):
                nvti = mapTVert[vti]
                if nvti<0:
                  nvti = IndexAdd(self.texList, TexCoord2f(ngrp.texList[vti]))
                  mapTVert[vti] = nvti
            
                fao.tvertIdx[i] = nvti
    
            if fao.fAttr & C_FACE_NORM:
              for i,vti in enumerate(fao.normIdx):
                nvti = mapNorm[vti]
                if nvti<0:
                  nvti = IndexAdd(self.normList, Vector3d(ngrp.normList[vti]))
                  mapNorm[vti] = nvti
            
                fao.normIdx[i] = nvti
      
      # TODO: Proceed with Lines
      else: # Use an octree and a PaveList2D to merge coordList(s)
        logging.info("Using Octree method: %d", nbMaxVerts)
                  # Create an empty mapping tables
        mapVert  = [-2] * nbInit
        mapTVert = [-2] * len(ngrp.texList)

        npTab = np.empty( (nbMaxVerts, 3) )
        for pNo, p in enumerate(self.coordList):
          npTab[pNo] = [ p.x, p.y, p.z ]
    
        # Create an KDTree with the 'known Vertex' in a "global" np.array
        tree = spatial.KDTree(npTab, leafsize=10 if nbMaxVerts<10000 else 100)
        svect = np.zeros((1,3))
        
        for i,vi in enumerate(ngrp.vertIdx):
          nvi = mapVert[vi]
          if nvi<0:
            # Search in KDTtree
            p = Point3d(ngrp.coordList[vi])
            svect[0] = [ p.x, p.y, p.z ]
            rest, resIdx = tree.query(svect)

            # if found (not too far) ==> Put it in a tmp table
            if rest[0]<FEPSILON: # Use an existing vertex
              nvi = int(resIdx[0])
            else: # Add a new vertex to the dest list of Vertex
              nvi = len(self.coordList)
              self.coordList.append(p)

            mapVert[vi] = nvi
          
          ngrp.vertIdx[i] = nvi
          
        #Remap Texture
        pl = PaveList2D(n=32, texList=self.texList)
        for fao in ngrp.matIdx:
          if fao.fAttr & C_FACE_TEXT:
            for i,vti in enumerate(fao.tvertIdx):
              nvti = mapTVert[vti]
              if nvti<0:
                texture = TexCoord2f(ngrp.texList[vti]) # FIX bad source texture index
                nvti = pl.IndexAdd(texture)
                mapTVert[vti] = nvti
                
              fao.tvertIdx[i] = nvti
          
      # Map Material indexes
      mapMatIdx = [ IndexAdd(self.lstMat, matName) for matName in ngrp.lstMat ]
      for fao in ngrp.matIdx:
        fao.fAttr = (fao.fAttr & C_FACE_TEXTNORM) | mapMatIdx[fao.fAttr & C_FACE_MATMASK]

      # Keep the new group for fusion
      angrp = ngrp
    # else VertIdx Maps are identity
        
    # Copy the faces 
    vertpos = len(self.vertIdx)
        
    self.matIdx   += copy.deepcopy(angrp.matIdx)
    self.vertIdx  += angrp.vertIdx
    self.stripCount = self.stripCount[:-1] + array.array('l', [ sc+vertpos for sc in angrp.stripCount ])
    logging.info("End Result [%s:%d faces, %d Vx]", self.getName(), self.getNbFace(), len(self.coordList))


  def linkCoordList(self, wg):
    ''' Ensure that the GeomGroup points to WaveGeom common data. '''
    self.coordList = wg.coordList if wg else None
    self.texList = wg.texList if wg else None
    self.normList = wg.normList if wg else None
    self.lstMat = wg.lstMat if wg else None
    self.geom = wg if wg else None


  
  
  #
  # Create a strip of faces with two loops in the geom group
  # l0 >= l1
  #
  #
  #     X---------------------X---------------------X
  #     |\                                    ----- |
  #     | \                               ----      |
  #     |  \                           ---          |
  #     |   x-------------------------x..           |
  #     |   |                         |  ...        |
  #     |   |                         |      ..     |
  #     |   |                         |        ...  |
  #     |   |                         |           ..X
  #     |   |                         |             |
  #     |   x--------e=l1.j0----------x..           |
  #     |  /                             ...        |
  #     | /                                  ..     |
  #     |/                                     .... |
  #     X---------------e0=l0.0---------------------X
  #
  # Return the list of faces defined by a list of vertex indexes
  #
  def createStrip(self, l0, l1, Rep0, Rep1, minAngle=0.7854, minCosinus=0.01):
    ''' Create a strip of faces from two loops in the geom group.

    Parameters
    ----------
    l0 : list of Edge
      First list of egdes

    l1 : list of Edge
      Second list of egdes

    Returns
    -------
    list of faces
        list of faces defined by a list of vertex indexes
    '''
  
    lstFaces = []
    nbl0 = len(l0)
    nbl1 = len(l1)

    if (nbl0==0) or (nbl1==0):
      return C_ERROR

    if nbl0<nbl1: # Swap lists and Coord Systems
      # The faces will be build in the wrong order (wrt normal)
      l0, nbl0, Rep0, l1, nbl1, Rep1 = l1, nbl1, Rep1, l0, nbl0, Rep0
      swaped = True
    else:
      swaped = False
    
    if WFBasic.PYPOS3D_TRACE:
      for i in range(0,nbl0):self.geom.addMaterial(f'DebugMat{i}')
      self.geom.curGroup = self
    
    hasTexture = min( [ l.hasTexture for l in l0 ] ) and min( [ l.hasTexture for l in l1 ] )
    
    # Change coordinates to l0 coordinate system
    l0 = Rep0.To(l0, hasTexture=hasTexture)
    l1 = Rep0.To(l1, hasTexture=hasTexture)
      
    # j0 : Edge number in l1 where p0 is the closest to the first point of l0
    dmin = sys.float_info.max
    P0 = l0[0].p0
    j0 = -1
    # New heuristic: Estimate the distance at the Middle of segment
    mide0 = Point3d(P0).add(l0[0].p1).scale(0.5)
    for j,e in enumerate(l1):
      d = mide0.distance(Point3d(e.p0).add(e.p1).scale(0.5))
      if d<dmin:
        j0 = j
        dmin = d
      
    oneAgain = True
    j, jmax = j0, (j0-1)%nbl1
    i, imax = 0, nbl0-1
    e0Consumed, e1Consumed = False, False
      
    # Plot the strips
    #Plot(l0,l1)
    
    nbFaceInit = self.getNbFace()
    
    while oneAgain:
      if WFBasic.PYPOS3D_TRACE:
        self.geom.selectMaterial(f'DebugMat{i}')
          
      e0 = l0[i]
      e1 = l1[j]

      configUtil = 2*e0Consumed + e1Consumed
      if configUtil==0: # 2 New edges
        # Try a Quadrangle
        amin, aidx, cmin, cidx, vn = Regularity(e0.p0, e0.p1, e1.p1, e1.p0)
        if WFBasic.PYPOS3D_TRACE: print('createStrip({0:d},{1:d}) - sin[{2:g}, {3:d}] - cos[{4:g}, {5:d}] - {6:s}'.format(i,j, amin*180.0/math.pi, aidx, cmin, cidx,str(vn)))

        if (cmin>minCosinus) and (amin>minAngle): # Create a QuadAngle
          # Create a quandrangular face          
          texIdxs = [ IndexAdd(self.texList, P.texture) for P in [ e0.p0, e0.p1, e1.p1, e1.p0 ] ] if hasTexture else [ ]
          vexIdxs = [e0.idx0, e0.idx1, e1.idx1, e1.idx0]
          e0Consumed = True
          e1Consumed = True
          if WFBasic.PYPOS3D_TRACE: print('  Quad {0:s} {1:s} {2:s} {3:s}'.format(str(e0.p0), str(e0.p1), str(e1.p1), str(e1.p0)))

        elif ((aidx==0) or (aidx==2)) or ((cidx==1) or (cidx==3)): # Create a T1 triangle
          texIdxs = [ IndexAdd(self.texList, P.texture) for P in [ e0.p0, e0.p1, e1.p0 ] ] if hasTexture else [ ]
          vexIdxs = [e0.idx0, e0.idx1, e1.idx0]
          e0Consumed = True
          e1Consumed = False
          if WFBasic.PYPOS3D_TRACE: print('  Tri1 {0:s} {1:s} {2:s}'.format(str(e0.p0), str(e0.p1), str(e1.p0)))

        else: # Create a T2 triangle
          texIdxs = [ IndexAdd(self.texList, P.texture) for P in [ e0.p0, e1.p1, e1.p0 ] ] if hasTexture else [ ]
          vexIdxs = [e0.idx0, e1.idx1, e1.idx0]
          e0Consumed = False
          e1Consumed = True          
          if WFBasic.PYPOS3D_TRACE: print('  Tri2 {0:s} {1:s} {2:s}'.format(str(e0.p0), str(e1.p1), str(e1.p0)))

      elif configUtil==1: # 1 New edge : e0
        texIdxs = [ IndexAdd(self.texList, P.texture) for P in [ e0.p0, e0.p1, e1.p1 ] ] if hasTexture else [ ]
        vexIdxs = [e0.idx0, e0.idx1, e1.idx1 ]
        e0Consumed = True

      elif configUtil==2: # 1 New edge : e1
        texIdxs = [ IndexAdd(self.texList, P.texture) for P in [ e0.p1, e1.p1, e1.p0 ] ] if hasTexture else [ ]
        vexIdxs = [e0.idx1, e1.idx1, e1.idx0]
        e1Consumed = True

      #else: print('Impossible') : e0Consumed and e0Consumed can be both false


      # Add the new face taking into accound the reverted loops
      if not swaped:
        vexIdxs.reverse()
        texIdxs.reverse()

      lstFaces += self.addFace( vexIdxs, texIdxs, [ ] )

      # Compute new egdes
      if (i==imax) and (j==jmax):
        if e0Consumed and (i!=imax):
          i+=1
          e0 = l0[i]
          e0Consumed = False
          
        if e1Consumed and (j!=jmax):
          j = (j+1)%nbl1 
          e1 = l1[j]
          e1Consumed = False
          
        oneAgain = False
      else:
        if e0Consumed and (i!=imax): 
          i+=1
          e0Consumed = False
              
        if e1Consumed and (j!=jmax):
          j = (j+1)%nbl1
          e1Consumed = False
    # Wend        
  
    # Final Edges may not be consumed
    # Create a last triangle
    if (not e0Consumed and e1Consumed):
      texIdxs = [ IndexAdd(self.texList, P.texture) for P in [ e0.p0, e0.p1, e1.p1 ] ] if hasTexture else [ ]
      vexIdxs = [e0.idx0, e0.idx1, e1.idx1 ]
      if swaped:
        vexIdxs.reverse()
        texIdxs.reverse()
      lstFaces += self.addFace( vexIdxs, texIdxs, [ ] )

    elif not e1Consumed and e0Consumed:
      texIdxs = [ IndexAdd(self.texList, P.texture) for P in [ e0.p1, e1.p1, e1.p0 ] ] if hasTexture else [ ]
      vexIdxs = [e0.idx1, e1.idx1, e1.idx0]
      if swaped:
        vexIdxs.reverse()
        texIdxs.reverse()
      lstFaces += self.addFace( vexIdxs, texIdxs, [ ] )

    if WFBasic.PYPOS3D_TRACE: print('==> createStrip[{0:s}]: InitFace={1:d} NewFaces={2:d}'.format(self.getName(), nbFaceInit, self.getNbFace()))
      
    return lstFaces    
       
       
  def calcCoordSyst(self, faceno=0, orientation='XZY'):
    ''' Create a coordinate system from the first (default) face of a group.
    The face is supposed to be a square (at least) 4 edges

    (Oy)

     3        2
      +-------+
      ^       |
   eu |   X   |
      |       |
      +------>+          (Ox)
     0   ev    1

    Parameters
    ----------
    faceno : int
        Index of the face to use
    orientation : str
      Orientation of coord (NOT USED - RESERVED FOR FUTURE)

    Returns
    -------
    CoordSyst
      A new 3D Coordinate System at the center of the face (X, eu, ev)
      the third vector of the coordinate system: ew = eu x ev
    '''

    vxtab = self.getFaceVertex(faceno)
    eu = Vector3d( vxtab[3].x - vxtab[0].x, vxtab[3].y - vxtab[0].y, vxtab[3].z - vxtab[0].z).normalize()
    ev = Vector3d( vxtab[1].x - vxtab[0].x, vxtab[1].y - vxtab[0].y, vxtab[1].z - vxtab[0].z).normalize()       
    center = Point3d(vxtab[3].x + vxtab[1].x, vxtab[3].y + vxtab[1].y, vxtab[3].z + vxtab[1].z).scale(0.5)
    
    return CoordSyst(center, eu, ev)

  @classmethod
  def getCoordSyst(clz, centerOrRepOrPlane, eu=None, ev=None):
    ''' Create a coordinate system from the given input. 
    Parameters
    ----------
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
    '''
    if isinstance(centerOrRepOrPlane, Point3d):
      rep = CoordSyst(centerOrRepOrPlane, eu, ev)
    elif isinstance(centerOrRepOrPlane, CoordSyst):
      rep = centerOrRepOrPlane
    else: # Supposed to be a plane
      rep = centerOrRepOrPlane.calcCoordSyst()

    return rep
  
  
  def calcBarycentre(self):
    '''Compute and return the iso barycentre of the used vertex. '''
    # Consider each vertex once
    return Point3d.barycentre([ self.coordList[i] for i in set(self.vertIdx) ])

  # ---------------------------------------------------------------------------
  # TODO: Move it in WFBasic for a more general usage and wall it the vertex
  # list of the GeomGroup
  #
  def RadialScale(self, center, eu, ev, dh, ds, R, nbLoop=0, topPlaneGrp=None):
    ''' Perform a quadratic Radial Scaling of vertexes.

    - Modified Point are below the top Coord. Syst and z>0.0 in the (center, eu, ev) one
      The top Coord system is either given by topPlaneGrp of computed as follow:
      TopCoord = ( center + (0,0,dh), eu, ev )
    - Modify the impunt vertex
    - The scaling curve is defined by the point [-ds, 0] and [+dh, R] 
      where R is a supposed Radius of the vextex at coordinate z = dh

      The Parabol z = a.r² 
      

      O = the center
   
                                ^ Scale Ratio
                                |                           .....  X (usually 1.0 (100%))
                                |                .....   X
                                |        ..... X
                                |    ..X
                                |  .. 
                               .x..
                             .  |
                           .    |
                          .     |
                         .      |
      ------------------x-------O-----------------------------------|--------------> Oz
                       -ds      |                                   dh
                                |        .....
 

 
    Parameters
    ----------
    center : Point3d
      Center of the bottom Plan

    eu : Vector3d
      First Vector of the bottom Plan

    ev : Vector3d
      Second Vector of the bottom Plan (eu and ev are supposed unitary and orthog)

    dh : float
      Height limit of the Parabol
    ds : float
      Down limit of the Parabol
    R : float
      Radius of the parabol in dh

    Returns
    -------
    GeomGroup
      returns self
  
    '''
    if WFBasic.PYPOS3D_TRACE: print('RadialScale({0:s}) ------------------------ '.format(self.getName()))
  
    # Compute the Cutting axis and the transformation matrix of the reference plan
    _,M,MT = CreateTransform(eu, ev)
  
    # Compute the 'a' coef of the Parabol z = a.r² - ds
    a = (dh+ds) / R / R
  
    rd2 = R*R
  
    if topPlaneGrp:
      centerTop, euTop, evTop = topPlaneGrp.calcCoordSyst()

      _, Mtop, _ = CreateTransform(euTop, evTop)

      # For each point in the upper cylinder and below the topPlane : Do a radial quadratic scaling
      for p in self.geom.coordList:
        
        # In top the Coord Syst
        pInTop = Point3d(p).sub(centerTop).inLin33(Mtop)
        
        if pInTop.z<FEPSILON:
          # Change for Cutting Plan Coordinate System
          p.sub(center).inLin33(M)
          
          # if (p.z>=-FEPSILON) and (p.z <= dh+FEPSILON) and (p.x*p.x+p.y*p.y < rd2): FIX Avoid double z condition
          if (p.z>=-FEPSILON) and (p.x*p.x+p.y*p.y < rd2):
            k = math.sqrt( (p.z + ds) / a) / R
            p.scale(k)
      
          # Change (back) to initial Coordinate System
          p.inLin33(MT).add(center) 
      
    else:
      # For each point in the upper cylinder : Do a radial quadratic scaling
      for p in self.geom.coordList:
        
        # Change for Cutting Plan Coordinate System
        p.sub(center).inLin33(M)
        
        if (p.z>=-FEPSILON) and (p.z <= dh+FEPSILON) and (p.x*p.x+p.y*p.y < rd2):
          k = math.sqrt( (p.z + ds) / a) / R
          p.scale(k)
    
        # Change (back) to initial Coordinate System
        p.inLin33(MT).add(center) 
    
    return self


  def FaceRadialScale(self, center, eu, ev, pc=1.0, lstFaceNo=None, materialName=None):
    ''' Perform a radial scaling of the vertex of a list of faces.
    '''
    if WFBasic.PYPOS3D_TRACE: print('FaceRadialScale({0:s}) ------------------------ '.format(self.getName()))
    
    nbface = self.getNbFace()
    if not lstFaceNo:
      matidx = self.lstMat.index(materialName)
      lstFaceNo = [ fi for fi in range(0, nbface) if self.matIdx[fi].fAttr&C_FACE_MATMASK==matidx ]
 
    # Compute the Cutting axis and the transformation matrix of the reference plan
    _,M,MT = CreateTransform(eu, ev)
    
    ptMap = { vi : self.coordList[vi] for fi in lstFaceNo for vi in self.vertIdx[self.stripCount[fi]:self.stripCount[fi+1]] }
        
    # For each point in the upper cylinder : Do a radial quadratic scaling
    for p in ptMap.values():
      # Change for Cutting Plan Coordinate System
      p.sub(center).inLin33(M)
      
      p.scale(pc)
  
      # Change (back) to initial Coordinate System
      p.inLin33(MT).add(center) 
    
    return self
  

  def translate(self, tx=0.0, ty=0.0, tz=0.0):
    ''' Translate the group of the given vector.
    This method creates new vertex (Point3d) in the coordList (usually in WaveGeom)
    
    Parameters
    ----------
    tx,ty,tz : Translation coordinates
    
    Return
    ------
    self for convenience
    '''
    # Create an empty mapping tables
    nbInit = len(self.coordList)      
    mapVert  = [-2] * nbInit

    vertIdxSet = set( self.vertIdx )
    
    v = Point3d(tx,ty,tz)
    nbPt = nbInit
    # Create new translated points
    for vi in vertIdxSet:
      p = Point3d(self.coordList[vi])
      p.add(v)
      self.coordList.append(p)
      mapVert[vi] = nbPt
      nbPt += 1
      
    # Remap Group's vertex indexes with the new ones
    self.vertIdx[:] = array.array('l', [ mapVert[vi] for vi in self.vertIdx ] )
    
    return self
    
  
  def rotate(self, rx=0.0, ry=0.0, rz=0.0, cx=0.0, cy=0.0, cz=0.0, AxisOrder='xyz'):
    ''' Rotate the group around standard axis with an optional rotation center and
    according given rotation orders.    
    Angles in degrees.
    This method creates new vertex (Point3d) in the coordList (usually in WaveGeom)
    
    Parameters
    ----------
    rx,ry,rz : Axis rotation angles (float)
    cx,cy,cz : Center coordinates
    axisOrder : str, defaul 'xyz'
      Rotation order between 'xyz', 'yzx' and 'zxy'
    
    Return
    ------
    self for convenience
    
    '''
    # Create an empty mapping tables
    nbInit = len(self.coordList)      
    mapVert  = [-2] * nbInit

    vertIdxSet = set( self.vertIdx )
    
    # Create the center for a simple origin usage
    center = Point3d(cx,cy,cz)

    theta = rx*math.pi/180.0
    c, s = math.cos(theta), math.sin(theta)
    MRotX = [ \
       [ 1.0, 0.0, 0.0], \
       [ 0.0,   c, - s ], \
       [ 0.0,   s,   c ], \
       ]
  
    theta = ry*math.pi/180.0
    c, s = math.cos(theta), math.sin(theta)
    MRotY = [ \
       [   c, 0.0,   s ], \
       [ 0.0, 1.0, 0.0 ], \
       [ - s, 0.0,   c ], \
       ]

    theta = rz*math.pi/180.0
    c, s = math.cos(theta), math.sin(theta)
    MRotZ = [ \
      [   c, - s, 0.0], \
      [   s,   c, 0.0 ], \
      [ 0.0, 0.0, 1.0 ], \
      ]

    if AxisOrder=='xyz':
      m = MxProd(MRotY, MRotX)
      m = MxProd(MRotZ, m)
    elif AxisOrder=='yzx':
      m = MxProd(MRotZ, MRotY)
      m = MxProd(MRotX, m)
    else: # zxy
      m = MxProd(MRotX, MRotZ)
      m = MxProd(MRotY, m)
    
    nbPt = nbInit
    # Create new rotated points
    for vi in vertIdxSet:
      p = Point3d(self.coordList[vi])
      p.sub(center)
      p.inLin33(m)
      p.add(center)
      self.coordList.append(p)
      mapVert[vi] = nbPt
      nbPt += 1
      
    # Remap Group's vertex indexes with the new ones
    self.vertIdx[:] = array.array('l', [ mapVert[vi] for vi in self.vertIdx ] )
    
    return self


  def mirror(self, centerOrRepOrPlane=None, eu=None, ev=None, duplicateData=False):
    ''' Mirror the group along standard planes with an optional origin center.

    This method creates new vertex (Point3d) in the coordList (usually in WaveGeom)
    if duplicateData is True
    
    Parameters
    ----------
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
    
    Return
    ------
    self for convenience
    '''
    
    # Compute the mirroring Frame
    rep = GeomGroup.getCoordSyst(centerOrRepOrPlane, eu, ev)
    
    # Compute the transformation matrix
    BT = MxProd(rep.MT, [ [ 1.0, 0.0, 0.0],  [ 0.0, 1.0, 0.0],  [ 0.0, 0.0, -1.0],  ])
    FT = MxProd(BT, rep.M)

    if duplicateData:
      nextVi = len(self.coordList)
      vertIdxCvt = [ -1 ]*nextVi
      
      # For each face create new vertex indexes
      for i in self.vertIdx:
        if vertIdxCvt[i]==-1:
          vertIdxCvt[i] = nextVi
          nextVi +=1
          self.coordList.append(Point3d(self.coordList[i]))

      self.vertIdx[:] = array.array('l', [ vertIdxCvt[vi] for vi in self.vertIdx ] )
    
    for no in set( self.vertIdx ):
      self.coordList[no].sub(rep.center).inLin33(FT).add(rep.center)
  
    # Invert face orders
    self.invertFaceOrder()
    
    return self


  def symetry(self, cx=0.0, cy=0.0, cz=0.0, sym='symxy'):
    ''' Mirror the group along standard planes with an optional origin center.

    This method creates new vertex (Point3d) in the coordList (usually in WaveGeom)
    
    Parameters
    ----------
    cx,cy,cz : Center coordinates
    sym : str, defaul 'symxy'
      Plan for symetry 'symxy', 'symyz' and 'symzx'
    
    Return
    ------
    self for convenience
    '''
    if sym=='symxy':
      eu = Vector3d(1.0 ,0.0, 0.0)
      ev = Vector3d(0.0, 1.0, 0.0)
    elif sym=='symyz':
      eu = Vector3d(0.0, 1.0, 0.0)
      ev = Vector3d(0.0 ,0.0, 1.0)
    else: # symzx
      eu = Vector3d(0.0 ,0.0, 1.0)
      ev = Vector3d(1.0, 0.0, 0.0)
    
    return self.mirror(Point3d(cx,cy,cz), eu, ev, True)
    
    
    
  def calcFaceOrientation(self, faceno=-1, materialName=None, AxisOrder='xyz'):
    ''' Compute the orientation of a face according to an Axis order (xyz, yzx, zxy).
    
    The orientation is the set of rotations that aligns the first axis of the
    axis order on the face normal vector.
    
    Parameters
    ----------
    faceno : int
      Face to remove (if >0)

    materialName : str, default None
      Name of the material. Use the first face with this material
      
    axisOrder : str, default 'xyz'
      Rotation order between 'xyz', 'yzx' and 'zxy'

    Returns
    -------
    int, Vector3d
      C_OK : Success
      C_FAIL : faceno==-1 and materialName not found
      C_ERROR : Face Index Error
    '''
    if faceno==-1:
      if materialName:
        try:
          matidx = self.lstMat.index(materialName)
          faceno = self.findFace(matidx)
          if faceno<0:
            return C_FAIL, None
        except ValueError:
          return C_FAIL, None
      else:
        return C_ERROR, None
    elif (faceno<0) or (faceno>=self.getNbFace()):
      return C_ERROR, None

    ret, vr = C_OK, None
    vxtab = self.getFaceVertex(faceno)    
    if vxtab and len(vxtab)>=3:
      # Perform the orientation computation  
      vr = Point3d.face_orientation(vxtab, AxisOrder=AxisOrder, inDegrees=True)              
    else:  
      ret = C_FAIL
            
    return ret, vr


  def unTriangularize(self, maxsin=FEPSILON, algo=C_FACE_NONE, surfaceThreshold=0.1):
    ''' Untriangularize the current group (inplace).
    Triangular faces are merged when:
    * They have the same material
    * They have a common edge
    * The sinus of their normals (angle) is smaller than 'maxsin' and 
      when 'algo' parameter is C_FACE_SURF if the merged face represents more than 'surfaceThreshold' percent
      of the final face.
    
    Parameters
    ----------
    maxsin: float, Optional, default = FEPSILON
      Maximal value for the sinus of the angle of both
      normals to permit a face merge
      
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
      >=0    : Number of faces in the result group
      C_FAIL : No face to merge
    
    '''
    lstTri = []
    nVertIdx = [] 
    nMatIdx = [] 
    nStrip = [0, ]
    initNbFace = self.getNbFace()
    
    # Initialize a list of list of triangles indexed by the vertex Id
    vertexId2Tri = [ None ] * len(self.coordList)
    
    for noface in range(0, initNbFace):
       
      startIdx = self.getFaceStartIdx(noface)
      lastIdx = self.getFaceLastIdx(noface)
      keepIt = (lastIdx-startIdx!=3)
      
      if not keepIt: # It's a triangle
        # Create a triangular face with some pre-computed values
        p0,p1,p2 = self.vertIdx[startIdx], self.vertIdx[startIdx+1], self.vertIdx[startIdx+2]
        tf = TriFace(noface, p0, p1, p2, coordList=self.coordList)

        if tf.surface > FEPSILON2: # Filter too small or null surface
          lstTri.append(tf)
          
          for i in [p0, p1, p2]:
            l = vertexId2Tri[i]
            if l is None:
              vertexId2Tri[i] = [ tf, ]
            elif not tf in l:
              l.append(tf)
        else: # Triangular surface is too small, Store it
          keepIt = True
           
      if keepIt: # Just copy non triangular face OR rejected triangles
        nVertIdx += self.vertIdx[startIdx:lastIdx]
        nStrip.append(len(nVertIdx))
        nMatIdx.append(self.matIdx[noface])
    
    dn2 = maxsin*maxsin
    # Check triangle by 2 with a filter on the material index and according to the 'algo'
    # a comparison of surfaces
    while lstTri:
      # Get the first triangle
      curTri = lstTri.pop()
      p0, p1, p2 = curTri.p0, curTri.p1, curTri.p2
      ltri0, ltri1, ltri2 = vertexId2Tri[p0], vertexId2Tri[p1], vertexId2Tri[p2]

      ltri0.remove(curTri)
      ltri1.remove(curTri)
      ltri2.remove(curTri)
      
      fao = self.matIdx[curTri.noface]
      mi = fao.fAttr
      
      # Compute the list of candidate triangles:
      lstCandidateTri = ltri0.copy() if ltri0 else []
      lstCandidateTri += [ t for t in (ltri1 if ltri1 else []) if t not in lstCandidateTri ]
      lstCandidateTri += [ t for t in (ltri2 if ltri2 else []) if t not in lstCandidateTri ]
      
      # Compute the list of adjacent triangles (up to 3)
      e0,e1,e2 = curTri.edges
      lstAdj = [ t for t in lstCandidateTri \
                  if (self.matIdx[t.noface].fAttr==mi) and \
                    ( (e0 in t.revedges) or (e1 in t.revedges) or (e2 in t.revedges) ) and \
                    (curTri.vnorm.cross(t.vnorm).norme2() <= dn2) ]
      
      if algo & C_FACE_SURF: # Add a filter on surface comparison
        lstAdj = [ t for t in lstAdj if math.fabs(t.surface/(curTri.surface + t.surface)) >= surfaceThreshold ]
        
      if lstAdj: # Choose the 'best' triangle to merge
        adjTri, ceCurTri = curTri.choose(lstAdj, algo)

        # Remove Adjacent Triangle from the list of available faces
        lstTri.remove(adjTri)
        
        vertexId2Tri[adjTri.p0].remove(adjTri)
        vertexId2Tri[adjTri.p1].remove(adjTri)
        vertexId2Tri[adjTri.p2].remove(adjTri)
          
        # Merge curTri and adjTri
        cea = adjTri.commEdge(curTri)
        pp = adjTri.p2 if cea==0 else (adjTri.p0 if cea==1 else adjTri.p1)
        if ceCurTri==0:
          tv = [ curTri.p0, pp, curTri.p1, curTri.p2 ]
        elif ceCurTri==1:
          tv = [ curTri.p0, curTri.p1, pp, curTri.p2 ]
        else:
          tv = [ curTri.p0, curTri.p1, curTri.p2, pp ]

        nVertIdx += tv
        nStrip.append(len(nVertIdx))
        nMatIdx.append(fao)
        
        adjFao = self.matIdx[adjTri.noface]
        
        if fao.fAttr & C_FACE_TEXT:
          tp = adjFao.tvertIdx[2] if cea==0 else (adjFao.tvertIdx[0] if cea==1 else adjFao.tvertIdx[1])

          if ceCurTri==0:
            fao.tvertIdx = array.array('l', [ fao.tvertIdx[0], tp, fao.tvertIdx[0+1], fao.tvertIdx[0+2] ])
          elif ceCurTri==1:
            fao.tvertIdx = array.array('l', [ fao.tvertIdx[0], fao.tvertIdx[0+1], tp, fao.tvertIdx[0+2] ])
          else:
            fao.tvertIdx = array.array('l', [ fao.tvertIdx[0], fao.tvertIdx[0+1], fao.tvertIdx[0+2], tp ])

        if self.matIdx[curTri.noface].fAttr & C_FACE_NORM: 
          np = adjFao.normIdx[2] if cea==0 else (adjFao.normIdx[0] if cea==1 else adjFao.normIdx[1])

          if ceCurTri==0:
            fao.normIdx = array.array('l', [ fao.normIdx[0], np, fao.normIdx[0+1], fao.normIdx[0+2] ])
          elif ceCurTri==1:
            fao.normIdx = array.array('l', [ fao.normIdx[0], fao.normIdx[0+1], np, fao.normIdx[0+2] ])
          else:
            fao.normIdx = array.array('l', [ fao.normIdx[0], fao.normIdx[0+1], fao.normIdx[0+2], np ])
        
      else: # The current triangle has no relevant adjacent, Add it to the new group
        startIdx = self.getFaceStartIdx(curTri.noface)
        lastIdx = self.getFaceLastIdx(curTri.noface)
        nVertIdx += self.vertIdx[startIdx:lastIdx]
        nStrip.append(len(nVertIdx))
        nMatIdx.append(self.matIdx[curTri.noface])
      
    #End of While LstTri
    
    # Finish the modification of the group
    self.vertIdx[:] = array.array('l', nVertIdx) 
    self.stripCount[:] = array.array('l', nStrip)
    self.matIdx[:] = nMatIdx
    
    return self.getNbFace() if initNbFace > self.getNbFace() else C_FAIL
    
      
  
# Named tuple replaced by a 'sloted' class for both performance and extension
#TriFace = collections.namedtuple('TriFace', ['noface', 'p0', 'p1', 'p2', 'vnorm', 'edges', 'revedges'])

class TriFace:
  ''' This class represents a triangular face used during 'Untriangularization' algorithm.
  '''
  noface:int
  p0:int
  p1:int
  p2:int
  edges:tuple
  revedges:tuple
  vnorm:float
  lenedges:tuple
  surface:float
  
  def __init__(self, noface, p0, p1, p2, coordList=None):
    
    self.noface = noface
    self.p0 = p0          
    self.p1 = p1
    self.p2 = p2
              
    self.edges =  ( (p0,p1), (p1,p2), (p2,p0) )
    self.revedges = ( (p0,p2), (p2,p1), (p1,p0) )
    
    # Perform computations
    if coordList:
      cp0,cp1,cp2 = coordList[p0], coordList[p1], coordList[p2]
      
      # Compute Normale
      self.vnorm = Point3d.triangle_normal(cp0, cp1, cp2)
      
      # Compute each edges length
      l0,l1,l2 = cp0.distance(cp1), cp1.distance(cp2), cp2.distance(cp0)
      self.lenedges = ( l0, l1, l2 )
      
      # Compute Surface (Heron formula)
      # Protect from rounding effects that create very small negative s2
      p = 0.5*(l0+l1+l2)
      s2 = p*(p-l0)*(p-l1)*(p-l2)
      self.surface = 0.0 if s2 < 0.0 else math.sqrt(s2) 
      
  def commEdge(self, adjt):
    return 0 if (self.p0,self.p1) in adjt.revedges else \
           (1 if (self.p1,self.p2) in adjt.revedges else \
            (2 if (self.p2, self.p0) in adjt.revedges else -1))
           
  def choose(self, lstAdj, algo):
    adjTri = lstAdj[0]
    if algo & C_FACE_ORDER_ANGLE:
      sinus2 = self.vnorm.cross(adjTri.vnorm).norme2()
      
      if len(lstAdj)>1:
        ns = self.vnorm.cross(lstAdj[1].vnorm).norme2()
        if ns < sinus2:
          adjTri = lstAdj[1]
          sinus2 = ns
          
      if len(lstAdj)>2:
        ns = self.vnorm.cross(lstAdj[2].vnorm).norme2()
        if ns < sinus2:
          adjTri = lstAdj[2]

      ceCurTri = self.commEdge(adjTri)
      
    elif algo & C_FACE_ORDER_SURF: #Keep the most contributing triangle
      deltas = math.fabs( adjTri.surface / (adjTri.surface + self.surface ) )
      
      if len(lstAdj)>1:
        nd = math.fabs( lstAdj[1].surface / (lstAdj[1].surface + self.surface))
        if nd > deltas:
          adjTri = lstAdj[1]
          deltas= nd
          
      if len(lstAdj)>2:
        nd = math.fabs( lstAdj[2].surface / (lstAdj[2].surface + self.surface))
        if nd > deltas:
          adjTri = lstAdj[2]

      ceCurTri = self.commEdge(adjTri)

    else: # algo & C_FACE_ORDER_LENGTH:    
      # Find the common Edge
      ceCurTri = self.commEdge(adjTri)
      lenEdge  = self.lenedges[ceCurTri]
      
      if len(lstAdj)>1:
        ce = self.commEdge(lstAdj[1])
        le = self.lenedges[ce]
        if le > lenEdge:
          adjTri = lstAdj[1]
          lenEdge = le
          ceCurTri = ce
          
      if len(lstAdj)>2:
        ce = self.commEdge(lstAdj[2])
        le = self.lenedges[ce]
        if le > lenEdge:
          adjTri = lstAdj[2]
          ceCurTri = ce
      
      
    return adjTri, ceCurTri
#








