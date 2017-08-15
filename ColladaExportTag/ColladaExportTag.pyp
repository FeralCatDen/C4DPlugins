import os
import c4d
from c4d import bitmaps, plugins, utils

PLUGIN_ID = 1039717

COLLADA_EXPORT_SETTINGS_ENABLE_EXPORT = 1017
COLLADA_EXPORT_SETTINGS_EXTERNAL_TEXTURE = 1018
COLLADA_EXPORT_SETTINGS_TEXTURETYPE = 1019
COLLADA_EXPORT_SETTINGS_TEXTURETYPE_SVG = 1020

class ColladaExport( plugins.TagData ):
    
    def Init( self, node ):
        tag = node

        # Configure default settings
        data = tag.GetDataInstance()
        data.SetBool( COLLADA_EXPORT_SETTINGS_ENABLE_EXPORT, True )
        data.SetBool( COLLADA_EXPORT_SETTINGS_EXTERNAL_TEXTURE, False )
        data.SetInt32( COLLADA_EXPORT_SETTINGS_TEXTURETYPE, COLLADA_EXPORT_SETTINGS_TEXTURETYPE_SVG )
        return True
    
    def Execute( self, tag, doc, op, bt, priority, flags ):
        return c4d.EXECUTIONRESULT_OK

    def GetDEnabling( self, node, id, t_data, flags, itemdesc ):
        if id[ 0 ].id == COLLADA_EXPORT_SETTINGS_TEXTURETYPE:
            return node[ COLLADA_EXPORT_SETTINGS_EXTERNAL_TEXTURE ] == 1
        else: 
            return plugins.NodeData.GetDEnabling( self, node, id, t_data, flags, itemdesc )

if __name__ == "__main__":
    dir, file = os.path.split( __file__ )
    bmp = bitmaps.BaseBitmap()
    bmp.InitWith( os.path.join( dir, "res", "icon.tif" ) )
    plugins.RegisterTagPlugin( 
        id = PLUGIN_ID, 
        str = "COLLADA Export Settings", 
        info = c4d.TAG_EXPRESSION | c4d.TAG_VISIBLE, 
        g = ColladaExport, 
        description = "ColladaExportSettings", 
        icon = bmp 
    )