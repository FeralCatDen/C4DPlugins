import c4d, os
from c4d import bitmaps, plugins, utils

PLUGIN_ID = 1039717

class ColladaExport( plugins.TagData ):
    
    def Init( self, node ):
        tag = node

        # Configure default settings
        data = tag.GetDataInstance()
        data.SetBool( c4d.COLLADA_EXPORT_SETTINGS_ENABLE_EXPORT, True )
        
        return True
    

    def Execute( self, tag, doc, op, bt, priority, flags ):
        return c4d.EXECUTIONRESULT_OK


if __name__ == "__main__":
    dir, file = os.path.split( __file__ )
    bmp = bitmaps.BaseBitmap()
    bmp.InitWith( os.path.join( dir, "res", "icon.tif" ) )
    plugins.RegisterTagPlugin( 
        id = PLUGIN_ID, 
        str = "COLLADA Export Settings", 
        info = c4d.TAG_VISIBLE, 
        g = ColladaExport, 
        description = "ColladaExportSettings", 
        icon = bmp 
    )