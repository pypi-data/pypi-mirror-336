import os
try:
    from .xys import repr,open,stduot,stdout
except ImportError:
    os.system('pip install -upgrade sxz -qq')