from git import Repo
from pathlib import Path

def get_repo_root(path=".") -> Path:
    repo = Repo(path, search_parent_directories=True)
    return Path(repo.git.rev_parse("--show-toplevel"))