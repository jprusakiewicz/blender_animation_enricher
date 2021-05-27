# Blender automation enricher using python API 🐍

## How to use
Add Blender to env path 
https://docs.blender.org/manual/en/2.93/advanced/command_line/launch/windows.html

loop _.fbx_ file to **idle_loops** folder  
add (one or many) _.fbx_ files to **a_poses** and **b_poses**folder  
Go to **code** folder  
Run `pip install -r requirements.txt`to install dependencies  
Run `python main.py `in console with necessary arguments.

### cli arguments:
to check all arguments type `python main.py --help` in console
##### required:
* A_POSE_NAME- **(str)** name of a_pose .fbx file (without extension)
* IDLE_LOOP_NAME- **(str)** name of idle_loop_animation .fbx / .blend (when --snapped) file

##### optional:
* b_pose_name- **(str)** name of b_pose .fbx file (without extension)
* a_to_idle_blend_length **(int)** (frame) length of blend between (first) a_pose and (main) idle_loop animations (default: 30)
* idle_to_b_blend_length **(int)** (frame) length of blend between (main) idle_loop (third) b_pose animations (default: 30)
* a_pose_frame **(int)** frame to choose pose from a_pose animation (default: 1)
* b_pose_frame **(int)** frame to choose pose from b_pose animation (default: 1)
* --snapped / no_snapped read idle_animation from .blend file (may be used i.e. for snapping bones in blend project) (default: False)

## user configuration 
####There are several parameters user can set in config.py file:

* import_scale - imported _.fbx_ object scale
* animation_group_name - **(only when using --snapped)** animation group to choose from idle_loop animation in blend file

##### All of the following paths are referenced starting from code directory
* core_path - core.py file path  
* target_file_path - .blend file with target object path 
* source_fbx_directory_path - directory path where will be preplaced source .fbx files  
* export_directory_path - directory where will be exported processed .fbx files  
* export_suffix - every exported .fbx file name suffix
   

## Error logs
If there is any error produced by user, preventing code to work properly 
(e.g. wrong user configuration) message will be logged.
Be aware that it doesn't have to lie at the end of output.  


1.0.1 version tested on 2.91.0 Blender version  
Made with 🧠 by Jakub Prusakiewicz