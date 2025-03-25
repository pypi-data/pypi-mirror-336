'''
Created on 24 déc. 2022

@author: olivier

Strings utility module for syntax conversions.
Usually needed by GUI or interaction with libreoffice or Microsoft XL

'''
def ColToLetter(n:int):
  ''' Convert an integer into an XL/LibreOffice column's letter. '''
  s = chr(0x41 + (n % 26))
  n = int(n // 26)
  while n > 26:
    s = chr(0x40 + (n % 26)) + s
    n = int(n // 26)

  if n >= 1:
    s = chr(0x40 + n) + s

  return s




def toPyVect(*arg):
  '''
  Convert a set of cells into a Python tuple (A, Y, z)
  Where values can be either strings or floats with a '.' decimal separator
  '''
  res = ''
  for a in arg:
    # print(f'Arg = {a}')
    if isinstance(a, tuple):
      if len(a)>=1 and isinstance(a[0], tuple):
        # Linearize a 2D table
        res += ''.join( [ str(v)+', ' for t in a for v in t ] )
      else:
        res += ''.join( [ str(v)+', ' for v in a ] )

    else:  # The argument is not a tuple : either a float or a string
      res += f'{a}, '
  return f'({res})'

  
def toPyTuple2(*arg):
  '''
  Convert a sheet selection of vectors or tables or individual values
  into a list of tuples (key, val)
  '''
  prevSingle, prevVector, prevVal = False, False, None

  res = ''
  for tno, a in enumerate(arg):
    # print(f'Arg#{tno} = {a}')
    if isinstance(a, tuple):
      if prevSingle:
        # Illegal case: Previous value was a single value
        # and can not be followed by a table
        return "Single Value Alone in arg #{tno}"
    
      if isinstance(a[0], tuple):
        if prevSingle:
          return f'Mix of vectors and values for arg #{tno}'
      
        if len(a)==2: # Horizontal selection
          res += ''.join( [ f'({v}, {a[1][i]}), ' for i, v in enumerate(a[0]) ])
          continue

        if len(a[0])==1: # Selection in a list of one element list --> Another Vector Case
          # Convert input in a real 1D vector
          a = [ t[0] for t in a ]

        elif len(a[0])==2: # Vertical selection
          res += ''.join( [ f'{v}, ' for v in a ] )
          continue

        elif len(a)==1:
          a = a[0]

        else: # Error
          return f'Bad Dimension for arg #{tno}'

      #else: # Vector case
      if prevVector:
        prevVector = False
          
        # Check if vector lengths are equal
        if len(a)==len(prevVal):
          res += ''.join( [ f"{t}, " for t in zip(prevVal,a) ] )
        else:
          return f'Unmatched vectors for arg #{tno}'

      else: # Found a first 1D vector
        prevVector = True
        prevVal = a
        #print('Prev Vector:' + str(a))

    else: #Single value - Must be paired with another single value
      if prevSingle:
        prevSingle = False
        res += f"({prevVal}, {a}), "
      else:
        prevSingle = True
        prevVal = a

  return f'({res})'

def byte2Human(deltam):
  return f"{deltam} B" if deltam<1024 else (f"{deltam>>10} kBi" if deltam<1048576 else f"{deltam>>20} MBi")


def readBool(s):
  '''
  Read a boolean from a cmdLgn source
  Return the boolean or False if empty
  '''
  if isinstance(s, str):
    s = s.strip()
    return (s=='1') or (s.lower()=='true')

  return s and (s==1.0)

def readInt(s, defaultValue=None):
  '''
  Read an int from a cmdLgn source
  Return the int or 0 if empty and no default value given
  '''
  if isinstance(s, str):
    s = s.strip()

  i = 0
  if s:
    i = int(s)
  elif defaultValue!=None:
    i = defaultValue
    
  return i

def readFloat(s, defaultValue=None):
  '''
  Read a float from a cmdLgn source.
  Return the float or 0.0 if empty and no default value given 
    else the default value 
  '''
  f = 0.0
  if isinstance(s, str):
    s = s.strip()

  if s:
    try:
      # Manage ValueError
      f = float(s)
    except ValueError as ve:
      # Could be a 'comma' issue
      if s.find(','):
        f = float(s.replace(',', '.'))
      else:
        raise ve
  elif defaultValue!=None:
    f = defaultValue
    
  return f


