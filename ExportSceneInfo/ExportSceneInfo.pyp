import c4d
import os
import json

from c4d import plugins, documents, gui, utils

PLUGIN_ID = 1039716

MISSING_MATERIAL = "MISSING MATERIAL"

def vectorToArray(v):
	return [v[0], v[1], v[2]]

class SceneInfoSaver(plugins.SceneSaverData):

	def Save(self, node, name, doc, filterflags):

		def _recurseHierarchy(op, sceneStack, *parent):
			while op:
				# Names with "::" in them are internal objects derived from xrefs. 
				# Since the xrefs will be replaced when importing into UE4, 
				# their internals don't need to be exported here.
				if "::" in op.GetName():
					break

				print "%s: %s" % (op.GetName(), type(op).__name__)

				origRotationOrder = op[c4d.ID_BASEOBJECT_ROTATION_ORDER]
				origRotation = op.GetRelRot()
				op[c4d.ID_BASEOBJECT_ROTATION_ORDER] = 4

				# Serialize basic properties
				entry = {}
				entry['name'] = op.GetName()
				entry['uid'] = op.GetGUID()
				entry['type'] = type(op).__name__
				entry['position'] = vectorToArray(op.GetRelPos())
				entry['scale'] = vectorToArray(op.GetRelScale())
				entry['rotation'] = vectorToArray(op.GetRelRot())
				entry['materials'] = []
				entry['children'] = []

				op[c4d.ID_BASEOBJECT_ROTATION_ORDER] = origRotationOrder
				op.SetRelRot(origRotation)

				# Serialize material tags
				for tag in op.GetTags():
					if type(tag) is c4d.TextureTag:
						targetMaterial = tag.GetMaterial()
						entryMaterial = {}

						if targetMaterial:
							entryMaterial['name'] = targetMaterial.GetName()
						else:
							entryMaterial['name'] = MISSING_MATERIAL

						entry['materials'].append(entryMaterial)

				if parent:
					parent[0]['children'].append(entry)
				else:
					sceneStack.append(entry)

				_recurseHierarchy(op.GetDown(), sceneStack, entry)
				op = op.GetNext()

		def _writeProcess(doc, fn, sceneStack):
			try:
				f = open(name, "w")
			except IOError, e:
				return c4d.FILEERROR_OPEN
				
			f.write(json.dumps(sceneStack, indent=4))

			try:
				f.close()
			except IOError, e:
				return c4d.FILEERROR_CLOSE

			return c4d.FILEERROR_NONE
		
		sceneStack = []
		sceneStack.append({})
		sceneStack[0]['actors'] = []
		_recurseHierarchy(doc.GetFirstObject(), sceneStack[0]['actors'])
		
		state = _writeProcess(doc, name, sceneStack)
		return state


if __name__=='__main__':
	plugins.RegisterSceneSaverPlugin(id=PLUGIN_ID, str="Genesis Noir Scene (*.gns)", info=0, g=SceneInfoSaver, description="", suffix="gns")