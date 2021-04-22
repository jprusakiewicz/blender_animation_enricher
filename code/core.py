import logging
import sys

import bpy


def add_poses_to_animation(import_scale: str, export_path: str, a_pose_path: str, idle_loop_fbx_path: str,
                           a_to_idle_blend_length: str, idle_to_b_blend_length: str, a_pose_frame: str,
                           b_pose_frame: str,
                           b_pose_path=None):
    # arguments bind

    import_scale = float(import_scale)
    a_to_idle_blend_length = int(a_to_idle_blend_length)
    idle_to_b_blend_length = int(idle_to_b_blend_length)
    a_pose_frame = int(a_pose_frame)
    b_pose_frame = int(b_pose_frame)

    bpy.ops.import_scene.fbx(filepath=idle_loop_fbx_path, global_scale=import_scale)

    bpy.ops.object.mode_set(mode='OBJECT')

    imported_objects = [o for o in bpy.context.selected_objects if o.type == 'ARMATURE']

    if len(imported_objects) > 1:
        logging.error("imported more than one armature!")
        exit()

    idle_loop = imported_objects[0]

    bpy.ops.object.select_all(action='DESELECT')

    bpy.ops.import_scene.fbx(filepath=a_pose_path)

    bpy.ops.object.mode_set(mode='OBJECT')

    imported_objects = [o for o in bpy.context.selected_objects if o.type == 'ARMATURE']

    if len(imported_objects) > 1:
        logging.error("imported more than one armature!")
        exit()

    a_pose = imported_objects[0]

    # fcurves
    idle_fcurves = idle_loop.animation_data.action.fcurves

    a_pose_fcurves = a_pose.animation_data.action.fcurves

    for f in reversed(idle_fcurves):
        for k in f.keyframe_points:
            k.co[0] += a_to_idle_blend_length
            k.handle_left[0] += a_to_idle_blend_length
            k.handle_right[0] += a_to_idle_blend_length

    # copy/paste a_pose to idle loop
    try:
        for idle_fc, a_pose_fc in zip(idle_fcurves, a_pose_fcurves):
            idle_fc.keyframe_points.insert(0, a_pose_fc.keyframe_points[a_pose_frame].co.y)
    except IndexError:
        print(f"given a pose frame out of range! frame: {a_pose_frame}")
        exit(1)


if __name__ == "__main__":
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # get all args after "--"
    print(len(argv))
    if len(argv) < 8 or len(argv) > 9:
        logging.critical("wrong parameters count")
        bpy.ops.wm.quit_blender()
        exit(1)

    add_poses_to_animation(*argv)
