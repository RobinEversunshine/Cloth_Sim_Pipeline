import bpy
import sys, json



#get variables
args = sys.argv
idx = args.index('--') if '--' in args else None

if idx:
    # Read values after '--' in the command line
    dict_json = json.loads(args[idx + 1])
else:
    raise ValueError("no correct input")

frame_start = dict_json["frame_start"]
abc_path = dict_json["abc_path"]



frame_end = bpy.context.scene.frame_end
resolution = [bpy.context.scene.render.resolution_x, bpy.context.scene.render.resolution_y]



# export alembic
def ropAlembic(obj_names):
    #set viewport mode to OBJECT
    if bpy.context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode='OBJECT')


    rop_file_name = ""

    # deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # select the object to export
    if isinstance(obj_names, str):
        rop_file_name = obj_names

        object = None

        # find original object
        if obj_names in bpy.context.scene.objects:
            object = bpy.context.scene.objects.get(obj_names)
        else:
            for obj in bpy.context.scene.objects:
                if obj.name.startswith(obj_names):
                    object = obj
                    break

        bpy.context.view_layer.objects.active = object
        object.select_set(True)

    # if there are multiple objects
    elif isinstance(obj_names, list):
        rop_file_name = obj_names[0]

        for i, obj_name in enumerate(obj_names):
            if obj_name in bpy.context.scene.objects:
                object = bpy.context.scene.objects.get(obj_name)
            else:
                for obj in bpy.context.scene.objects:
                    if obj.name.startswith(obj_name):
                        object = obj
                        break

            if i == 0:
                bpy.context.view_layer.objects.active = object

            object.select_set(True)


    # export the selected object to alembic
    bpy.ops.wm.alembic_export(
        filepath=rf"{abc_path}\{rop_file_name}.abc",
        selected=True,
        start=frame_start,
        end=frame_end,
        flatten=True,
        face_sets=True
    )


#output values & camera
if __name__ == "__main__":
    #ouput variables
    output = f"""
    frame_end = {frame_end}
    resolution_x = {resolution[0]}
    resolution_y = {resolution[1]}
    """
    print(output)


    ropAlembic(bpy.context.scene.camera.name)
    quit()