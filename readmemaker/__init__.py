"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import io
import os
import re
import sys
from typing import IO, List, Optional, Union

import path


class ReadmeMaker:
    """
    Make a README file with reStructuredText that
    acceptable format both GitHub and PyPI.
    """

    @property
    def doc_root_dir_path(self) -> path.Path:
        return self.__doc_root_dir_path

    @doc_root_dir_path.setter
    def doc_root_dir_path(self, dir_path: Union[str, path.Path]) -> None:
        self.__doc_root_dir_path = path.Path(dir_path)

    @property
    def doc_page_root_dir_path(self) -> path.Path:
        return self.doc_root_dir_path.joinpath(self.pages_dir_name)

    @property
    def file_search_dir_path(self) -> path.Path:
        return self.__file_search_dir_path

    @file_search_dir_path.setter
    def file_search_dir_path(self, dir_path) -> None:
        self.__file_search_dir_path = path.Path(dir_path)

    def __init__(
        self,
        project_name: str,
        output_dir: str,
        encoding: str = "utf8",
        is_make_toc: bool = False,
        project_url: str = None,
    ) -> None:
        if not os.path.isdir(output_dir):
            raise IOError("directory not found: " + output_dir)

        self.doc_root_dir_path = "."
        self.pages_dir_name = "pages"
        self.introduction_dir_name = "introduction"
        self.file_search_dir_path = self.doc_root_dir_path

        self.__project_name = project_name
        self.__project_url = project_url
        self.__indent_level = 0
        self.__stream = io.open(
            os.path.join(output_dir, "README.rst"), "w", encoding=encoding
        )  # type: Optional[IO]

        self.__encoding = encoding

        if self.__project_url:
            self.__project_link = "`{:s} <{:s}>`__".format(self.__project_name, self.__project_url)
        else:
            self.__project_link = "{:s}".format(self.__project_name)

        if is_make_toc:
            self.write_toc()
        else:
            self.write_chapter(self.__project_name)

    def __del__(self) -> None:
        if self.__stream:
            self.__stream.close()
        self.__stream = None

    def set_indent_level(self, indent_level: int) -> None:
        self.__indent_level = indent_level

    def inc_indent_level(self) -> None:
        self.__indent_level += 1

    def dec_indent_level(self) -> None:
        self.__indent_level -= 1

    def write_lines(self, lines: List[str], line_break_count: int = 2) -> None:
        if not self.__stream:
            print("ERROR: attempt to write to closed stream", file=sys.stderr)
            return

        self.__stream.write(
            "\n".join(
                [
                    self.__adjust_for_pypi(line)
                    for line in lines
                    if re.search(":caption:", line) is None
                ]
            )
        )
        self.__stream.write("\n" * line_break_count)

    def write_toc(self, header: str = None) -> None:
        if header is None:
            header = "**{:s}**".format(self.__project_name)

        self.write_lines(
            [".. contents:: {:s}".format(header), "   :backlinks: top", "   :depth: 2"]
        )

    def write_chapter(self, text: str) -> None:
        self.write_lines([text, self.__get_chapter_char() * (len(text) + 2)], line_break_count=1)

    def write_file(self, file_path: str) -> None:
        with io.open(file_path, "r", encoding=self.__encoding) as f:
            self.write_lines(
                [
                    line.rstrip().replace(
                        "{:s} is".format(self.__project_name), "{:s} is".format(self.__project_link)
                    )
                    for line in f.readlines()
                ]
            )

    def write_introduction_file(self, filename: str) -> None:
        self.write_file(
            self.doc_page_root_dir_path.joinpath(self.introduction_dir_name).joinpath(filename)
        )

    def write_from_relative_file(self, filename: str) -> None:
        self.write_file(self.file_search_dir_path.joinpath(filename))

    def __get_chapter_char(self) -> str:
        char_table = {0: "=", 1: "-", 2: "~", 3: "^"}

        return char_table.get(self.__indent_level, char_table[max(char_table)])

    @staticmethod
    def __adjust_for_pypi(line: str) -> str:
        line = line.replace(".. code:: none", ".. code::")
        line = line.replace(".. code-block:: none", ".. code-block::")

        return line
