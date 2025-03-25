'''
Created on 7 août 2022

Prototype of a DAZ3D DSON file to Poser translator

@author: olivier
'''

import os.path
import json
import gzip
import logging
from urllib.parse import urlparse, unquote


from pypos3d.wftk.WFBasic import PYPOS3D_TRACE, Point3d, TexCoord2f, Vector3d
from pypos3d.wftk.WaveGeom import WaveGeom
from pypos3d.pftk.PoserBasic import PoserToken
from pypos3d.pftk.PoserMeshed import PoserProp
from pypos3d.pftk.ChannelImportAnalysis import FigurePart, ChannelDescriptor



class DSONConst:
  ''' DSON fileformat constants. Should be moved later in its own module.
  '''
  GEOM_LIB = 'geometry_library'
  NODE_LIB = 'node_library'
  

class DSONLibrary:
  ''' This class is a singleton, that holds common library files. '''
  def __init__(self, DSONRoot='.'):
    self.rootDir = DSONRoot
    self.fileMap = {}
  
  def addDSONFile(self, dfic:'DSONFile'):
    self.fileMap[dfic.dsonID] = dfic
  
  def getDSONFile(self, fn):
    try:
      dfic = self.fileMap[fn]
      
    except KeyError:
      dfic = DSONFile(os.path.join(self.rootDir, fn[1:] if fn[0]==os.sep else fn))
      self.addDSONFile(dfic)
      
    return dfic
  
  def getDSONFileByURI(self, uri):
    op = urlparse(uri)
    
    # print(str(op))
    # print(unquote(uri))
       
    return self.getDSONFile(unquote(op.path))
  

''' The singleton for all shared files '''
DSONLIB = None

