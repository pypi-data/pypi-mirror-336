# -*- coding: utf-8 -*-
import shutil
import os

from pslmw_md_toc import MdToc

INPUT_DIR = os.path.dirname(__file__)

if not os.path.exists(INPUT_DIR + "/test_default/.invisible_dir"):
    os.mkdir(INPUT_DIR + "/test_default/.invisible_dir")

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
        MdToc()
    except Exception as e:
        assert "MdToc.__init__() missing 1 required positional argument: 'root_path'" in str(e)


def test_only_root_dir_args():
    destination_path = INPUT_DIR + "/test_dir"
    rmtree(destination_path)
    toc_filename = INPUT_DIR + "/test_dir/TOC.md"
    MdToc(INPUT_DIR)
    assert not os.path.exists(destination_path)
    assert not os.path.exists(toc_filename)

def test_diff_root_than_destination_path_args():
    root_path = INPUT_DIR + "/test_default"
    destination_path = INPUT_DIR + "/test_dir"
    toc_filename = destination_path + "/TOC.md"
    rmtree(destination_path)
    try:
        MdToc(root_path, destination_path)
        assert os.path.exists(destination_path)
        assert not os.path.exists(toc_filename)
    finally:
        rmtree(destination_path)

def test_path_bad_end_args():
    root_path = INPUT_DIR + "/test_default"
    destination_path = INPUT_DIR + "/test_dir"
    toc_filename = destination_path + "/TOC.md"
    rmtree(destination_path)
    try:
        toc = MdToc(root_path + "/////", destination_path + "/")
        toc.create_toc()
        assert os.path.exists(INPUT_DIR)
        assert os.path.exists(toc_filename)
    finally:
        rmtree(destination_path)

def test_toc_args():
    root_path = INPUT_DIR + "/test_default"
    destination_path = INPUT_DIR + "/test_dir"
    toc_filename = destination_path + "/TOC.md"
    rmtree(destination_path)
    try:
        generador = MdToc(root_path, destination_path)
        generador.create_toc()
        assert os.path.exists(destination_path)
        assert os.path.exists(toc_filename)
    finally:
        rmtree(destination_path)
        rmfile(toc_filename)


def test_toc_output_file_name_args():
    root_path = INPUT_DIR + "/test_default"
    destination_path = INPUT_DIR + "/test_dir"
    toc_filename = destination_path + "/test_TOC_file_name.md"
    rmtree(destination_path)
    try:
        generador = MdToc(root_path, destination_path=destination_path, output_toc_filename="test_TOC_file_name")
        generador.create_toc()
        assert os.path.exists(destination_path)
        assert os.path.exists(toc_filename)
        assert check_text_on_file(toc_filename, "# Table of Contents")
        assert not check_text_on_file(toc_filename, "invisible_file")
    finally:
        rmtree(destination_path)

def test_error_toc_ignore_string_value():
    root_path = INPUT_DIR + "/test_default"
    destination_path = INPUT_DIR + "/test_dir"
    rmtree(destination_path)
    try:
        MdToc(root_path, destination_path=destination_path, ignore="string_value_error")
    except Exception as e:
        assert "The ignore string_value_error value must be list or tuple." in str(e)
    finally:
        rmtree(destination_path)

def test_toc_ignore_dir():
    root_path = INPUT_DIR + "/test_default"
    destination_path = INPUT_DIR + "/test_dir"
    toc_filename = destination_path + "/TOC.md"
    rmtree(destination_path)
    try:
        generador = MdToc(root_path, destination_path=destination_path, ignore=["ignore_dir"])
        generador.create_toc()
        assert os.path.exists(toc_filename)
        assert not os.path.exists(destination_path + "/ignore_dir")
        assert os.path.exists(destination_path + "/.invisible_dir")
    finally:
        rmtree(destination_path)

def test_toc_ignore_file():
    root_path = INPUT_DIR + "/test_default"
    destination_path = INPUT_DIR + "/test_dir"
    toc_filename = destination_path + "/TOC.md"
    rmtree(destination_path)
    try:
        generador = MdToc(root_path, destination_path=destination_path, ignore=["ignore_file1.md"])
        generador.create_toc()
        assert os.path.exists(toc_filename)
        assert not os.path.exists(destination_path + "/ignore_file1.md")
        assert os.path.exists(destination_path + "/.invisible_dir")
    finally:
        rmtree(destination_path)
#
def test_toc_ignore_dir_and_file():
    root_path = INPUT_DIR + "/test_default"
    destination_path = INPUT_DIR + "/test_dir"
    toc_filename = destination_path + "/TOC.md"
    rmtree(destination_path)
    try:
        generador = MdToc(root_path, destination_path=destination_path, ignore=["ignore_dir", "ignore_file1.md"])
        generador.create_toc()
        assert os.path.exists(toc_filename)
        assert not os.path.exists(destination_path + "/ignore_dir")
        assert not os.path.exists(destination_path + "/ignore_file1.md")
        assert os.path.exists(destination_path + "/.invisible_dir")
    finally:
        rmtree(destination_path)

def test_error_destination_path_exists():
    root_path = INPUT_DIR + "/test_default"
    destination_path = INPUT_DIR + "/test_dir"
    rmtree(destination_path)
    try:
        MdToc(root_path, destination_path=destination_path)
        MdToc(root_path, destination_path=destination_path)
    except Exception as e:
        assert f'The destination Path {INPUT_DIR}/test_dir already exist.' in str(e)
    finally:
        rmtree(destination_path)

def test_copy():
    root_path = INPUT_DIR + "/test_default"
    destination_path = INPUT_DIR + "/test_dir"
    rmtree(destination_path)
    try:
        md_toc = MdToc(root_path)
        md_toc.set_destination_path(destination_path=destination_path)
        assert os.path.exists(destination_path)
    finally:
        rmtree(destination_path)

def test_error_copy():
    root_path = INPUT_DIR + "/test_default"
    destination_path = INPUT_DIR + "/test_dir"
    rmtree(destination_path)
    try:
        MdToc(root_path)
        assert not os.path.exists(destination_path)
    finally:
        rmtree(destination_path)

def test_error_invalid_destination_path():
    root_path = INPUT_DIR + "/test_default"
    destination_path = INPUT_DIR + "/test_dir/md.md"
    try:
        MdToc(root_path, destination_path=destination_path)
    except Exception as e:
        assert f"The path {destination_path} is not valid." in str(e)
    finally:
        rmtree(destination_path)

def test_error_invalid_destination_path_with_set():
    root_path = INPUT_DIR + "/test_default"
    destination_path = INPUT_DIR + "/test_dir/md.md"
    try:
        md_toc = MdToc(root_path)
        md_toc.set_destination_path(destination_path=destination_path)
    except Exception as e:
        assert f"The path {destination_path} is not valid." in str(e)
    finally:
        rmtree(destination_path)

    destination_path = INPUT_DIR + "/test_dir"
    try:
        md_toc = MdToc(root_path)
        md_toc.set_destination_path(destination_path=destination_path)
        assert os.path.exists(destination_path)
    finally:
        rmtree(destination_path)
