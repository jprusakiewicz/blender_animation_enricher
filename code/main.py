import os
from pathlib import Path

import typer
from config import settings


# def get_all_fbx_files(dir_path: str) -> List[str]:
#     fbx_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(".fbx")]
#     return fbx_files


def main(a_pose_name: str, idle_loop_name: str, b_pose_path: str = None, a_to_idle_blend_length: int = 30,
         idle_to_b_blend_length: int = 30, a_pose_frame: int = 1, b_pose_frame: int = 1):

    # region files validation
    idle_loops_path = os.path.join(settings.source_fbx_directory_path, "idle_loops", idle_loop_name+ ".fbx")
    a_poses_path = os.path.join(settings.source_fbx_directory_path, "a_poses", a_pose_name+ ".fbx")
    if b_pose_path:
        b_poses_path = os.path.join(settings.source_fbx_directory_path, "b_poses", b_pose_path+ ".fbx")
        c = Path(b_poses_path)

    # all_idle_loops = get_all_fbx_files(idle_loops_path)
    # all_a_poses = get_all_fbx_files(a_poses_path)
    # all_b_poses = get_all_fbx_files(b_poses_path)
    a = Path(idle_loops_path)
    print(a)
    print(a.is_file())

    b = Path(a_poses_path)
    print(b)
    print(b.is_file())

    print(1)
    # endregion

if __name__ == "__main__":
    typer.run(main)
