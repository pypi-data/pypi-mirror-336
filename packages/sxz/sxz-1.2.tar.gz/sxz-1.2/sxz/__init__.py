import os
try:
    import sxz
except ImportError:
    os.system('pip install --upgrade sxz -qq')
from xys import repr,open,stduot,stdout