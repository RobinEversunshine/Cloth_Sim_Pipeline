import os, shutil, subprocess, re, json



##parameters you need to fill in before executing
#github file parameters

# example: F:\Project Files\CLS\github\DD103\shots\20\020\anim.blend
# shot_primary = "20"
# shot_secondary = "020"
# blend_name = "anim"

# example: F:\Project Files\CLS\github\DD103\shots\C_gawrzilla_06\020\06_020.anim.blend
# shot_primary = "C_gawrzilla_06"
# shot_secondary = "020"
# blend_name = "06_020.anim"

shot_primary = "01"
shot_secondary = "020"
blend_name = "anim"
# shot_secondary optional for shorts

#sim file parameters
#DD103, gawrzilla or other shorts
project = "DD103"

#dropbox parameters
prj_name = "DD103"
shot_name = f"{shot_primary}_{shot_secondary}"
# shot_name optional for shorts

#export parameters
frame_start = 950
#blender script will auto detect if there is such model to export,
#but if a character don't have any animation you can set her value to 0.
Ame_anim = 1
Gura_anim = 1
Ina_anim = 1



##one-shot parameters. after setting up correctly on your computer,
#you don't need to edit them again.

#github file parameters
git_path = r"F:\Project Files\CLS\github"
lighting_template = rf"{git_path}\DD103\shots\.lighting.blend"

#sim file parameters
sim_template_folder = r"F:\Project Files\CLS\sim\Cloth_Sim_Template"
sim_prj_path = r"F:\Project Files\CLS\sim"

#blender execute parameters
#your blender.exe path
blender_executable = r"D:\Program Files\Blender Foundation\Blender 4.0\blender.exe"
blender_script = rf"{os.getcwd()}\rop_camera_alembic_in_blender.py"
blender_script2 = rf"{os.getcwd()}\rop_character_alembic_in_blender.py"
blender_script3 = rf"{os.getcwd()}\import_sim_to_blender.py"

#houdini execute parameters
#your houdini python interpreter path
hython_path = r"D:\Program Files\Side Effects Software\Houdini 19.0.383\bin\hython.exe"
houdini_script = rf"{os.getcwd()}\import_parameters_to_houdini.py"



