# -*- coding: utf-8 -*-
import os
import shutil
from .logger_config import logger
from pslmw_md_toc_files import MdTOCFiles


class MdTOCFilesPlus(MdTOCFiles):
    def __init__(self, root_path, destination_path=None, ignore=None, output_toc_filename="TOC", toc_files=False, rm_toc_files=False, force=False, single=False):
        """
        Add to initializes the class MarkdownTOCFiles initializes the class with force and single
        :param force: Delete destination path if exist before make a copy (optional).
        :param single: Allow to work with a file as a root_path (optional).
        """
        if not os.path.isdir(os.path.dirname(root_path)):
            raise Exception("ERROR", f"The root path {root_path} is not valid.")

        if destination_path and not os.path.isdir(os.path.dirname(destination_path)):
            raise Exception("ERROR", f"The destination path {destination_path} is not valid.")

        self.force = force
        self.single = single
        if force:
            if destination_path is not None and destination_path != root_path:
                self.delete_tree(destination_path)
            else:
                raise Exception("ERROR", f"Can delete de {root_path}. Its the Root Path.")

        if single:
            if not destination_path:
                # Get root directory
                destination_path = os.path.dirname(root_path)
                # Remove the last dir and set de niu dir
                destination_path = os.path.dirname(destination_path) + "/md_toc_single"

            if not os.path.exists(destination_path):
                os.makedirs(destination_path, exist_ok=True)
            shutil.copy(root_path, destination_path)
            root_path = destination_path

        super().__init__(root_path, destination_path=destination_path, ignore=ignore, output_toc_filename=output_toc_filename, toc_files=toc_files, rm_toc_files=rm_toc_files)

    def delete_tree(self, abs_path):
        """
        Delete folder with content on it.
        :param abs_path:
        """
        try:
            shutil.rmtree(abs_path)
        except OSError as e:
            msg = f"The path {abs_path} can be deleted.\n\n{e.strerror}"
            logger.error(msg)
            raise Exception("ERROR", )