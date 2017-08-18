import c4d, os, sys
from c4d import documents, gui, plugins, utils

# Set up sys.path to import ColladaExport
__currdir__ = os.path.dirname( __file__ )
if __currdir__ not in sys.path:
    sys.path.insert( 0, __currdir__ )
from ColladaExport import ColladaExport


# COLLADA Export Plus Command Plugin
class ColladaExportPlus( plugins.CommandData ):

    PLUGIN_ID = 1039724
    PLUGIN_NAME = "COLLADA Export Plus"
    PLUGIN_HELP = "A Better COLLADA Exporter."
    PLUGIN_INFO = 0
    PLUGIN_ICON = None

    dialog = None

    def Execute( self, doc ):

        if self.dialog is None:
            self.dialog = ColladaExportPlusDialog()

        # Get a path to save the exported file
        self.dialog.filePath = c4d.storage.LoadDialog( title = 'Save File for COLLADA Export', flags = c4d.FILESELECT_SAVE, force_suffix = 'dae' )

        # Exit if the user cancels the file dialog
        if self.dialog.filePath is None:
            return True

        # Open the export settings dialog window
        return self.dialog.Open( dlgtype = c4d.DLG_TYPE_ASYNC, pluginid = self.PLUGIN_ID, defaultw = 250, defaulth = 250 )


    def RestoreLayout( self, secRef ):

        if self.dialog is None:
            self.dialog = ColladaExportPlusDialog()

        return self.dialog.Restore( pluginid = self.PLUGIN_ID, secret = secRef )


    def Register( self ):
        return c4d.plugins.RegisterCommandPlugin( self.PLUGIN_ID, self.PLUGIN_NAME,
            self.PLUGIN_INFO, self.PLUGIN_ICON, self.PLUGIN_HELP, self )


# Main dialog window for the COLLADA exporter
class ColladaExportPlusDialog( gui.GeDialog ):

    BUTTON_OK = 1
    BUTTON_CANCEL = 2

    DLG_COLLADAEXPORTPLUSSETTINGS = 10000
    COLLADAEXPORT_ANIMATION = 1000
    COLLADAEXPORT_EMPTY_NULLS = 1001
    COLLADAEXPORT_REMOVE_XREFS = 1002
    COLLADAEXPORT_REMOVE_TEXTURE_TAGS = 1003

    filePath = None

    def CreateLayout( self ):
        return self.LoadDialogResource( self.DLG_COLLADAEXPORTPLUSSETTINGS )


    def InitValues( self ): 
        self.SetBool( self.COLLADAEXPORT_ANIMATION, True )
        self.SetBool( self.COLLADAEXPORT_EMPTY_NULLS, True )
        self.SetBool( self.COLLADAEXPORT_REMOVE_XREFS, True )
        self.SetBool( self.COLLADAEXPORT_REMOVE_TEXTURE_TAGS, True )
        return True


    def Command( self, id, msg ):

        # Close dialog window on cancel button click
        if id == self.BUTTON_CANCEL:
            self.Close()
            return True

        # Run the exporter on ok button click
        if id == self.BUTTON_OK:
            exporter = ColladaExport()
            result = exporter.Execute(
                self.filePath,
                self.GetBool( self.COLLADAEXPORT_ANIMATION ), 
                self.GetBool( self.COLLADAEXPORT_EMPTY_NULLS ), 
                self.GetBool( self.COLLADAEXPORT_REMOVE_XREFS ),
                self.GetBool( self.COLLADAEXPORT_REMOVE_TEXTURE_TAGS )
            )

            c4d.EventAdd()
            gui.MessageDialog( result )
            self.Close()
            
        return True


# Loads a c4d.bitmaps.BaseBitmap by name relative to the plugins
# containing directory and returns it. None is returned if the bitmap
# could not be loaded.
def load_icon( fn ):
    fn = os.path.join( os.path.dirname( __file__ ), fn )
    bmp = c4d.bitmaps.BaseBitmap()
    if bmp.InitWith( fn )[ 0 ] == c4d.IMAGERESULT_OK:
        return bmp
    return None


def main():
  ColladaExportPlus().Register()

if __name__ == "__main__":
  main()
