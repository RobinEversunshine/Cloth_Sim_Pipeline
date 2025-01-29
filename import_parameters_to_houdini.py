import hou
import sys, json
from ScriptParameters import lighting_template, blender_executable



#get variables
args = sys.argv
idx = args.index('--') if '--' in args else None

if idx:
    # Read values after '--' in the command line
    dict_json = json.loads(args[idx + 1])
else:
    raise ValueError("no correct input")

github_path = dict_json["github_path"]
blend_file_path = dict_json["blend_file_path"]
hip_file_path = dict_json["hip_file_path"]
sim_output_path = dict_json["sim_output_path"]
Ame_anim = dict_json["Ame_anim"]
Gura_anim = dict_json["Gura_anim"]
Ina_anim = dict_json["Ina_anim"]
frame_start = dict_json["frame_start"]
frame_end = dict_json["frame_end"]
resolution = dict_json["resolution"]



#parameters
parm_dict = {
    "lighting_template" : lighting_template,
    "blender_executable" : blender_executable,
    "frame_end" : frame_end,
    "resolution" : resolution,

    "github_path" : github_path,
    "blend_file_path" : blend_file_path,
    "sim_output_path" : sim_output_path,
    "ame_anim" : Ame_anim,
    "gura_anim" : Gura_anim,
    "ina_anim" : Ina_anim
}



#load file
hou.hipFile.load(hip_file_path)

#update frame range
hou.playbar.setFrameRange(975, frame_end)

#update camera & resolution
hou.node('/obj/Alembic_camera').parm("buildHierarchy").pressButton()
cam = hou.node('/obj/Alembic_camera/CAM-camera/data_CAM-camera')
cam.parm("resx").set(resolution[0])
cam.parm("resy").set(resolution[1])

#set parameters on node
prj_node = hou.node("/obj/SIM/CLS_PRJ")
if prj_node:
    prj_node.setParms(parm_dict)
else:
    raise ValueError("cannot find CLS_PRJ node")

#save file
hou.hipFile.save()