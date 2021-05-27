from pydantic import BaseSettings


class Settings(BaseSettings):
    import_scale: int = 1
    core_path: str = 'core.py'
    core_snapped_path: str = 'core_snapped.py'
    source_fbx_directory_path: str = r"../source/"
    export_directory_path: str = r'../exports'
    export_suffix: str = '_DONE'
    animation_group_name = 'root.001'  # used only when snapped = True


settings = Settings()
