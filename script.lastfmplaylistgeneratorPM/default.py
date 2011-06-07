

import os
import time 
import xbmc
import xbmcgui
from traceback import print_exc

BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )

process = os.path.join( BASE_RESOURCE_PATH , "pm.pid")
if os.path.exists(process):
    if xbmcgui.Dialog().yesno("Last.FM playlist generator (partymode)", "Would you like to exit partymode?" ):
        os.remove(process)        
else:
    file( process , "w" ).write( "" )
    xbmc.executebuiltin('XBMC.RunScript(%s)' % os.path.join( os.getcwd(), "pm.py" ))