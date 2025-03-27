from typing import Union, List, Dict
from pathlib import Path
from utils import download_from_github
from .arc import Task


class ARC1:
    def __init__(
        self, dataset_path: Union[str, Path], train: bool = True, download: bool = True
    ):
        self._tasks: List[Task] = list()
        self._tasks_map: Dict[str, int] = dict()
        self._dataset_path = (
            dataset_path if isinstance(dataset_path, Path) else Path(dataset_path)
        )
        self._train = train

        if download:
            self.download()

        self.load()

    def load(self):
        if not self.dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset path '{self._dataset_path}' does not exist. "
            )
        if self.dataset_path.is_dir():
            raise NotADirectoryError(
                f"Dataset path '{self._dataset_path}' is not a directory. "
            )

        for file_path in self._dataset_path.glob("*.json"):
            task = Task.from_json(file_path)
            self._tasks.append(task)

    def download(self):
        download_from_github(
            "fchollet",
            "ARC-AGI",
            f"data/{'training' if self._train else 'evaluation'}",
            "main",
            self._dataset_path,
        )

    def __contains__(self, task_id: str) -> bool:
        return any(task.task_id == task_id for task in self._tasks)

    def get(self, task_id: str) -> Task:
        if task_id not in self:
            raise KeyError(f"Task with task id: {task_id} is not in this dataset. ")
        return next((task for task in self._tasks if task.task_id == task_id), None)

    def __getitem__(self, i: int) -> Task:
        return self._tasks[i]

    def __len__(self) -> int:
        return len(self._tasks)


class ARC2(ARC1):
    def download(self):
        download_from_github(
            "arcprize",
            "ARC-AGI-2",
            f"data/{'training' if self._train else 'evaluation'}",
            "main",
            self._dataset_path,
        )
