# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import shutil
from .logger_config import logger


class MdToc:
    def __init__(self, root_path, destination_path=None, ignore=None, output_toc_filename="TOC"):
        """
        Initializes the class with the base directory, destination directory, the list of directories to ignore and a filename .md.
        :param root_path: Base path of the directory.
        :param destination_path: Path of the directory (optional).
        :param ignore: List of directories to ignore (optional).
        :param output_toc_filename: Name of de resulting TOC file name (optional).
        """
        self.ignore = ['.DS_Store', '.gitignore', '.idea', '*.log']
        if ignore is not None:
            if not isinstance(ignore, (list, tuple)):
                raise Exception("ERROR", f"The ignore {ignore} value must be list or tuple.")
            self.ignore += ignore

        root_path = self.remove_bad_end(root_path)
        if self.valid_path(root_path):
            self.root_path = root_path

        self.destination_path = self.set_destination_path(destination_path)

        if not isinstance(output_toc_filename, str):
            msg = f"The output_toc_filename {output_toc_filename} value must be string."
            logger.error(msg)
            raise Exception("ERROR", msg)
        self.output_toc_filename = output_toc_filename + ".md"

        logger.info(f"[SET] Root path: {self.root_path} Destination path: {self.destination_path} List ignore: {self.ignore} and TOC name: {self.output_toc_filename}")

    def set_destination_path(self, destination_path):
        if destination_path is None:
            destination_path = self.root_path
        else:
            destination_path = self.remove_bad_end(destination_path)
            if self.valid_path(destination_path):
                if self.root_path != destination_path:
                    self.copy(root_path=self.root_path, destination_path=destination_path, ignore=self.ignore)
        self.destination_path = destination_path
        return destination_path

    def set_ignore(self, ignore):
        if not isinstance(ignore, (tuple, list)):
            msg = f"The param must be a list"
            logger.error(msg)
            raise Exception("Error", msg)
        self.ignore = ignore

    def set_output_toc_filename(self, output_toc_filename):
        self.output_toc_filename = output_toc_filename

    def get_root_path(self):
        return self.root_path

    def get_destination_path(self):
        return self.destination_path

    def get_ignore(self):
        return self.ignore

    def get_output_toc_filename(self):
        return self.output_toc_filename

    def remove_bad_end(self, path):
        """
        Remove "/" at the end of the path to avoid bad rutes
        :param path:
        :return (str): path
        """
        logger.debug(f"Removing all '/' from the end of the {path} ...")
        if path.endswith("/"):
            dirname, filename = os.path.split(path)
            os.path.join(os.path.dirname(dirname), filename)
        else:
            dirname = path
        logger.debug(f"Final path {dirname}")
        return dirname

    def valid_path(self, full_path):
        """
        Check if the Path is on the ignore list.
        :param full_path: (str): Path.
        :returns str: Name formated.
        """
        logger.debug(f"Validating the path '{full_path}' is a correct dir ...")
        if not os.path.isdir(os.path.dirname(full_path)):
            msg = f"The path {full_path} is not valid."
            logger.error(msg)
            raise Exception("ERROR", msg)
        logger.debug("Its CORRECT.")

        logger.debug(f"Validating the path '{full_path}' is not on the ignores path list")
        if any(shutil.fnmatch.fnmatch(full_path, pattern) for pattern in self.ignore):
            msg = f"The Path {full_path} is on list of ignore argument."
            logger.error(msg)
            raise Exception("ERROR", msg)
        logger.debug("It is NOT on it.")
        return True

    def has_ignore(self, name):
        """
        Ignore hidden files or files that are on the ignore list.
        :param: name (str)
        :returns: boolean
        """
        return name.startswith('.') or name in self.ignore

    def copy(self, root_path=None, destination_path=None, ignore=None):
        """
        Copy all files except ignored ones from root path to destination path
        :param root_path: Base path of the directory. (optional)
        :param destination_path: Path of the directory (optional).
        :param ignore: List of directories to ignore (optional).
        """
        logger.debug(f"Start copy form path '{root_path} to the destination path '{destination_path} ignoring {ignore} files ...")
        if root_path is None:
            root_path = self.root_path
        else:
            if self.valid_path(root_path):
                root_path = self.root_path

        if destination_path is None:
            destination_path = self.root_path
        else:
            if self.valid_path(destination_path):
                destination_path = destination_path

        to_ignore = False
        if ignore is not None and isinstance(ignore, (list, tuple)):
            to_ignore = True

        if not os.path.exists(root_path):
            raise Exception("ERROR", f"The root Path {root_path} does not exist.")

        if not os.path.exists(destination_path):
            # Copy everything
            # shutil.copytree(root_path, destination_path, ignore=shutil.ignore_patterns(*ignore))

            # Copy only the files to work off
            for item in os.listdir(root_path):
                if to_ignore and item in ignore:
                    continue

                origen_item = os.path.join(root_path, item)
                destino_item = os.path.join(destination_path, item)

                if os.path.isdir(origen_item):
                    shutil.copytree(origen_item, destino_item, dirs_exist_ok=True)
                else:
                    os.makedirs(os.path.dirname(destino_item), exist_ok=True)
                    shutil.copy2(origen_item, destino_item)
        else:
            msg = f"The destination Path {destination_path} already exist."
            logger.info(msg)

    def get_format_name(self, name, is_dir=False):
        """
        Format name of the directory or file.
        :param name: (str): Name of the directory or file.
        :param is_dir: (bool): Tells if is a directory.
        :returns: str: Name formated.
        """
        logger.debug(f"Formatting the name on TOC ...")
        if is_dir:
            final_name = name.upper()
        else:
            name_not_ext, _ = os.path.splitext(name)
            if name_not_ext.startswith('_'):
                return name_not_ext
            name_not_ext = name_not_ext.replace('_', ' ').strip()
            final_name = name_not_ext.capitalize()

        logger.debug(f"The name will be '{final_name}'")
        return final_name

    def generate_markdown_toc(self, root_path, level=0, parent_index="", is_root=False):
        """
        Generates a table of contents in markdown based on the structure of directories and subdirectories.
        :param root_path: (str): Base path of the directory.
        :param level: (int): Depth level in the structure (for subdirectories).
        :param parent_index: (str): The index of the parent directory to keep numbering.
        :param is_root: (bool): Indicates whether we are at the root to use readable numbers.
        :returns: str: TOC in Markdown format.
        """
        elements = []
        local_index = 1

        logger.debug(f"Staring generation Markdown File TOC {self.output_toc_filename} ...")
        # List of directories and files in the base path, ignoring hidden and those in the IGNORE list
        for name in sorted(os.listdir(root_path)):
            if self.has_ignore(name):
                continue

            full_path = os.path.join(root_path, name)
            absolute_path = os.path.abspath(full_path)
            less_path = os.path.abspath(self.destination_path)
            link_to = absolute_path.replace(less_path, '.')

            # Create hierarchical index (use readable numbers in root)
            if is_root:
                current_index = f"{local_index}."
            else:
                current_index = f"{parent_index}{local_index}."

            format_name = self.get_format_name(name, is_dir=os.path.isdir(full_path))

            if os.path.isdir(full_path) and not os.path.islink(full_path):
                logger.debug(f"Working with directory '{full_path}' ...")
                # If it is a directory, add to TOC with absolute link and process recursively
                elements.append(f"{'  ' * level}- {current_index} [{format_name}/]({link_to}/)")
                sub_elementos = self.generate_markdown_toc(full_path, level + 1, current_index)
                elements.append(sub_elementos)
            else:
                logger.debug(f"Working with file '{full_path}' ...")
                # If it is a file, add it to the TOC with an absolute link
                elements.append(f"{'  ' * level}- {current_index} [{format_name}]({link_to})")

            local_index += 1

        logger.debug(f"File TOC created with {len(elements)} lines")
        return "\n".join(elements)

    def create_toc(self):
        """
        Create the TOC.md file with the contents of the generated TOC.
        """
        toc = self.generate_markdown_toc(self.destination_path, is_root=True)

        try:
            # Save the TOC to the TOC.md file
            with open(os.path.join(self.destination_path, self.output_toc_filename), 'w') as toc_file:
                toc_file.write("# Table of Contents\n\n")
                toc_file.write(toc)
                logger.info(f"TOC generated successfully on {self.destination_path}/{self.output_toc_filename} from {self.root_path}")
        except:
            msg = f"The TOC could not be generated because the path {self.destination_path} is not a directory."
            logger.error(msg)
            raise Exception("ERROR", msg)