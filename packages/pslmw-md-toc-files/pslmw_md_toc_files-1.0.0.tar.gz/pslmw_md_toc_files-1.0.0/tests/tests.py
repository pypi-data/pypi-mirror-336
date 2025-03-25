# -*- coding: utf-8 -*-
from __future__ import absolute_import
import shutil
import os

from pslmw_md_toc_files import MdTOCFiles

INPUT_DIR = os.path.dirname(__file__)

def rmtree(curr_dir):
    try:
        shutil.rmtree(curr_dir)
    except OSError as e:
        print(f"Error: {e.strerror}")

def rmfile(file_path):
    try:
        os.remove(file_path)
        print(f"File \'{file_path}\' deleted successfully.")
    except FileNotFoundError:
        print(f"File \'{file_path}\' not found.")
    except PermissionError:
        print(f"Permission denied to delete the file \'{file_path}\'.")
    except Exception as e:
        print(f"Error occurred while deleting the file: {e}")

def check_text_on_file(path_file, text_to_check):
    with open(path_file) as f:
        for line in f:
            if text_to_check in line:
                return True
    return False

def test_none_args():
    try:
        MdTOCFiles()
    except Exception as e:
        assert "MdTOCFiles.__init__() missing 1 required positional argument: 'root_path'" in str(e)

def test_toc_and_toc_files():
    root_path = INPUT_DIR + "/test_default"
    destination_path = INPUT_DIR + "/test_dir"
    rmtree(destination_path)
    try:
        generador = MdTOCFiles(root_path, destination_path=destination_path, toc_files=True)
        generador.create_toc()
        toc_start = generador.get_toc_start()
        toc_end = generador.get_toc_end()
        assert os.path.exists(destination_path + "/TOC.md")
        assert check_text_on_file(destination_path + "/TOC.md", "# Table of Contents")
        assert not check_text_on_file(destination_path + "/TOC.md", toc_start)
        generador.process_markdown_files()
        assert os.path.exists(destination_path)
        assert check_text_on_file(destination_path + "/file1.md", toc_start)
        assert check_text_on_file(destination_path + "/file1.md", toc_end)
        assert check_text_on_file(destination_path + "/file1.md", "## Subtitle 4")
        assert check_text_on_file(destination_path + "/TOC.md", toc_start)
    finally:
        rmtree(destination_path)

def test_toc_and_toc_files_with_toc_ignore():
    root_path = INPUT_DIR + "/test_default"
    destination_path = INPUT_DIR + "/test_dir"
    rmtree(destination_path)
    try:
        generador = MdTOCFiles(root_path, destination_path=destination_path, ignore=["TOC.md"], toc_files=True)
        generador.create_toc()
        toc_start = generador.get_toc_start()
        toc_end = generador.get_toc_end()
        assert os.path.exists(destination_path + "/TOC.md")
        assert check_text_on_file(destination_path + "/TOC.md", "# Table of Contents")
        assert not check_text_on_file(destination_path + "/TOC.md", toc_start)
        generador.process_markdown_files()
        assert os.path.exists(destination_path)
        assert check_text_on_file(destination_path + "/file1.md", toc_start)
        assert check_text_on_file(destination_path + "/file1.md", toc_end)
        assert check_text_on_file(destination_path + "/file1.md", "## Subtitle 4")
        assert not check_text_on_file(destination_path + "/TOC.md", toc_start)
    finally:
        rmtree(destination_path)

def test_toc_and_toc_files_with_toc_ignore_error_ignore_name():
    root_path = INPUT_DIR + "/test_default"
    destination_path = INPUT_DIR + "/test_dir"
    rmtree(destination_path)
    try:
        generador = MdTOCFiles(root_path, destination_path=destination_path, ignore=["test.md"], toc_files=True)
        generador.create_toc()
        toc_start = generador.get_toc_start()
        toc_end = generador.get_toc_end()
        assert os.path.exists(destination_path + "/TOC.md")
        assert check_text_on_file(destination_path + "/TOC.md", "# Table of Contents")
        assert not check_text_on_file(destination_path + "/TOC.md", toc_start)
        generador.process_markdown_files()
        assert os.path.exists(destination_path)
        assert check_text_on_file(destination_path + "/file1.md", toc_start)
        assert check_text_on_file(destination_path + "/file1.md", toc_end)
        assert check_text_on_file(destination_path + "/file1.md", "## Subtitle 4")
        assert check_text_on_file(destination_path + "/TOC.md", toc_start)
    finally:
        rmtree(destination_path)

def test_toc_files():
    root_path = INPUT_DIR + "/test_default"
    destination_path = INPUT_DIR + "/test_dir"
    rmtree(destination_path)
    try:
        generador = MdTOCFiles(root_path, destination_path=destination_path, toc_files=True)
        generador.process_markdown_files()
        toc_start = generador.get_toc_start()
        toc_end = generador.get_toc_end()
        assert os.path.exists(destination_path)
        assert check_text_on_file(destination_path + "/file1.md", toc_start)
        assert check_text_on_file(destination_path + "/file1.md", toc_end)
        assert check_text_on_file(destination_path + "/file1.md", "## Subtitle 4")
    finally:
        rmtree(destination_path)

def test_toc_files_with_toc():
    root_path = INPUT_DIR + "/test_default"
    destination_path = INPUT_DIR + "/test_dir"
    rmtree(destination_path)
    try:
        generador = MdTOCFiles(root_path, destination_path=destination_path, toc_files=True)
        generador.process_markdown_files()
        toc_start = generador.get_toc_start()
        toc_end = generador.get_toc_end()
        assert os.path.exists(destination_path)
        assert check_text_on_file(destination_path + "/file1.md", toc_start)
        assert check_text_on_file(destination_path + "/file1.md", toc_end)
        assert check_text_on_file(destination_path + "/file1.md", "## Subtitle 4")
        assert check_text_on_file(destination_path + "/file_with_toc.md", toc_start)
        assert check_text_on_file(destination_path + "/file_with_toc.md", toc_end)
        assert check_text_on_file(destination_path + "/file_with_toc.md", "## Subtitle 4")
    finally:
        rmtree(destination_path)

def test_rm_all_toc_files():
    root_path = INPUT_DIR + "/test_default"
    destination_path = INPUT_DIR + "/test_dir"
    rmtree(destination_path)
    try:
        generador = MdTOCFiles(root_path, destination_path=destination_path, toc_files=True)
        generador.process_markdown_files()
        toc_start = generador.get_toc_start()
        assert os.path.exists(destination_path)
        assert check_text_on_file(destination_path + "/file1.md", toc_start)
        assert check_text_on_file(destination_path + "/file1.md", "## Subtitle 4")
        assert check_text_on_file(destination_path + "/file_with_toc.md", toc_start)
        assert check_text_on_file(destination_path + "/file_with_toc.md", "## Subtitle 4")
        generador.remove_toc_in_file(destination_path + "/file_with_toc.md")
        assert check_text_on_file(destination_path + "/file1.md", toc_start)
        assert check_text_on_file(destination_path + "/file1.md", "## Subtitle 4")
        assert not check_text_on_file(destination_path + "/file_with_toc.md", toc_start)
        assert check_text_on_file(destination_path + "/file_with_toc.md", "## Subtitle 4")
    finally:
        rmtree(destination_path)
