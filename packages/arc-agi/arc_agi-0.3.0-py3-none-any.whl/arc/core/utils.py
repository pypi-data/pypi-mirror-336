import re
from typing import List, Literal, Any
import os
import requests
import zipfile
import io


ANSI_ESCAPE_PATTERN = re.compile(r"\x1b\[[0-9;]*m")


def strip_ansi(text: str) -> str:
    """Removes ANSI escape codes from the string for correct width calculation."""
    return ANSI_ESCAPE_PATTERN.sub("", text)


def ansi_width(text: str) -> int:
    """Returns the width of text after removing ANSI escape sequences."""
    return len(strip_ansi(text))


def align_lines(
    lines: List[str],
    target_width: int,
    align: Literal["start", "center", "end"],
) -> List[str]:
    """Aligns lines while preserving ANSI codes."""
    if align == "start":
        return [
            line + " " * (max(target_width - ansi_width(line), 0)) for line in lines
        ]
    elif align == "center":
        return [
            " " * (max(target_width - ansi_width(line), 0) // 2)
            + line
            + " " * ((max(target_width - ansi_width(line), 0) + 1) // 2)
            for line in lines
        ]
    elif align == "end":
        return [" " * max(target_width - ansi_width(line), 0) + line for line in lines]


class Layout:
    def __init__(
        self,
        *elements: Any,
        direction: Literal["horizontal", "vertical"] = "horizontal",
        align: Literal["start", "center", "end"] = "start",
        show_divider: bool = False,
        min_width: int = 0,
    ):
        self.elements = elements
        self.direction = direction
        self.align = align
        self.show_divider = show_divider
        self.min_width = min_width

    @property
    def width(self):
        return max(ansi_width(line) for line in repr(self).splitlines())

    @property
    def height(self):
        return len(repr(self).splitlines())

    def __repr__(self) -> str:
        elements = [
            (element if isinstance(element, str) else repr(element)).splitlines()
            for element in self.elements
        ]

        if self.direction == "horizontal":
            max_height = max(len(element) for element in elements)
            normalized_elements = [
                element + [""] * (max_height - len(element)) for element in elements
            ]
            widths = [max(ansi_width(line) for line in element) for element in elements]
            aligned_elements = [
                align_lines(element, width, self.align)
                for element, width in zip(normalized_elements, widths)
            ]
            divider = " | " if self.show_divider else ""
            return "\n".join(
                align_lines(
                    [
                        divider.join(
                            aligned_elements[col][row]
                            for col in range(len(aligned_elements))
                        )
                        for row in range(max_height)
                    ],
                    self.min_width,
                    self.align,
                )
            )

        elif self.direction == "vertical":
            max_width = max(
                max(ansi_width(line) for line in element) for element in elements
            )
            aligned_elements = [
                align_lines(element, max_width, self.align) for element in elements
            ]
            divider = "\n" + "-" * max_width if self.show_divider else ""
            return f"{divider}\n".join(
                "\n".join(element) for element in aligned_elements
            )

    def __str__(self) -> str:
        elements = [str(element).splitlines() for element in self.elements]

        if self.direction == "horizontal":
            max_height = max(len(element) for element in elements)
            normalized_elements = [
                element + [""] * (max_height - len(element)) for element in elements
            ]
            widths = [max(ansi_width(line) for line in element) for element in elements]
            aligned_elements = [
                align_lines(element, width, self.align)
                for element, width in zip(normalized_elements, widths)
            ]
            divider = " | " if self.show_divider else ""
            return "\n".join(
                divider.join(
                    aligned_elements[col][row] for col in range(len(aligned_elements))
                )
                for row in range(max_height)
            )

        elif self.direction == "vertical":
            max_width = max(
                max(ansi_width(line) for line in element) for element in elements
            )
            aligned_elements = [
                align_lines(element, max_width, self.align) for element in elements
            ]
            divider = "\n" + "-" * max_width if self.show_divider else ""
            return f"{divider}\n".join(
                "\n".join(element) for element in aligned_elements
            )


def download_from_github(
    repo_owner, repo_name, path, branch="main", destination="./downloaded"
):
    """
    Downloads and extracts a specific path from a GitHub repository.

    :param repo_owner: GitHub username or organization.
    :param repo_name: Repository name.
    :param path: Path to the folder inside the repo to extract.
    :param branch: Repo branch (default: "main").
    :param destination: Local destination folder for saving files.
    """
    url = f"https://github.com/{repo_owner}/{repo_name}/archive/refs/heads/{branch}.zip"
    print(f"Downloading from {url}")
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            repo_folder = f"{repo_name}-{branch}/"
            target_folder = f"{repo_folder}{path}/"

            extracted_files = 0

            for file in zip_file.namelist():
                if file.startswith(target_folder) and not file.endswith("/"):
                    relative_path = file[len(target_folder) :]
                    save_path = os.path.join(destination, relative_path)

                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    with zip_file.open(file) as source, open(save_path, "wb") as target:
                        target.write(source.read())

                    extracted_files += 1

            if extracted_files > 0:
                print(
                    f"✅ Successfully downloaded '{path}' from {repo_owner}/{repo_name} into '{destination}'."
                )
            else:
                print(
                    f"⚠️ No files extracted. Check if the path '{path}' exists in the repository."
                )

    else:
        print(f"❌ Failed to download: HTTP {response.status_code}")