class DSONFile:
  '''
  ** PROTOTYPE **

  DSON File internal representation. JSON tree based (for the moment)

  '''

  def __init__(self, fn, DSONRoot=None, analysis=True):
    '''
    ** PROTOTYPE **
    Open and parse a .dsf/.duf file and return the loaded object tree.
    '''
    global DSONLIB
    
    if DSONLIB is None:
      DSONLIB = DSONLibrary(DSONRoot)
    
    try:      
      p = fn.lower().rfind('.dsf')
      self.isDSF = (p>0)
      self.filename = fn
      
      # Create an input stream
      rin = gzip.open(fn, 'rt', errors='replace') 
      self.tree = json.loads(rin.read()) # .decode("ascii"))
      rin.close()
 
      # Retrieve the asset ID and its type
      ai = self.tree.get('asset_info')
      self.dsonID   = ai.get('id')
      self.dsonType = ai.get('type')
      
      # Record it in the library
      DSONLIB.addDSONFile(self)
 
      if analysis:
        self.analyse()

    except FileNotFoundError as e:
      if PYPOS3D_TRACE: print(f'File({fn} - Read Error {e.args}')

    
  def analyse(self):
    '''
    ** PROTOTYPE **
    Scan the DSON file to detect its content and its links (references) with other files.
    '''
    logging.info(f"File Analysis[{self.filename}] : ID={self.dsonID} TYPE={self.dsonType}")


  def loadGeom(self):
    '''
    ** PROTOTYPE **

    Read a dsf/duf file and extract the included geometries.

    Return
    ------
      A list of WaveGeom read in the DSON file itsself or in referenced files.
    
    '''
    global DSONLIB
    lstGeom = []
    
    # Retrieve the list of geometries
    gl = self.tree.get(DSONConst.GEOM_LIB)
    
    if not gl:
      logging.error("File[%s]: no geometry", self.dsonID)
      return None
    
    
    for geom in gl:
      wg = WaveGeom()
      
      geomid = geom.get('id')
      vertices = geom.get('vertices')
      s = vertices.get('count')
      print(f'# id:{geomid} Vertices.count={s}')
      wg.setName(geomid)
      
      # Retrieve Vertices coordinates
      verttab = vertices.get('values')
      wg.coordList = [ Point3d(vert) for vert in verttab ]
    
      groupnames = geom.get('polygon_groups')
      
      # TODO: Create Materials    
      mats = geom.get('polygon_material_groups')
      
      for matName in mats.get('values'):
        wg.addMaterial(matName)
      
      
      # Retrieve the default UV Set of the geometry (URI)
      defaultUVSet = geom.get('default_uv_set')
      
      op = urlparse(defaultUVSet)
      if op.path:
        uvset = DSONLIB.getDSONFileByURI(defaultUVSet)
        if uvset is not None and (uvset.dsonType=='uv_set'):
          # Retrive UV data and prepare a mapping structure
          uvSetLib =  uvset.tree.get('uv_set_library')
        else:
          logging.warn(f'defaultUVSet has a wrong type {uvset.dsonType}')

      elif op.fragment:
        uvSetLib = self.tree.get('uv_set_library')
        
      else: # Invalid or empty URI?
        logging.warn(f'defaultUVSet wrong type {op}')
      
      uvSetRes = list(filter(lambda x:x['id']==op.fragment, uvSetLib))
      if uvSetRes:
        uvSet = uvSetRes[0]
        
        # Convert texture coordinates
        uvs = uvSet.get('uvs').get('values')
        wg.texList = [ TexCoord2f(tx[0], tx[1]) for tx in uvs ]
        polylst = uvSet.get('polygon_vertex_indices')
      
      # Get the geometry list of polygons
      polylist = geom.get('polylist')
      
      # Create the list of GeomGroup 
      lstgrp = [ wg.createGeomGroup(dazGrpName) for dazGrpName in groupnames.get('values') ]
      
      for polyno,face in enumerate(polylist.get('values')):
        grp = lstgrp[face[0]]
        grp.curMatIdx = face[1]
        
        #TODO: Manage Normals coordinates?
        
        # Create the face
        if uvSetRes:          
          # Default texture indexes shall match vertice index
          txind = [ i for i in face[2:] ]
          
          #TODO: Ugly O(n2) algo - To optimize
          l = list(filter(lambda x:x[0]==polyno, polylst))
          
          for i,vno in enumerate(face[2:]):
            for polytex in l:
              if polytex[1]==vno:
                txind[i] = polytex[2]
                break
              
          grp.addFace( face[2:], txind, None)
        else:
          grp.addFace( face[2:], None, None)
    
      
      lstGeom.append(wg)
  
    return lstGeom


  def loadProp(self):
    '''
    Read a dsf/duf file and extract the included Properties and Geometries.
    
    '''
    global DSONLIB
    lstProp = []
    
    # Retrieve the list of geometries
    nl = self.tree.get(DSONConst.NODE_LIB)
    
    if not nl:
      logging.error("File[%s]:  no node", self.dsonID)
      return None

    for node in nl:
      pp = PoserProp()
      name=node.get('name')
      center = node.get('center_point')
      orient = node.get('orientation')
      rot = node.get('rotation')
      trans = node.get('translation')
      
      # partType='', level=-1, name=None, printName=None, geom=None, geomGroup=None, oplst=None, \
      #  trans=None, rot=None, orient=None, center=None, hidden=False, addToMenu=True
      fp = FigurePart(partType='act', name=name, printName=node.get('label'), \
                      trans=Vector3d(float(trans[0].get('value')), trans[1].get('value'), trans[2].get('value')), \
                      rot=Vector3d(float(rot[0].get('value')), rot[1].get('value'), rot[2].get('value')), \
                      orient=f"{node.get('rotation_order')}, ({orient[0].get('value')}, {orient[1].get('value')}, {orient[2].get('value')})", \
                      center=Point3d(float(center[0].get('value')), center[1].get('value'), center[2].get('value')))
      
      pp.createDefaultChannels(fp)
      
      scaleXYZ = node.get('scale')
      sX = pp.getGenericTransform(PoserToken.E_propagatingScaleX)
      sX.setInitValue(scaleXYZ[0].get('value'))

      sY = pp.getGenericTransform(PoserToken.E_propagatingScaleX)
      sY.setInitValue(scaleXYZ[1].get('value'))
      
      sZ = pp.getGenericTransform(PoserToken.E_propagatingScaleX)
      sZ.setInitValue(scaleXYZ[2].get('value'))

      scale = node.get('general_scale').get('value')
      gtscale = pp.getGenericTransform(PoserToken.E_propagatingScale)
      gtscale.setInitValue(scale)
      
      endPoint = node.get('end_point')
      pp.setEndPoint(Point3d(float(endPoint[0].get('value')), endPoint[1].get('value'), endPoint[2].get('value')))
      
      
      # Check for 'extra' channels like visibility ...
      extralst = node.get('extra')
      if extralst:
        for e in extralst:
          print(f'ex:{e}')
          channels = e.get('channels')
          if channels:
            for chan in channels:
              print(f'Chan:{chan}')
              chanDef = chan['channel']
              chanID = chanDef.get('id')
              if chanID=='Visible':
                
                curChan = ChannelDescriptor(0, name, \
                                            chanTypeName  = 'visibility', \
                                            chanName      = chanID, \
                                            printName     = chanDef.get('label'), \
                                            initValue     = float(chanDef.get('value')), \
                                            minValue      = 0.0, \
                                            maxValue      = 1.0, \
                                            trackingScale = 1.0)

                ret = curChan.checkLink()
                
              else:
                logging.info(f"Prop {name}: Channel {chanID} ignored")
                
        # Add the list of discovered channels
        # 2022-08-20: Pb : Il me faut une figure ou réimplémenter le importChannels(self, lstChanDest:list, poserRootDir, hideComputed=False)
        # au niveau actor
        
        
      lstProp.append(pp)
      
    #End for node
    
    
    return lstProp



















