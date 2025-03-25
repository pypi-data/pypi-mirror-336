# -*- coding: utf-8 -*-
from __future__ import absolute_import
import shutil
import os

from pslmw_md_toc_files_plus import MdTOCFilesPlus

INPUT_DIR = os.path.dirname(__file__)

def rmtree(curr_dir):
    try:
        shutil.rmtree(curr_dir)
    except OSError as e:
        print(f"Error: {e.strerror}")

def check_text_on_file(path_file, text_to_check):
    with open(path_file) as f:
        for line in f:
            if text_to_check in line:
                return True
    return False

def test_none_args():
    try:
        MdTOCFilesPlus()
    except Exception as e:
        assert "MdTOCFilesPlus.__init__() missing 1 required positional argument: 'root_path'" in str(e)

def test_toc_file_from_single_file():
    filename = "/file1.md"
    root_path = INPUT_DIR + "/test_default" + filename
    destination_path = INPUT_DIR + "/md_toc_single"
    try:
        generador = MdTOCFilesPlus(root_path, toc_files=True, single=True)
        toc_start = generador.get_toc_start()
        generador.process_markdown_files()
        assert os.path.exists(destination_path)
        assert check_text_on_file(destination_path + filename, toc_start)
    finally:
        rmtree(destination_path)

def test_error_toc_file_from_single_file_with_dest_path():
    root_path = INPUT_DIR + "/test_default/file1.md"
    destination_path = INPUT_DIR + "/asd/f.md"
    try:
        MdTOCFilesPlus(root_path, destination_path=destination_path, toc_files=True, single=True)
    except Exception as e:
        assert "ERROR", f"The destination path {destination_path} is not valid." in str(e)

def test_force_copy():
    root_path = INPUT_DIR + "/test_default"
    destination_path = INPUT_DIR + "/test_dir"
    md_toc = MdTOCFilesPlus(root_path, destination_path=destination_path)
    md_toc.create_toc()
    assert os.path.exists(destination_path + "/TOC.md")
    try:
        MdTOCFilesPlus(root_path, destination_path=destination_path, force=True)
        assert not os.path.exists(destination_path + "/TOC.md")
    finally:
        rmtree(destination_path)

def test_error_force_copy_root_path():
    root_path = INPUT_DIR + "/test_default"
    try:
        MdTOCFilesPlus(root_path, force=True)
    except Exception as e:
        assert f'Can delete de {root_path}. Its the Root Path.' in str(e)
