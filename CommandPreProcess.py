from ScriptParameters import SimJob



#one shot
# job = SimJob()
# job.commandPreProcess()

shots = '''


13_050


'''






#multiple shots
# shot_secondary_list = ["010", "020", "030", "040", "060", "070", "080"]


for shot in shots.split():
    if shot:
        shot_pri = shot.split("_")[0]
        shot_sec = shot.split("_")[1]
        print(shot_pri)
        print(shot_sec)

        job = SimJob(shot_primary=shot_pri, shot_secondary=shot_sec, shot_name=f"{shot_pri}_{shot_sec}")
        job.commandPreProcess()
        print("\n\n/////////////////////////////////////////////////////////////////////////////////\n\n")




# for sec in shot_secondary_list:
#     job = SimJob(shot_primary = "01", shot_secondary = sec, shot_name = f"03_{sec}")
#     job.commandPreProcess()
#     print("\n\n/////////////////////////////////////////////////////////////////////////////////\n\n")


