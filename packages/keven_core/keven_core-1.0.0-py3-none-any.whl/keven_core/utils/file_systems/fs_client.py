import logging
import os
import re

from enum import Enum
from typing import List, Optional


class FilepathType(Enum):
    """Different types of file paths"""
    NO_PATH = 0
    FILE = 1
    DIRECTORY = 2


class FileSystemClient:
    """
    The FileSystemClient class is designed to abstract and simplify file system operations by providing methods for
    file handling, directory management, and path manipulation. It centralizes file I/O operations, ensuring
    consistent handling of file paths, automatic directory creation, and support for file extensions.

    Key Features
        Path Management
            _get_full_path() ensures correct resolution of file paths.
            _force_extension() ensures that files use the expected extension if specified.
            path_type() identifies if a given path is a file, directory, or non-existent.
            list() retrieves files in a directory (non-recursively).

        File Operations
            open() safely opens files and ensures their directories exist.
            read(), write(), and update() provide structured access to file contents.
            quick_write() and quick_read() offer simplified one-liner read/write operations.
            delete() removes a file from the system.

        Resource Management
            close() ensures file handles are closed properly.
            close_all() prevents resource leaks by closing all open file handles.
    """

    def __init__(self, host: str, root_folder: str = "/", extension: Optional[str] = None):
        """
        Initializes the FileSystemClient.

        :param host: Host where the file system is located (currently unused, reserved for future remote FS support).
        :param root_folder: The root directory for file operations.
        :param extension: Optional file extension enforcement.
        """
        self.host_address = host  # Placeholder for remote FS support (currently unused)

        # Normalize root folder path
        if not root_folder:
            root_folder = "/"
        elif root_folder.startswith("."):
            root_folder = os.path.abspath(root_folder) + "/"
        elif not root_folder.endswith("/"):
            root_folder += "/"

        self.root_folder = root_folder
        self.extension = extension
        self.open_file_handles = []

        logging.info(f"Initialized FileSystemClient with root: {self.root_folder}")

    def _get_full_path(self, file_path: str) -> str:
        """
        Generates an absolute path by prepending the root folder.

        :param file_path: Relative or absolute file path.
        :return: Absolute file path.
        """
        file_path = file_path.lstrip("/")  # Ensure no double leading slashes
        full_path = os.path.join(self.root_folder, file_path)

        # Clean up redundant slashes and dots
        full_path = re.sub(r'//+', '/', full_path)
        full_path = re.sub(r'/\.$', '', full_path)
        full_path = os.path.abspath(full_path)

        return full_path

    def _force_extension(self, file_path: str) -> str:
        """
        Ensures the specified file extension is applied if configured.

        :param file_path: Original file path.
        :return: File path with the enforced extension.
        """
        if not self.extension:
            return file_path

        base, ext = os.path.splitext(file_path)
        if ext:
            return f"{base}.{self.extension}"
        return f"{file_path}.{self.extension}"

    def open(self, file_path: str, mode: str):
        """
        Opens a file, creating parent directories if needed.

        :param file_path: Path to the file.
        :param mode: File mode ('r', 'w', 'a', etc.).
        :return: File handle.
        """
        full_path = self._force_extension(self._get_full_path(file_path))
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        try:
            handle = open(full_path, mode)
            self.open_file_handles.append(handle)
            return handle
        except IOError as e:
            logging.error(f"Failed to open file {full_path}: {e}")
            raise

    def read(self, file_handle) -> str:
        """Reads the entire content of an open file."""
        return file_handle.read()

    def write(self, file_handle, content: str):
        """Writes content to an open file."""
        file_handle.write(content)

    def update(self, file_handle, content: str):
        """
        Overwrites the content of an open file.

        :param file_handle: Open file handle.
        :param content: New content.
        """
        file_handle.seek(0)
        file_handle.write(content)
        file_handle.truncate()

    def delete(self, file_path: str):
        """
        Deletes a file safely.

        :param file_path: Path to the file.
        """
        full_path = self._force_extension(self._get_full_path(file_path))

        try:
            os.remove(full_path)
            logging.info(f"Deleted file: {full_path}")
        except FileNotFoundError:
            logging.warning(f"Attempted to delete non-existent file: {full_path}")
        except PermissionError:
            logging.error(f"Permission denied: Cannot delete {full_path}")
            raise

    def close(self, file_handle):
        """Closes a file handle safely."""
        try:
            file_handle.close()
            self.open_file_handles.remove(file_handle)
        except ValueError:
            logging.warning("Attempted to close an already closed file handle.")

    def close_all(self):
        """Closes all open file handles."""
        for handle in self.open_file_handles[:]:
            self.close(handle)

    def quick_write(self, file_path: str, content: str):
        """Writes content to a file and closes it."""
        with self.open(file_path, "w") as handle:
            handle.write(content)

    def quick_read(self, file_path: str) -> str:
        """Reads content from a file and closes it."""
        with self.open(file_path, "r") as handle:
            return handle.read()

    def path_type(self, path: str) -> FilepathType:
        """
        Determines if a path is a file, directory, or does not exist.

        :param path: Path to check.
        :return: Enum representing the type.
        """
        full_path = self._get_full_path(path)
        if os.path.isfile(full_path):
            return FilepathType.FILE
        if os.path.isdir(full_path):
            return FilepathType.DIRECTORY
        return FilepathType.NO_PATH

    def list(self, path: str, recursive: bool = False) -> List[str]:
        """
        Lists files in a directory, with optional recursion.

        :param path: Directory path.
        :param recursive: Whether to list files recursively.
        :return: List of file names.
        """
        full_path = self._get_full_path(path)

        if not os.path.isdir(full_path):
            raise ValueError(f"Path is not a directory: {full_path}")

        if recursive:
            return [
                os.path.relpath(os.path.join(root, file), full_path)
                for root, _, files in os.walk(full_path)
                for file in files
            ]

        return os.listdir(full_path)