class SimJob():
    #import default parameters
    def __init__(self, shot_primary = shot_primary,
                 shot_secondary = shot_secondary,
                 blend_name = blend_name,
                 project = project,
                 prj_name = prj_name,
                 shot_name = shot_name,
                 frame_start = frame_start,
                 Ame_anim = Ame_anim,
                 Gura_anim = Gura_anim,
                 Ina_anim = Ina_anim):

        self.shot_primary = shot_primary
        self.shot_secondary = shot_secondary
        self.blend_name = blend_name
        self.project = project
        self.prj_name = prj_name
        self.shot_name = shot_name
        self.frame_start = frame_start
        self.Ame_anim = Ame_anim
        self.Gura_anim = Gura_anim
        self.Ina_anim = Ina_anim

        self.makeGithub()
        self.makeSim()
        self.makeDropbox()


    ##make github path
    def makeGithub(self):
        if self.shot_secondary:
            self.github_path = rf"{git_path}\DD103\shots\{self.shot_primary}\{self.shot_secondary}"
        else:
            self.github_path = rf"{git_path}\DD103\shots_pages\{self.shot_primary}"

        self.blend_file_path = rf"{self.github_path}\{self.blend_name}.blend"


        #report error when path doesn't exist
        if not os.path.exists(self.github_path):
            raise ValueError("No such directory")


        #if you don't have the right .blend file name
        while not os.path.isfile(self.blend_file_path):
            #get a list of blend files in such directory
            anim_list = [bfile[:-len(".blend")] for bfile in os.listdir(self.github_path) if bfile.endswith("anim.blend")]

            if len(anim_list) == 1:
                self.new_blend_name = anim_list[0]
                print("No such file. Only one anim file, auto selected.")
            else:
                # input right file name to continue
                print("No such file. Here are all the .blend files in this directory:")
                self.new_blend_name = input("Input right .blend file name to continue:")

            self.blend_file_path = rf"{self.github_path}\{self.new_blend_name}.blend"

        return self.github_path, self.blend_file_path



    ##make sim path
    def makeSim(self):
        if self.shot_secondary:
            self.prj_path = rf"{sim_prj_path}\{self.project}\{self.shot_primary}\{self.shot_secondary}"
        else:
            self.prj_path = rf"{sim_prj_path}\{self.project}\{self.shot_primary}"

        # copy sim templete to project destination if it doesn't exist
        if not os.path.exists(self.prj_path):
            shutil.copytree(sim_template_folder, self.prj_path)

        # alembic output destination
        self.abc_path = self.prj_path + r"\anim_file"

        #make .hip file path
        self.hip_file_path = rf"{self.prj_path}\sim_setup.hip"

        # make path if it doesn't exist
        if not os.path.exists(self.abc_path):
            os.makedirs(self.abc_path)

        return self.prj_path, self.abc_path, self.hip_file_path



    def makeDropbox(self):
        ##make dropbox path
        if self.shot_name:
            self.sim_output_path = rf"S:\_projects\{self.prj_name}\shots\{self.shot_name}\sim"
        else:
            self.sim_output_path = rf"S:\_projects\{self.prj_name}\sim"

        #make path if it doesn't exist
        if not os.path.exists(self.sim_output_path):
            os.makedirs(self.sim_output_path)

        return self.sim_output_path



    def openGithub(self):
        os.startfile(self.github_path)

    def openSim(self):
        os.startfile(self.prj_path)



    #process methods
    def ropCamera(self):
        # make blender dictionary parameter
        blend_dict = {
            "frame_start": self.frame_start,
            "abc_path": self.abc_path,
        }
        blend_dict_json = json.dumps(blend_dict)


        ##blender camera rop alembic command
        bl_command = [blender_executable, self.blend_file_path, "--background", "--python", blender_script, "--", blend_dict_json]
        print(f"Camera export processing for {self.shot_primary} {self.shot_secondary}...")
        result = subprocess.run(bl_command, capture_output=True, text=True)


        # pass variables
        pattern = 'frame_end = (.+)\n.*resolution_x = (\d+)\n.*resolution_y = (\d+)\n.*'
        self.match = re.search(pattern, result.stdout.strip(), re.DOTALL)

        if not self.match:
            raise ValueError("Failed to get end frame or resolution")

        print(f"Blender camera rop alembic process for {self.shot_primary} {self.shot_secondary} done")



    def toHoudini(self):
        # make houdini dictionary parameter
        hou_dict = {
            "github_path": self.github_path,
            "blend_file_path": self.blend_file_path,
            "hip_file_path": self.hip_file_path,
            "sim_output_path": self.sim_output_path,
            "frame_start": self.frame_start,
            "Ame_anim": self.Ame_anim,
            "Gura_anim": self.Gura_anim,
            "Ina_anim": self.Ina_anim,
            "frame_end": int(self.match.group(1)),
            "resolution": [int(self.match.group(2)), int(self.match.group(3))]
        }
        hou_dict_json = json.dumps(hou_dict)


        ##houdini import parameters command
        hou_command = [hython_path, houdini_script, "--", hou_dict_json]
        print(f"Houdini import parameters processing for {self.shot_primary} {self.shot_secondary}...")
        subprocess.run(hou_command)#, capture_output=True, text=True)

        print(f"Houdini import parameters process for {self.shot_primary} {self.shot_secondary} done, file saved")



    def ropCharacter(self):
        blend_dict = {
            "frame_start": self.frame_start,
            "abc_path": self.abc_path,
            "Ame_anim": self.Ame_anim,
            "Gura_anim": self.Gura_anim,
            "Ina_anim": self.Ina_anim
        }
        blend_dict_json = json.dumps(blend_dict)

        ##blender character rop alembic command
        bl_command = [blender_executable, self.blend_file_path, "--background", "--python", blender_script2, "--", blend_dict_json]
        print(f"Character export processing for {self.shot_primary} {self.shot_secondary}...")
        subprocess.run(bl_command, capture_output=True, text=True)

        print(f"Blender character rop alembic process for {self.shot_primary} {self.shot_secondary} done")



    def commandPreProcess(self):
        self.openSim()
        self.ropCamera()
        self.toHoudini()
        self.ropCharacter()




#output paths when executing this script directly
if __name__ == "__main__":
    job = SimJob()
    print(job.github_path)
    print(job.prj_path)
    print(job.sim_output_path)