import os
from pathlib import Path

from git import Repo
from pydantic import BaseModel, model_validator


class DoubletParameters(BaseModel):
    use_stimulation: bool = False
    use_heat_pump: bool = False
    hp_minimum_injection_temperature: float = 15
    max_cooling_temperature_range: float = 100
    stimKhMax: float = 20
    return_temperature: float = 30
    surface_temperature: float = 10
class Config(BaseModel):
    input_data_path: Path | None
    results_path: Path | None

    DoubletParameters : DoubletParameters


    @model_validator(mode="after")
    def set_paths(self):
        if not self.output_path:
            repo_path = Path(Repo(".", search_parent_directories=True).working_tree_dir)
            self.output_path = repo_path / "models" / self.model_name
        return self
