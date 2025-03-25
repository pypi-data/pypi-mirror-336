
This file is the README of the library pypos3d.

# 1) INTRODUCTION:

This library is a port of the old DATA3D library of the OpenSource Pojamas project.
I own both of them.

pypos3d aims to replace Pojamas.DATA3D library with a very close interface.
Application ePOSER (in Eclipse RCP) is replaced by a new MMI concept based on 
LibreOffice/Python.

This Python library intends to give high level operations for some 3D files:
- WaveFront Files (.OBJ and compressed .obz [gziped]): 
  * Read / Write
  * Groups manupilation : add, remove, optimization, fusion
  * UV texture maps creation and modification
  * High level method:
    Plane Split, Plane Slice, Remesh, Hole filling, untriangularization

  All Wavefront functions (classes) are in the pypos3d.wftk package

- Poser Files (.PZ3, .CR2, .PZZ, .CRZ, .PP2, .PPZ, .HR2, .HRZ):
  * Read / Write
  * Actors, Props, Cameras, ... manipulations\: add, remove, rename
  * Morph report and morph report on alternate geometries
  * Cleaning
  * Character creation
  
  All Poser functions (classes) are in the pypos3d.pftk packages

Initialy, Pojamas project was a Eclipse RCP application based on a SWT/Java3D MMI. 
For maintenance reason, this RCP application will be discontinued and shall be replaced
by another one (cf. chapter 4 'GUI').

#2) INSTALLATION:

##2.1) Library Installation:
The library shall be installed with pip:
`> python3 -m pip --user pypos3d`

##2.2) GUI Install:

  First, download the relevant GUI distribution package from Source Forge: https://sourceforge.net/projects/pojamas/files/
     Filename : PyPos3DLO-X.Y.Z.zip
  Unzip it in your usual work directory (anywhere, in fact)

  1. On _Linux_ (and probably Mac - To Be Confirmed):
     Install first the library and its dependencies
     Launch the GUI installer\: PyPos3D-App-Installer.ods
     Clic on **Check** install first and then on **Install**
     Close LibreOffice

     The installation is finished, you can use the PyPos3DLO.ods computation sheet
     
     For Debian 11, you could have to add support of python to LibreOffice with the following package:
     apt-get install libreoffice-script-provider-python


  2. On _Windows_ (and for pure LibreOffice Installation on Linux)
     You will need to extend the internal Python installation with the dependencies.
     The PyPos3dLO installer will help you.

     Launch the GUI installer : PyPos3D-App-Installer.ods
     Clic on **Check** install first and then on **Install**
     Close LibreOffice
     
     In case of failure, you could need to visit the 'pip' tab of the file PyPos3D-App-Installer.ods
     This tab provides the means to check pip status on your platform and to install or upgrade it if needed.
     
     Important notice\:
     On windows the current working directory is the installation directory of libreoffice (event if you double-click on a file somewhere).
     So, if you need to install pip with the 'Get pip boot' option, you will have to choose a writable destination file for the downloaded module. 
     For example C:\\Users\\olivier\\Documents\\get-pip.py
     
     Then, after a click on 'Install Boot Pip', the results are like\:
     
     **Install stdout**	
     Defaulting to user installation because normal site-packages is not writeable 
     Collecting pip   
     Downloading pip-25.0.1-py3-none-any.whl.metadata (3.7 kB) Collecting setuptools   
     Downloading setuptools-77.0.3-py3-none-any.whl.metadata (6.6 kB) 
     Collecting wheel   
     Downloading wheel-0.45.1-py3-none-any.whl.metadata (2.3 kB) 
     Downloading pip-25.0.1-py3-none-any.whl (1.8 MB)    ---------------------------------------- 1.8/1.8 MB 1.2 MB/s eta 0:00:00 
     Downloading setuptools-77.0.3-py3-none-any.whl (1.3 MB)    ---------------------------------------- 1.3/1.3 MB 1.2 MB/s eta 0:00:00 
     Downloading wheel-0.45.1-py3-none-any.whl (72 kB) 
     Installing collected packages: wheel, setuptools, pip Successfully installed pip-25.0.1 setuptools-77.0.3 wheel-0.45.1 
     
     
     **Install stderr**	  
     WARNING: The script wheel.exe is installed in 'C:\Users\olivier\AppData\Roaming\Python\Python310\Scripts' which is not on PATH.   
     Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.   
     WARNING: The scripts pip.exe, pip3.10.exe and pip3.exe are installed in 'C:\Users\olivier\AppData\Roaming\Python\Python310\Scripts' which is not on PATH.   
     Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location. 
     
     Both warning are  __not relevant__  for pypos3d usage
     

     The installation is finished, you can use the PyPos3DLO.ods sheet as an algorithm launcher.
     
     
	 __deprecated mention__
	 As of May-2021, a **limitation** has appeared on Windows 10 / LibreOffice both 6.4 and >7 using Python 3.7
	 pip 21 is  does not run anymore under LibreOffice 
	 Workaround: Install Python 3.7 on Windows and install pypos3dv manualy


  3. Manual Install:
     Check which version is used (or brought) by LibreOffice
     First, try to Install the 3D viewer (if it works, it will bring all dependencies)\:
     `> python3 -m pip --user pypos3dv`

     In case of pypos3dv trouble, Install the _only_ library:
     `> python3 -m pip --user pypos3d`
     
     From the previously unzipped GUI package:
     copy pypos3dapp.py and pyposinstaller.py files in your LibreOffice Python's scripts directory (create it if needed)
	On Linux:   $HOME/.config/libreoffice/4/user/Scripts/python/
	On Windows: C:\Users\olivier\AppData\Roaming\Python\Python310

    That's all, you can use the PyPos3DLO.ods computation sheet


