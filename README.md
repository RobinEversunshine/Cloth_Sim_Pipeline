# Cloth_Sim_Pipeline
A CG/Animation pipeline between Houdini and Blender, using Python to manage shots and simulation results. I made this pipline tool to deal with multiple shots requiring cloth & hair simulation in Crash Landing Studio, and also cooperate with other VFX artists & animators.


What this tool does is:

1.Input shot parameters, run the script, it will copy my sim template folder under the shot folder, and export character & camera alembic. It will also output other data, like end frame and resolution to sim .hip file.

2.I have a hda in sim template, which has buttons to open folders (we have folders for sim, blender animation and sim cache), and another button to export sim cache back to the other blender file, then generate a playblast for me to see if anything goes wrong.

3.some object names in blender file is not that accurate, so I wrote some more codes to find them correctly.

4.I made a class of SimJob to let me input a list of shot numbers to generate a few shots' setup and export animation in a row, so I don't have to do them one by one.


Here's my note of this tool if you're interested:

General explanation of the whole pipeline: https://elevated-temples.notion.site/cloth-hair-simulation-pipeline-of-cls

Coding part: https://elevated-temples.notion.site/advanced-level-scripting-in-cloth-sim-pipeline
