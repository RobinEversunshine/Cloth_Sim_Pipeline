import bpy
import os, sys, json



#get variables
args = sys.argv
idx = args.index('--') if '--' in args else None

if idx:
    # Read values after '--' in the command line
    dict_json = json.loads(args[idx + 1])
else:
    raise ValueError("no correct input")

blend_file_path = dict_json["blend_file_path"]
sim_output_path = dict_json["sim_output_path"]
frame_end = dict_json["frame_end"]
resolution = dict_json["resolution"]



#dictionary of original hair and cloth objects
orig_dict = {
    "ame_cloth" : "GEO-Ame_clo_proxy",
    "ame_hair" : "GEO-Ame_hair",
    "gura_cloth" : "GEO-Gura_TShirt",
    "gura_hair" : "GEO-Gura_hair",
    "ina_cloth" : "GEO-Ina_dress_proxy",
    "ina_hair" : "GEO-Ina_hair"
}


#dictionary of materials
mat_dict = {
    "ame_cloth" : ["_MAT-ame_clo_indoors"],
    "ame_hair" : ["Ame.hair.r",
                  "Ame.hair_front",
                  "Ame.hair.l",
                  "Ame.hair_solid"],
    "gura_cloth" : ["_MAT-gura_clo_tShirt"],
    "gura_hair" : ["Gura.hair_inner",
                   "Gura.hair_front",
                   "Gura.hair_bang.L",
                   "Gura.hair_back.L",
                   "Gura.hair_bang.R",
                   "Gura.hair_back.R",
                   "Gura.hair_back_inner.R",
                   "Gura.hair_solid"],
    "ina_cloth" : ["_MAT-ina_clo_dress"],
    "ina_hair" : ["ina_hair",
                  "ina_hair_solid",
                  "ina_hair_bangs"]
}



def appendCollection(coll_name):
    bpy.ops.wm.append(
        filepath=rf"{blend_file_path}\Collection\{coll_name}",
        directory=rf"{blend_file_path}\Collection",
        filename=coll_name,
        link=True
    )



#link collection _anim.output from anim.blend
def linkAnimOutput():
    #activate scene collection so .anim.output will be under that
    scene_collection = bpy.context.view_layer.layer_collection
    bpy.context.view_layer.active_layer_collection = scene_collection

    #detect if correct collection name exists in anim blend file
    with bpy.data.libraries.load(blend_file_path) as (data_from, data_to):
        if ".anim.output" in data_from.collections:
            appendCollection(".anim.output")
        elif "_anim.output" in data_from.collections:
            bpy.ops.wm.append(
                filepath=rf"{blend_file_path}\Collection\_anim.output",
                directory=rf"{blend_file_path}\Collection",
                filename="_anim.output",
                link=True
            )
        else:
            for coll in data_from.collections:
                if "anim.output" in coll:
                    appendCollection(coll)
                    break
            else:
                raise ValueError("no correct collection found in anim file")



def overrideCollection():
    linked_coll = None

    if ".anim.output" in bpy.data.collections:
        linked_coll = bpy.data.collections.get(".anim.output")
    else:
        for coll in bpy.data.collections:
            if "anim.output" in coll:
                linked_coll = coll
                break


    if linked_coll and linked_coll.library:
        # create a library override for the collection
        scene = bpy.context.scene
        view_layer = bpy.context.view_layer
        overridden_collection = linked_coll.override_hierarchy_create(scene, view_layer)

        # unlink the original collection
        scene_collection = bpy.context.scene.collection
        scene_collection.children.unlink(linked_coll)



#import sim results and assign materials
def importAlembic(file_name):
    sim_file_path = rf"{sim_output_path}\{file_name}.abc"

    #if sim file doesn't exist
    if not os.path.isfile(sim_file_path):
        return


    bpy.ops.object.select_all(action='DESELECT')

    ## import and activate imported sim object
    bpy.ops.wm.alembic_import(
        filepath = sim_file_path,
        relative_path = False,
        as_background_job = False
    )


    # change name
    obj = bpy.context.active_object
    obj.name = file_name


    ## move to collections
    # get character's collection name
    coll_name = ""

    if "ame" in file_name:
        coll_name = "Ame"
    elif "gura" in file_name:
        coll_name = "Gura"
    elif "ina" in file_name:
        coll_name = "Ina"

    coll = bpy.data.collections[coll_name]

    # unlink from original collection
    for orig_coll in obj.users_collection:
        orig_coll.objects.unlink(obj)

    # move to corresponding collection
    if obj.name not in coll.objects:
        coll.objects.link(obj)


    ## assign materials
    if file_name in mat_dict:
        materials = mat_dict[file_name]

        for i, mat_name in enumerate(materials):
            mat_to_copy = None

            # check if the material exists, if not find it without suffixes
            if mat_name in bpy.data.materials:
                mat_to_copy = bpy.data.materials.get(mat_name)
            else:
                for material in bpy.data.materials:
                    if material.name.startswith(mat_name):
                        mat_to_copy = material
                        break

            # replace certain material slot
            if len(obj.data.materials) > i:
                obj.data.materials[i] = mat_to_copy
            # add a new material slot and assign the material
            else:
                obj.data.materials.append(mat_to_copy)


    #hide original hair or cloth objects
    if file_name in orig_dict:
        orig_name = orig_dict[file_name]

        for object in bpy.context.scene.objects:
            if object.name.startswith(orig_name):
                orig_obj = object
                orig_obj.hide_set(True)
                orig_obj.hide_render = True



def saveFile():
    bpy.ops.wm.save_mainfile()

    # remove auto generated copy file
    template_file = bpy.context.blend_data.filepath + "1"
    if os.path.isfile(template_file):
        os.remove(template_file)



def renderPlayblast():
    #set resolution
    bpy.context.scene.render.resolution_x = resolution[0]
    bpy.context.scene.render.resolution_y = resolution[1]

    #set camera
    bpy.context.scene.camera = bpy.data.objects["CAM-camera"]

    #set render parameters
    bpy.context.scene.render.engine = "BLENDER_WORKBENCH"
    bpy.context.scene.display.shading.light = "STUDIO"
    bpy.context.scene.display.shading.color_type = "TEXTURE"

    #set the output settings
    bpy.context.scene.render.filepath = "//sim_playblast"
    bpy.context.scene.render.image_settings.file_format = "FFMPEG"
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'
    bpy.context.scene.render.ffmpeg.codec = 'H264'

    # save
    saveFile()

    #render the animation sequence
    bpy.ops.render.render(animation=True)



##execute
#link anim file
linkAnimOutput()

#override
overrideCollection()

#import sim
importAlembic("ame_cloth")
importAlembic("ame_hair")

importAlembic("gura_cloth")
importAlembic("gura_hair")

importAlembic("ina_cloth")
importAlembic("ina_hair")

#render playblast
renderPlayblast()