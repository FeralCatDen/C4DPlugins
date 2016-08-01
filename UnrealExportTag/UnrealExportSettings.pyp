import os

import c4d
from c4d import bitmaps, plugins, utils

PLUGIN_ID = 1000001

UE_EXPORT = 1016

class UnrealExport(plugins.TagData):
    
    def Init(self, node):
        tag = node
        data = tag.GetDataInstance()
        
        data.SetBool(c4d.UE_EXPORT, True)

        pd = tag[c4d.EXPRESSION_PRIORITY]
        if pd is not None:
            pd.SetPriorityValue(c4d.PRIORITYVALUE_CAMERADEPENDENT, True)
            tag[c4d.EXPRESSION_PRIORITY] = pd
        
        return True
    
    def Execute(self, tag, doc, op, bt, priority, flags):
        # bd = doc.GetRenderBaseDraw()
        # if bd is None: return c4d.EXECUTIONRESULT_OK
        # data = tag.GetDataInstance()
        # if data is None: return c4d.EXECUTIONRESULT_OK
        
        # cp = bd.GetSceneCamera(doc)
        # if cp is None: cp = bd.GetEditorCamera()
        # if cp is None: return c4d.EXECUTIONRESULT_OK

        # local = cp.GetMg().off * (~(op.GetUpMg() * op.GetFrozenMln())) - op.GetRelPos()
        # hpb = utils.VectorToHPB(local)
        
        # if not data.GetBool(c4d.UE_EXPORT):
        #     hpb.y = op.GetRelRot().y
        
        # hpb.z = op.GetRelRot().z

        # op.SetRelRot(hpb)
        
        return c4d.EXECUTIONRESULT_OK


if __name__ == "__main__":
    dir, file = os.path.split(__file__)
    bmp = bitmaps.BaseBitmap()
    bmp.InitWith(os.path.join(dir, "res", "icon.tif"))
    plugins.RegisterTagPlugin(id=PLUGIN_ID, str="Unreal Export Settings", info=c4d.TAG_EXPRESSION|c4d.TAG_VISIBLE, g=UnrealExport, description="UnrealExportSettings", icon=bmp)