import json
import os
import subprocess
from pathlib import Path
from typing import Optional

import typer

from config import settings


def log_subprocess_output(subprocess_result: subprocess.CompletedProcess, encoding='utf-8'):
    for line in subprocess_result.stdout.splitlines():
        print(str(line, encoding))  # feel free changing to logging.log()


def main(a_pose_name: str, idle_loop_name: str, b_pose_name: str = None, a_to_idle_blend_length: int = 30,
         idle_to_b_blend_length: int = 30, a_pose_frame: int = 1, b_pose_frame: int = 1, snapped: bool = False,
         a_pose_range: Optional[int] = None, b_pose_range: Optional[int] = None):
    if snapped:
        idle_loops_path = os.path.join(settings.source_fbx_directory_path, "idle_loops", idle_loop_name + ".blend")
    else:
        idle_loops_path = os.path.join(settings.source_fbx_directory_path, "idle_loops", idle_loop_name + ".fbx")
    idle = Path(idle_loops_path)
    if not idle.is_file():
        print(f"no such file {idle}")
        exit(1)

    a_pose_path = os.path.join(settings.source_fbx_directory_path, "a_poses", a_pose_name + ".fbx")
    a_pose = Path(a_pose_path)
    if not a_pose.is_file():
        print(f"no such file {a_pose}")
        exit(1)

    configuration = dict(idle_loop_fbx_path=idle_loops_path,
                         import_scale=settings.import_scale, export_directory_path=settings.export_directory_path,
                         a_pose_path=a_pose_path, a_to_idle_blend_length=a_to_idle_blend_length,
                         idle_to_b_blend_length=idle_to_b_blend_length,
                         a_pose_frame=a_pose_frame, b_pose_frame=b_pose_frame,
                         animation_group_name=settings.animation_group_name, a_pose_range=a_pose_range,
                         b_pose_range=b_pose_range)

    if b_pose_name:
        b_pose_path = os.path.join(settings.source_fbx_directory_path, "b_poses", b_pose_name + ".fbx")
        b_pose = Path(b_pose_path)
        if not b_pose.is_file():
            print(f"no such file {b_pose}")
            exit(1)
        configuration['b_pose_path'] = b_pose_path

    if snapped:
        configuration_json = json.dumps(configuration)
        command = ['Blender', idle_loops_path, '--background', '--python', settings.core_snapped_path, "--",
                   configuration_json]

    else:
        configuration[idle_loops_path] = idle_loops_path
        configuration_json = json.dumps(configuration)
        command = ['Blender', '--background', '--python', settings.core_path, "--", configuration_json]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            cwd=os.path.dirname(os.path.realpath(__file__)))
    log_subprocess_output(result)


if __name__ == "__main__":
    typer.run(main)
