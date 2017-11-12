# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import io
import os
import re

import path


class ReadmeMaker(object):
    """
    Make a README file with reStructuredText that
    acceptable format both GitHub and PyPI.
    """

    @property
    def doc_root_dir_path(self):
        return self.__doc_root_dir_path

    @doc_root_dir_path.setter
    def doc_root_dir_path(self, dir_path):
        self.__doc_root_dir_path = path.Path(dir_path)

    @property
    def doc_page_root_dir_path(self):
        return self.doc_root_dir_path.joinpath(self.pages_dir_name)

    @property
    def file_search_dir_path(self):
        return self.__file_search_dir_path

    @file_search_dir_path.setter
    def file_search_dir_path(self, dir_path):
        self.__file_search_dir_path = path.Path(dir_path)

    def __init__(self, project_name, output_dir, encoding="utf8"):
        if not os.path.isdir(output_dir):
            raise IOError("directory not found: " + output_dir)

        self.doc_root_dir_path = "."
        self.pages_dir_name = "pages"
        self.introduction_dir_name = "introduction"
        self.file_search_dir_path = self.doc_root_dir_path

        self.__project_name = project_name
        self.__indent_level = 0
        self.__stream = io.open(
            os.path.join(output_dir, "README.rst"), "w", encoding=encoding)

        self.__encoding = encoding

        self.write_chapter(self.__project_name)

    def __del__(self):
        self.__stream.close()
        self.__stream = None

    def set_indent_level(self, indent_level):
        self.__indent_level = indent_level

    def inc_indent_level(self):
        self.__indent_level += 1

    def dec_indent_level(self):
        self.__indent_level -= 1

    def write_line_list(self, line_list, line_break_count=2):
        self.__stream.write("\n".join([
            self.__adjust_for_pypi(line)
            for line in line_list
            if re.search(":caption:", line) is None
        ]))
        self.__stream.write("\n" * line_break_count)

    def write_toc(self, header="Table of Contents"):
        self.write_line_list([
            ".. contents:: {:s}".format(header),
            "   :depth: 2",
        ])

    def write_chapter(self, text):
        self.write_line_list([
            #"",
            text,
            self.__get_chapter_char() * (len(text) + 2),
        ], line_break_count=1)

    def write_file(self, file_path):
        with io.open(file_path, "r", encoding=self.__encoding) as f:
            self.write_line_list(
                [line.rstrip() for line in f.readlines()])

    def write_introduction_file(self, filename):
        self.write_file(
            self.doc_page_root_dir_path.joinpath(self.introduction_dir_name)
                .joinpath(filename))

    def write_from_relative_file(self, filename):
        self.write_file(self.file_search_dir_path.joinpath(filename))

    def __get_chapter_char(self):
        char_table = {
            0: "=",
            1: "-",
            2: "~",
            3: "^",
        }

        return char_table.get(self.__indent_level, char_table[max(char_table)])

    def __adjust_for_pypi(self, line):
        line = line.replace(".. code:: none", ".. code::")

        return line
