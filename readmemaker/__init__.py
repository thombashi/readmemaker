# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

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
    def introduction_root_dir_path(self):
        return self.doc_page_root_dir_path.joinpath(self.introduction_dir_name)

    @property
    def examples_root_dir_path(self):
        return self.doc_page_root_dir_path.joinpath(self.examples_dir_name)

    def __init__(self, project_name, output_dir):
        if not os.path.isdir(output_dir):
            raise IOError("directory not found: " + output_dir)

        self.doc_root_dir_path = u"."
        self.pages_dir_name = u"pages"
        self.introduction_dir_name = u"introduction"
        self.examples_dir_name = u"examples"

        self.__project_name = project_name
        self.__indent_level = 0
        self.__stream = open(os.path.join(output_dir, "README.rst"), "w")

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

    def write_line_list(self, line_list):
        self.__stream.write(u"\n".join([
            self.__adjust_for_pypi(line)
            for line in line_list
            if re.search(":caption:", line) is None
        ]))
        self.__stream.write(u"\n" * 2)

    def write_chapter(self, text):
        self.write_line_list([
            text,
            self.__get_chapter_char() * len(text),
        ])

    def write_file(self, file_path):
        with open(file_path) as f:
            self.write_line_list([line.rstrip()for line in f.readlines()])

    def write_introduction_file(self, filename):
        self.write_file(self.introduction_root_dir_path.joinpath(filename))

    def write_example_file(self, filename):
        self.write_file(self.examples_root_dir_path.joinpath(filename))

    def __get_chapter_char(self):
        char_table = {
            0: u"=",
            1: u"-",
            2: u"~",
            3: u"^",
        }

        return char_table.get(self.__indent_level, char_table[max(char_table)])

    def __adjust_for_pypi(self, line):
        line = line.replace(".. code-block::", ".. code::")
        line = line.replace(".. code:: none", ".. code::")

        return line
