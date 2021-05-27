import logging
import os
import sys

import bpy


def add_to_snapped_animation(import_scale: str, export_directory_path: str, a_pose_path: str,
                             a_to_idle_blend_length: str, idle_to_b_blend_length: str, a_pose_frame: str,
                             b_pose_frame: str, animation_group_name=None, b_pose_path=None):
    idle_loop = bpy.context.scene.collection.all_objects["root"]  # base object name

    # arguments bind
    import_scale = float(import_scale)
    a_to_idle_blend_length = int(a_to_idle_blend_length)
    idle_to_b_blend_length = int(idle_to_b_blend_length)
    a_pose_frame = int(a_pose_frame)
    b_pose_frame = int(b_pose_frame)

    a_pose_file_name = os.path.basename(a_pose_path).strip(".fbx")
    idle_loop_file_name = "snapped"

    if b_pose_path:
        b_pose_file_name = "_" + os.path.basename(b_pose_path).strip(".fbx")
    else:
        b_pose_file_name = ""

    export_name = a_pose_file_name + "_" + idle_loop_file_name + b_pose_file_name

    # import a_pose
    bpy.ops.import_scene.fbx(filepath=a_pose_path)

    bpy.ops.object.mode_set(mode='OBJECT')

    imported_objects = [o for o in bpy.context.selected_objects if o.type == 'ARMATURE']

    if len(imported_objects) > 1:
        logging.error("imported more than one armature!")
        exit()

    a_pose = imported_objects[0]
    bpy.ops.object.select_all(action='DESELECT')

    # try import b_pose
    if b_pose_path:
        bpy.ops.import_scene.fbx(filepath=b_pose_path, global_scale=import_scale)
        bpy.ops.object.mode_set(mode='OBJECT')

        imported_objects = [o for o in bpy.context.selected_objects if o.type == 'ARMATURE']

        if len(imported_objects) > 1:
            logging.error("imported more than one armature!")
            exit()

        b_pose = imported_objects[0]
        b_pose_fcurves = b_pose.animation_data.action.fcurves

    else:
        b_pose_fcurves = a_pose.animation_data.action.fcurves
        b_pose_frame = a_pose_frame

    first_idle_loop_frame = int(idle_loop.animation_data.action.frame_range[0])
    animation_frame_delta = a_to_idle_blend_length - first_idle_loop_frame

    # fcurves
    idle_fcurves = idle_loop.animation_data.action.fcurves
    a_pose_fcurves = a_pose.animation_data.action.fcurves

    for c in reversed(idle_loop.animation_data.action.groups[animation_group_name].channels):
        for k in c.keyframe_points:
            k.co[0] += animation_frame_delta
            k.handle_left[0] += animation_frame_delta
            k.handle_right[0] += animation_frame_delta

    # copy/paste a_pose to idle loop
    try:
        for idle_fc, a_pose_fc in zip(idle_fcurves, a_pose_fcurves):
            idle_fc.keyframe_points.insert(0, a_pose_fc.keyframe_points[a_pose_frame].co.y)
    except IndexError:
        print(f"given a pose frame out of range! frame: {a_pose_frame}")
        exit(1)

    last_idle_loop_frame = idle_loop.animation_data.action.frame_range[1]
    last_frame = last_idle_loop_frame + idle_to_b_blend_length

    # copy/paste b_pose to idle loop
    b_pose_frame_delta = b_pose_frame + first_idle_loop_frame
    try:
        for idle_fc, b_pose_fc in zip(idle_fcurves, b_pose_fcurves):
            idle_fc.keyframe_points.insert(last_frame, b_pose_fc.keyframe_points[b_pose_frame_delta].co.y)
    except IndexError:
        print(f"given b_pose frame out of range! frame: {b_pose_frame_delta}")
        exit(1)

    # key interpolation mode -> bezier
    for f in idle_fcurves:
        for k in f.keyframe_points:
            k.interpolation = 'BEZIER'

    bpy.context.scene.frame_end = last_frame

    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    idle_loop.select_set(True)

    full_export_path = os.path.join(export_directory_path, export_name + ".fbx")
    bpy.ops.export_scene.fbx(filepath=full_export_path, use_selection=True, apply_scale_options="FBX_SCALE_UNITS",
                             object_types={'ARMATURE', 'MESH'}, apply_unit_scale=True, use_mesh_modifiers=True,
                             add_leaf_bones=False, use_armature_deform_only=True,
                             bake_anim=True, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=False,
                             bake_anim_use_all_actions=False, bake_anim_force_startend_keying=False)


if __name__ == "__main__":
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # get all args after "--"
    print(len(argv))
    if len(argv) < 8 or len(argv) > 9:
        logging.critical("wrong parameters count")
        bpy.ops.wm.quit_blender()
        exit(1)

    add_to_snapped_animation(*argv)
