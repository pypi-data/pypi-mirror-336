from enum import Enum
from typing import List, Union, Dict, Tuple, Self, Optional, Literal
import numpy as np
import json
from pathlib import Path
from utils import Layout
import warnings


class COLOR(Enum):
    ZERO = 0  # Background
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9


class Grid:
    PALETTE: Dict[COLOR, str] = {
        COLOR.ZERO: "\033[48;5;0m  \033[0m",
        COLOR.ONE: "\033[48;5;20m  \033[0m",
        COLOR.TWO: "\033[48;5;124m  \033[0m",
        COLOR.THREE: "\033[48;5;10m  \033[0m",
        COLOR.FOUR: "\033[48;5;11m  \033[0m",
        COLOR.FIVE: "\033[48;5;7m  \033[0m",
        COLOR.SIX: "\033[48;5;5m  \033[0m",
        COLOR.SEVEN: "\033[48;5;208m  \033[0m",
        COLOR.EIGHT: "\033[48;5;14m  \033[0m",
        COLOR.NINE: "\033[48;5;1m  \033[0m",
    }

    @classmethod
    def show_palette(cls):
        """Prints the color palette."""
        print(
            " | ".join(
                f"{color}={symbol.value}" for symbol, color in cls.PALETTE.items()
            )
        )

    def __init__(self, array: Union[List[List[int]], np.ndarray, None] = None) -> None:
        """
        Initializes the `Grid` with a 2D array of integers.

        Args:
            array (Union[List[List[int]], np.ndarray, None]): A 2D list of int or numpy ndarray representing the grid.
            If None, a default 1x1 `Grid` of `COLOR.ZERO` is used.

        Raises:
            ValueError: If the input array is not a 2D list or numpy ndarray of integers.
            ValueError: If any element in the array is not a value of `COLOR` (values of `COLOR` is 0~9 integers by default if `COLOR` is not modified. )

        Returns:
            None

        """
        if not array:
            array = [[0]]

        if not isinstance(array, (np.ndarray, list)):
            raise ValueError("Input array must be a 2D list or numpy ndarray.")

        if not all(item in COLOR for row in array for item in row):
            raise ValueError("Array elements must be values of `COLOR`")

        self._array = array if isinstance(array, np.ndarray) else np.array(array)

    @classmethod
    def from_json(cls, file_path: Union[str, Path]) -> Self:
        """
        Creates a `Grid` instance from a JSON file at a given path.

        Args:
            file_path (Union[str, Path]): File path of the JSON file to be loaded.

        Raises:
            ValueError: If the string format is incorrect or if any element is not a valid `COLOR` value.

        Returns:
            Grid: A `Grid` instance created from the JSON file.
        """
        try:
            with open(file_path) as f:
                array = json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format.")

        return cls(array)

    @classmethod
    def from_npy(cls, filePath: Union[str, Path]) -> Self:
        return cls(np.load(filePath))

    def save_as_json(self, path: Union[str, Path]) -> None:
        with open(path, "w") as f:
            json.dump(self.to_list(), f)

    def save_as_npy(self, path: str | Path) -> None:
        np.save(path, self.to_numpy())

    def to_list(self) -> List[List[int]]:
        return self._array.tolist()

    def to_numpy(self) -> np.ndarray:
        return self._array

    @property
    def shape(self) -> Tuple[int, int]:
        return self.to_numpy().shape

    def __repr__(self) -> str:
        return (
            "\n".join(
                "".join(self.PALETTE[COLOR(value)] for value in row)
                for row in self.to_numpy()
            )
            + "\n"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Grid):
            raise ValueError(
                "Cannot compare with non-`Grid` object. "
                "If the object is 2d list or numpy array, try converting it to `Grid` and then compare. "
            )
        return bool((self.to_numpy() == other.to_numpy()).all())

    def __sub__(self, other: object) -> int:
        """Number of different pixels"""
        if not isinstance(other, Grid):
            raise NotImplementedError(
                "Cannot compare with non-`Grid` object. "
                "If the object is 2d list or numpy array, try converting it to `Grid` and then compare. "
            )
        if self.shape != other.shape:
            raise ValueError(
                f"Connot compare `Grid`s of different shape. {self.shape} != {other.shape}"
            )
        return np.sum(self.to_numpy() != other.to_numpy())


