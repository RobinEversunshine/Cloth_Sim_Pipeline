import os, subprocess, shutil, json


#import sim to blender
def CommandPostProcess(kwargs):
    node = kwargs["node"]

    #parameters
    lighting_template = node.evalParm("lighting_template")
    blender_executable = node.evalParm("blender_executable")
    blender_script3 = node.evalParm("blender_script3")

    github_path = node.evalParm("github_path")
    blend_file_path = node.evalParm("blend_file_path")
    sim_output_path = node.evalParm("sim_output_path")
    frame_end = node.evalParm("frame_end")
    resolution = [node.evalParm("resolutionx"), node.evalParm("resolutiony")]


    #copy lighting template file to destination
    lighting_dst = rf"{github_path}\lighting.blend"
    shutil.copyfile(lighting_template, lighting_dst)


    #make dictionary parameter
    dict = {
        "blend_file_path" : blend_file_path,
        "sim_output_path" : sim_output_path,
        "frame_end" : frame_end,
        "resolution" : resolution
    }

    dict_json = json.dumps(dict)


    #blender import sim command
    if os.path.isfile(blender_script3):
        bl_command = [blender_executable, lighting_dst, "--background", "--python", blender_script3, "--", dict_json]
        print("Sim import processing...")
        subprocess.run(bl_command, capture_output=True, text=True)

        print("Blender import sim file process done, file saved")
    else:
        raise ValueError("Incorrect script path")

