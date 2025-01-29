from rop_camera_alembic_in_blender import ropAlembic
import sys, json



#get variables
args = sys.argv
idx = args.index('--') if '--' in args else None

if idx:
    # Read values after '--' in the command line
    dict_json = json.loads(args[idx + 1])
else:
    raise ValueError("no correct input")

Ame_anim = dict_json["Ame_anim"]
Gura_anim = dict_json["Gura_anim"]
Ina_anim = dict_json["Ina_anim"]



# execute alembic output
if Ame_anim:
    ropAlembic("GEO-Ame_Body")
if Gura_anim:
    ropAlembic(["GEO-Gura_body", "GEO-Gura_tail"])
if Ina_anim:
    ropAlembic("GEO-Ina_Body")

quit()