'''
Created on 3 nov. 2023

@author: olivier
'''
import logging

from PIL import Image, ImageDraw

from langutil import C_OK, C_FAIL
from pypos3d.wftk.WFBasic import C_FACE_MATMASK


def UVRender(destFile, lstGrp, lstMat=None, size=(1024,1024), \
             lstGrpColors=None, \
             background=(128,128,128,128), backgroundImage=None):
  ''' Draw the UV maps of a list of groups (GeomGroup) and generate an image file.
  
  Parameters
  ----------
  destfile : string
    Path of the destination file
    
  lstGrp : List of GeomGroup
    List of GeomGroups to draw
    
  lstMat : List of string, default None
    List of material to draw. All materials are drawn when None
    
  size : (int, int), default (1024,1024)
    Size of the generated image in pixel
  
  lstGrpColors : list of (R,G,B) or (R,G,B,A) colors
    colors to be used for faces' groups drawing.
    Ignored when length does not match lstGrp's length
  
  background : (R,G,B) or (R,G,B,A)
    Background color in (R,G,B) or in RGBA for transparency management
    
  backgroundImage : str, default None
    Image to load in background. Size will be scaled to match 'size'
  
  '''
  ret = C_OK

  # Image dimensions in float to enhance scaling   
  imWidth, imHeight = float(size[0]), float(size[1])
  
  if backgroundImage:
    # Load the given background image
    im = Image.open(backgroundImage)
    
    # Rescale it - Maps shall be drawn "over" it
    im = im.resize(size, Image.LANCZOS)

  else:
    # Create an empty image with Pillow
    im = Image.new('RGBA' if len(background)==4 else 'RGB', size, color=background)
  
  # Retrieve the drawing context
  gc = ImageDraw.Draw(im)
  
  # Check if groups have their own drawing color
  otherGrpColor = (lstGrpColors!=None) and (len(lstGrpColors)==len(lstGrp))
  
  # For each group 
  for i,grp in enumerate(lstGrp):
    
    # Prevent None group
    if not grp:
      logging.warning(f'Null group ignored: {i}')
      continue
    
    outlineColor = lstGrpColors[i] if otherGrpColor else (0,0,0)
    
    # For each material
    for materialName in (lstMat if lstMat else grp.lstMat):
      matidx = -1
      try:
        matidx = grp.lstMat.index(materialName)
        
        # Retrieve material's faces
        for fao in [ f for f in grp.matIdx if (lstMat==None) or (f.fAttr & C_FACE_MATMASK==matidx)]:
          texTab = [ grp.texList[i] for i in fao.tvertIdx ]          
          ptTab = [ ( (int)( imWidth * tx.x ), size[1] - (int)( imHeight * tx.y ) ) for tx in texTab ]
          
          # Draw faces with the material's color
          gc.polygon(ptTab, outline=outlineColor)
        
      except ValueError:
        logging.warning(f'Draw Material[{materialName}] not found in {grp.getName()}')
        ret = C_FAIL
    
  # Save the image as destFile. May raise OSError
  im.save(destFile, quality=95)

  logging.info(f'File Rendered:[{destFile}] with size {size}')

  return ret