##2.3) 3D OpenGL Viewer Install:
The Viewer shall be installed with pip:
`> python3 -m pip --user pypos3dv`

According to your system install, you may have to install some libraries:
Pillow (>= 6.2)
glfw (>=3)

On Debian 10 (i386)
  glfw can't find the glfw3 library, because of the installation path
  `apt-get install libglfw3`
  `export PYGLFW_LIBRARY=/lib/i386-linux-gnu/libglfw.so.3`



#3) DESIGN:
The pypos3d Library has the following structure:
  * langutil: A personal generic package for some utilities

  * pypos3d.wftk: WaveFront manipulation package
    The main classes are pypos3d.wftk.WaveGeom and pypos3d.wftk.GeomGroup.
    Refer to WaveGeom documention for information

  * pypos3d.pftk: Poser files manipulation package

  * pypos3d.propslim: Decimation function (port of Michael Garland "SlimKit Surface Modeling Tools")

  * Dependencies:
    - numpy
    - scipy
    - xlrd

The pypod3dv Viewer package has a flat structure:
  * Modules: Window.py and Renderable.py
  * Launcher: pypos3dv (executes __main__.py)

  * Dependencies:
    - pypos3d
    - Pillow
    - PyOpenGL
    - PyGLM
    - GLFW


#4) TESTS:
This library is tested with unitest with a target coverage rate over 90%.
Unit tests are delivered in another package: pypos3dtu
Coding rules are based on CNES (RNC-CNES-Q-HB-80-535) - CNES is the French National Space Agency https://www.cnes.fr -

Installation and commissionning tests are performed on:
- AlmaLinux 9           Python 3.9   LibreOffice 7.1
- AlmaLinux 9           Python 3.12  LibreOffice 7.1
- CentOS 8, 7           Python 3.6   LibreOffice 6.4 : Deprecated
- Fedora >34            Python 3.10  LibreOffice 7.2
- Debian 10 (i386)      Python 3.7   LibreOffice 7.0 : Deprecated
- debian 11             Python 3.9   LibreOffice 7.1
- Microsoft Windows 10  Python 3.10  LibreOffice 25

#5) GUI:
As mentioned previously, the former Pojamas application was an Eclipse RCP (obsolete RCP3).
For tests purpose, a LibreOffice calc based GUI is proposed.
The GUI requires LibreOffice >= 6.4 on Windows and LibreOffice >= 6.3 on Linux (CentOS > 7)

This version of the library provides a simple 3d Viewer (cf. pypo3dv)

#6) LIMITATIONS:
pypos3d read/write operations have been validated on Poser9, Poser11 and partially with Poser12
Nevertheless, some new features in Poser11/Poser12 or Poser13 may generate mis-interpretation 

#LICENCE:
This library is delivered under the BSD license.


KR, Olivier


------------

#Dev Notes

Add a View on Poser File
Extract WFMat from Poser File
- Options

Add a View in Edit Sheet
  * File (scene, character(s), prop(s))
  * Character
  * Prop
  * Actor
  * Channel

Add a Menu to the viewer
  - Hide/Show parts (groups)
  - Move parts
  - Rotate parts

For actors :
+ Add 'puton:FACE' for translation/rotation
For geom : 

