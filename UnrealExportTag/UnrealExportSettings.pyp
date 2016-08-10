import os

import c4d
from c4d import bitmaps, plugins, utils

PLUGIN_ID = 1000001

UE_EXPORT = 1016

class UnrealExport(plugins.TagData):
    
    def Init(self, node):
        tag = node
        data = tag.GetDataInstance()

        data.SetBool(UE_EXPORT, True)

        pd = tag[c4d.EXPRESSION_PRIORITY]
        if pd is not None:
            pd.SetPriorityValue(c4d.PRIORITYVALUE_CAMERADEPENDENT, True)
            tag[c4d.EXPRESSION_PRIORITY] = pd
        
        return True
    
    def Execute(self, tag, doc, op, bt, priority, flags):
        return c4d.EXECUTIONRESULT_OK

if __name__ == "__main__":
    dir, file = os.path.split(__file__)
    bmp = bitmaps.BaseBitmap()
    bmp.InitWith(os.path.join(dir, "res", "icon.tif"))
    plugins.RegisterTagPlugin(id=PLUGIN_ID, str="Unreal Export Settings", info=c4d.TAG_EXPRESSION|c4d.TAG_VISIBLE, g=UnrealExport, description="UnrealExportSettings", icon=bmp)