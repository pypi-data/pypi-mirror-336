# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import re
from pslmw_md_toc import MdToc
from .logger_config import logger


class MdTOCFiles(MdToc):
    def __init__(self, root_path, destination_path=None, ignore=None, output_toc_filename="TOC", toc_files=False, rm_toc_files=False):
        """
        Add to initializes the class MdToc with toc_files and rm_toc_files
        :param toc_files: Create toc on each md file from root_path (optional).
        :param rm_toc_files: Remove toc on each md file from root_path (optional).
        """
        super().__init__(root_path, destination_path=destination_path, ignore=ignore, output_toc_filename=output_toc_filename)

        for param in [toc_files, rm_toc_files]:
            if not isinstance(param, bool):
                msg =f"The {param} value must be boolean."
                logger.error(msg)
                raise Exception("ERROR", msg)

        self.toc_files = toc_files
        self.rm_toc_files = rm_toc_files

        self.TOC_START = "<!-- TOC START -->"
        self.TOC_END = "<!-- TOC END -->"

    def set_toc_files(self, value):
        self.toc_files = value

    def set_rm_toc_files(self, value):
        self.rm_toc_files = value

    def set_toc_start(self, value):
        self.TOC_START = value

    def set_toc_end(self, value):
        self.TOC_END = value

    def get_toc_files(self):
        return self.toc_files

    def get_rm_toc_files(self):
        return self.rm_toc_files

    def get_toc_start(self):
        return self.TOC_START

    def get_toc_end(self):
        return self.TOC_END

    def file_has_ignore_part(self, name):
        """
        Function to ignore directories that are on the ignore list
        :param name:
        :return list
        """
        ignore = [s for s in self.ignore if s in name]
        return ignore

    def generate_slug(self, heading):
        """
        Converts a heading into a Markdown-compatible anchor
        Replaces spaces with hyphens
        Removes special characters and converts to lowercase
        :param heading (str)
        :return str
        """
        slug = heading.strip().lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = slug.replace(' ', '-')
        return slug

    def get_content(self, ruta_archivo):
        """
        From the content file extract the TOC and the content in a list of lines for each list separated by comma.
        :param ruta_archivo:
        :return: list of lists
        """
        try:
            with open(ruta_archivo, 'r') as file:
                lines = file.readlines()
        except Exception as e:
            raise Exception("ERROR", f"Can not write on file {ruta_archivo}")

        inside_markers = False
        extracted_lines = []
        remaining_lines = []

        for line in lines:
            if self.TOC_START in line:
                inside_markers = True
                continue
            elif self.TOC_END in line:
                inside_markers = False
                continue

            if inside_markers:
                extracted_lines.append(line)
            else:
                remaining_lines.append(line)

        return extracted_lines, remaining_lines

    def generate_toc_for_file(self, content):
        """
        Generates the TOC based on the headings within a Markdown file,
        ignoring those within code blocks.
        :param content: (list): content Markdown from the file.
        :returns str:
        """
        toc = []
        in_block_code = False

        for line in content:
            # Detect start or end of a block of code with ```
            if line.strip().startswith("```"):
                in_block_code = not in_block_code
                continue

            if in_block_code:
                continue

            # Search for lines beginning with one or more `#` to detect headers
            if line.startswith('#'):
                level = line.count('#')  # The level is defined by the number of `#`
                header_text = line.strip('#').strip()
                slug = self.generate_slug(header_text)
                toc.append(f"{'  ' * (level - 1)}- [{header_text}](#{slug})")

        return "\n".join(toc)

    def save_markdown(self, file_path, content):
        """
        Save th content into the file
        :param content:
        :return:
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("".join(content))
        except Exception as e:
            raise Exception("ERROR", f"Can not write on file {file_path}")

    def remove_toc_in_file(self, file_path):
        """
        Remove TOC in the Markdown file.
        :param file_path: (str): Path of Markdown file
        :return boolean
        """
        try:
            toc, content = self.get_content(file_path)
            self.save_markdown(file_path, "".join(content))
            return True
        except:
            raise Exception("ERROR", f"Can remove the TOC in file '{file_path}'")

    def process_markdown_files(self, destination_path=None):
        """
        Processes all Markdown files in the directory, adding or replacing the TOC in each one.
        :param destination_path: str
        """
        if destination_path is None:
            destination_path = self.destination_path

        if os.path.isfile(destination_path) and destination_path.endswith('.md'):
            # If it's a Markdown file, process only that file
            self.generar_actualizar_toc(destination_path)
        elif os.path.isdir(destination_path):
            # If it is a directory, process all Markdown files in the directory
            for current_dir, subdi, files in os.walk(destination_path):
                # Skip directories
                if self.file_has_ignore_part(current_dir):
                    continue

                for f in files:
                    # Generate TOC for markdown files if they are not in the ignore list
                    if f.endswith('.md') and not self.has_ignore(f):
                        file_path = os.path.join(current_dir, f)
                        self.update_toc(str(file_path))
        else:
            logger.info(f"The path provided '{destination_path}' is not a valid .md file or directory")

    def update_toc(self, destination_path):
        """
        From a path creates a tree directory in a TOC Markdown format to a file
        :param destination_path:
        """
        toc, content = self.get_content(destination_path)
        toc = self.generate_toc_for_file(content)
        new_content = ""
        if content:
            if self.rm_toc_files and not self.toc_files:
                new_content = "".join(content).strip()
            else:
                new_content = self.TOC_START + "".join(toc).strip() + "\n" + self.TOC_END  + "\n\n" + "".join(content).strip()
        self.save_markdown(destination_path, new_content)
