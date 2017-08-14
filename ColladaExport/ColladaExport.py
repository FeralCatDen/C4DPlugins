import c4d

from c4d import plugins, documents, storage, gui

colladaPluginId = 1025755
noExportFlag = 'NO_EXPORT'
nullTypeName = 'Null'
xrefTypeName = 'XRef'

xrefCounter = 0
polyCounter = 0
docCopy = None

def main():

	global docCopy 

	c4d.StopAllThreads()

	# Get the COLLADA export plugin
	colladaPlugin = plugins.FindPlugin( colladaPluginId, c4d.PLUGINTYPE_SCENESAVER )
	if colladaPlugin is None:
		gui.MessageDialog( 'Cannot find COLLADA (.dae) exporter. Check the plugin ID.' );
		return

	# Get a path to save the exported file
	filePath = c4d.storage.LoadDialog( title = 'Save File for COLLADA Export', flags = c4d.FILESELECT_SAVE, force_suffix = 'dae' )

	if filePath is None:
		return

	# Clone the current document so the modifications aren't applied to the original scene
	docCopy = doc.GetClone( c4d.COPYFLAGS_DOCUMENT )

	# Remove xrefs
	RemoveXRefs( docCopy.GetFirstObject() )

	# Remove objects that are on non-exporting layers
	RemoveNonExporting( docCopy.GetFirstObject() )

	# Add empty polygon objects to childless null objects so that they are exported by the
	# COLLADA exporter
	FixUpEmptyNulls( docCopy.GetFirstObject() )

	# Container for plugin object data
	op = {}

	# Configure COLLADA export plugin and export the modified scene
	if colladaPlugin.Message( c4d.MSG_RETRIEVEPRIVATEDATA, op ):
		if 'imexporter' not in op:
			gui.MessageDialog( 'There was an error with the COLLADA exporter.' )
			return

		# Get the exporter settings from the plugin object
		colladaExport = op[ 'imexporter' ]
		if colladaExport is None:
			gui.MessageDialog( 'There was an error with the COLLADA exporter.' )
			return

		# Define the settings
		colladaExport[ c4d.COLLADA_EXPORT_ANIMATION ] = True
		colladaExport[ c4d.COLLADA_EXPORT_TRIANGLES ] = True
		
		# Export without the dialog
		if c4d.documents.SaveDocument( docCopy, filePath, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, colladaPluginId ):
			gui.MessageDialog( 'Export complete\n\nRemoved %d xrefs\nAdded %d polygon objects' % ( xrefCounter, polyCounter ) )
		else:
			gui.MessageDialog( 'The document failed to save.' );
			return

		c4d.EventAdd()

	else:
		gui.MessageDialog( 'There was an error with the COLLADA exporter.' )


def RemoveXRefs( op ): 

	global xrefCounter

	while op:

		# Names with "::" in them are internal objects derived from xrefs. 
		# Since the xrefs will be replaced when importing into js,
		# their internals don't need to be exported here.
		if '::' in op.GetName():
			break

		if xrefTypeName in op.GetTypeName():
			xrefCounter += 1
			op.Remove()
			break

		# Recurse thru the hierarchy
		RemoveXRefs( op.GetDown() )
		op = op.GetNext()


def RemoveNonExporting( op ):

	global docCopy

	while op:

		remove = False

		# Remove if render display mode is off
		if op.GetRenderMode() is c4d.MODE_OFF:
			remove = True

		# Remove if editor display mode is off 
		if op.GetEditorMode() is c4d.MODE_OFF:
			remove = True

		# Remove if the object is in a layer that contains the no-export flag
		if op.GetLayerObject( docCopy ) is not None:
			if noExportFlag in op.GetLayerObject( docCopy ).GetName():
				remove = True

		if remove is True:
			op.Remove()
			break

		# Recurse thru the hierarchy
		RemoveNonExporting( op.GetDown() )
		op = op.GetNext()


def FixUpEmptyNulls( op ):

	global polyCounter

	while op:

		# Add empty polygon objects to any null nodes with no children, so 
		# that they are exported by the COLLADA exporter correctly.
		if nullTypeName in op.GetTypeName():
			if len( op.GetChildren() ) == 0:
				polyOp = c4d.PolygonObject( 0, 0 )
				polyOp.InsertUnder( op )
				polyCounter += 1

		# Recurse thru the hierarchy
		FixUpEmptyNulls( op.GetDown() )
		op = op.GetNext()


if __name__ == '__main__':
	main()