class Pair:
    def __init__(
        self,
        input: Union[Grid, List[List[int]]],
        output: Union[Grid, List[List[int]]],
        censor: bool = False,
    ) -> None:
        self._input = input if isinstance(input, Grid) else Grid(input)
        self._output = output if isinstance(output, Grid) else Grid(output)
        self._is_censored = censor

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, grid: Union[Grid, List[List[int]]]):
        self._input = grid if isinstance(grid, Grid) else Grid(grid)
        return self._input

    @property
    def output(self):
        if self._is_censored:
            warnings.warn(
                "Access to `output` is censored. Call `.uncensor()` to gain access. ",
                UserWarning,
            )
            return None
        return self._output

    @output.setter
    def output(self, grid: Union[Grid, List[List[int]]]):
        if self._is_censored:
            warnings.warn(
                "Access to `output` is censored. Call `.uncensor()` to gain access. ",
                UserWarning,
            )
            return None
        self._output = grid if isinstance(grid, Grid) else Grid(grid)
        return self._output

    def censor(self):
        self._is_censored = True

    def uncensor(self):
        self._is_censored = False

    def __repr__(self):
        return repr(
            Layout(
                Layout(
                    "INPUT",
                    self.input,
                    direction="vertical",
                    align="center",
                ),
                "->",
                Layout(
                    "OUTPUT",
                    self.output if self.output else "*CENSORED*",
                    direction="vertical",
                    align="center",
                ),
                align="center",
            )
        )

    def to_dict(self):
        return {"input": self.input.to_list(), "output": self.output.to_list()}


class Task:
    def __init__(
        self,
        train: Union[
            List[Pair],
            List[Tuple[List[List[int]], List[List[int]]]],
            List[Tuple[Grid, Grid]],
        ],
        test: Union[
            List[Pair],
            List[Tuple[List[List[int]], List[List[int]]]],
            List[Tuple[Grid, Grid]],
        ],
        task_id: Optional[str] = None,
    ):
        self.train = [pair if isinstance(pair, Pair) else Pair(*pair) for pair in train]
        self.test = [pair if isinstance(pair, Pair) else Pair(*pair) for pair in test]
        self.task_id = task_id

    @classmethod
    def from_dict(
        cls,
        task_dict: Dict[
            Literal["train", "test"],
            List[Dict[Literal["input", "output"], List[List[int]]]],
        ],
        task_id: Optional[str] = None,
    ):
        train = [Pair(pair["input"], pair["output"]) for pair in task_dict["train"]]
        test = [Pair(pair["input"], pair["output"]) for pair in task_dict["test"]]

        return cls(train, test, task_id)

    def to_dict(self):
        return {
            "train": [pair.to_dict() for pair in self.train],
            "test": [pair.to_dict() for pair in self.test],
        }

    @classmethod
    def from_json(cls, file_path: Union[str, Path]):
        file_path = file_path if isinstance(file_path, Path) else Path(file_path)
        task_id = file_path.stem

        task = None
        try:
            with file_path.open() as f:
                task = json.load(f)
                # TODO: validate schema
        except Exception as e:
            raise RuntimeError(
                f"Failed to load and parse task json file at '{file_path}: {e}"
            )

        return cls.from_dict(task, task_id)

    @property
    def inputs(self):
        return [pair.input for pair in self.train + self.test]

    @property
    def outputs(self):
        return [pair.output for pair in self.train + self.test]

    def __repr__(self):
        train = Layout(
            *[
                Layout(
                    Layout(
                        f"INPUT {i}",
                        pair.input,
                        direction="vertical",
                        align="center",
                    ),
                    " -> ",
                    Layout(
                        f"OUTPUT {i}",
                        pair.output if pair.output else "*CENSORED*",
                        direction="vertical",
                        align="center",
                    ),
                )
                for i, pair in enumerate(self.train)
            ],
            direction="vertical",
        )
        test = Layout(
            *[
                Layout(
                    Layout(
                        f"INPUT {i}",
                        pair.input,
                        direction="vertical",
                        align="center",
                    ),
                    " -> ",
                    Layout(
                        f"OUTPUT {i}",
                        pair.output if pair.output else "*CENSORED*",
                        direction="vertical",
                        align="center",
                    ),
                )
                for i, pair in enumerate(self.test)
            ],
            direction="vertical",
        )
        width = max(train.width, test.width)
        return repr(
            Layout(
                f"< Task{' ' + self.task_id if self.task_id else ''} >".center(
                    width, "="
                ),
                " Train ".center(width, "-"),
                train,
                " Test ".center(width, "-"),
                test,
                direction="vertical",
            )
        )

    def __str__(self):
        return str(repr(self))

    def censor_outputs(self):
        for pair in self.train + self.test:
            pair.censor()

    def uncensor_outputs(self):
        for pair in self.train + self.test:
            pair.uncensor()

    def censor_test_outputs(self):
        for pair in self.test:
            pair.censor()

    def uncensor_test_outputs(self):
        for pair in self.test:
            pair.uncensor()
