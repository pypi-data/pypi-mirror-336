import logging
import os
from typing import Dict, Optional
from pathlib import Path

LARGE_ATTRIBUTE_BYTES_THRESHOLD_DEFAULT = 1024 * 1024  # 1 Megabyte
LARGE_ATTRIBUTE_VERBOSE_DEFAULT = "0"

class LargeAttributeManager:
    """
    Manages the offloading of large message attributes to the file system
    to optimize memory usage in event-driven architectures.

    - Automatically writes large attributes to disk when exceeding a size threshold.
    - Stores the file path inside the message instead of the actual content.
    - Reloads the original content into the message when needed.
    - Uses FileSystemClient for efficient file operations.
    """

    def __init__(self, large_attribute_host: str,
                 large_attribute_folder: str,
                 large_attribute_partition: str,
                 large_attribute_bytes_threshold: Optional[int] =
                 LARGE_ATTRIBUTE_BYTES_THRESHOLD_DEFAULT):
        """
        Initializes the LargeAttributeManager.

        :param large_attribute_host: Host where file storage is located (local or remote).
        :param large_attribute_folder: Root folder for storing offloaded attributes.
        :param large_attribute_partition: Name of an attribute used to create partitioned directories.
        :param large_attribute_bytes_threshold: Byte size threshold for offloading (default: LARGE_ATTRIBUTE_BYTES_THRESHOLD_DEFAULT bytes).
        """
        from keven_core.utils.file_systems.fs_client import FileSystemClient

        self.host = large_attribute_host
        self.folder = Path(large_attribute_folder).resolve()
        self.partition = large_attribute_partition
        self.bytes_threshold = int(large_attribute_bytes_threshold) if large_attribute_bytes_threshold else 64
        self.file_system_client = FileSystemClient(large_attribute_host)

        # Verbose logging control
        self.full_verbose = os.getenv("LARGE_ATTRIBUTE_VERBOSE", LARGE_ATTRIBUTE_VERBOSE_DEFAULT) == "1"

        logging.info(f"LargeAttributeManager initialized with folder: {self.folder}, "
                     f"partition key: {self.partition}, threshold: {self.bytes_threshold} bytes")

    def offload(self, message: "Message") -> Dict[str, str]:
        """
        Offloads large attributes from the given message.

        :param message: The message object containing attributes.
        :return: Dictionary mapping offloaded attribute names to their original values.
        """
        from keven_core.kafka.abstracts.message import Message

        self._verbose_log(message, "offload", "before")

        original_values = {}
        if hasattr(message.__class__, "large_attributes"):
            for attr_name in message.__class__.large_attributes or []:
                if self._write(message, attr_name):
                    original_values[attr_name] = getattr(message.details, attr_name, "")

        self._verbose_log(message, "offload", "after")

        return original_values

    def restore(self, message: "Message", original_values: Dict[str, str]) -> None:
        """
        Restores the original large attribute values back into the message.

        :param message: The message object.
        :param original_values: Dictionary of offloaded attributes to restore.
        """
        if hasattr(message, "details"):
            for attr_name, original_value in original_values.items():
                setattr(message.details, attr_name, original_value)

    def reload(self, message: "Message") -> None:
        """
        Reloads all offloaded attributes from storage back into the message.

        :param message: The message object.
        """
        from keven_core.kafka.abstracts.message import Message
        self._verbose_log(message, "reload", "before")

        if hasattr(message, "details") and hasattr(message.details, "offloads"):
            for attr_name in message.details.offloads.split(","):
                attr_name = attr_name.strip()
                if attr_name:
                    self._read(message, attr_name)
            delattr(message.details, "offloads")

        self._verbose_log(message, "reload", "after")

    def _write(self, message: "Message", attr_name: str) -> bool:
        """
        Writes a large attribute to disk and replaces it with the file path.

        :param message: The message object.
        :param attr_name: The name of the attribute to offload.
        :return: True if offloaded, False otherwise.
        """
        if not hasattr(message, "details") or not hasattr(message.details, attr_name):
            return False

        value = getattr(message.details, attr_name)
        if not isinstance(value, (str, bytes)):
            return False  # Only offload valid content
        elif ((isinstance(value, str) and len(value.encode('utf-8')) <= self.bytes_threshold) or
              (isinstance(value, bytes) and len(value) <= self.bytes_threshold)):
            return False  #  Size does not exceed threshold

        partition_value = getattr(message.details, self.partition, "")
        partition_path = Path(self.folder, str(partition_value)).resolve()
        partition_path.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

        file_path = partition_path / f"{message._uuid}_{attr_name}.la"

        try:
            self.file_system_client.quick_write(str(file_path), value)
            setattr(message.details, attr_name, str(file_path))  # Store file path in message

            # Track offloaded attributes
            offloads = getattr(message.details, "offloads", "").strip()
            setattr(message.details, "offloads", f"{offloads}, {attr_name}".strip(", "))

            return True
        except Exception as e:
            logging.error(f"Failed to offload {attr_name}: {e}")
            return False

    def _read(self, message: "Message", attr_name: str) -> None:
        """
        Reads a previously offloaded attribute from disk and restores it.

        :param message: The message object.
        :param attr_name: The name of the attribute to restore.
        """
        if not hasattr(message, "details") or not hasattr(message.details, attr_name):
            return

        file_path = getattr(message.details, attr_name)

        if not Path(file_path).is_file():
            logging.error(f"File not found for attribute {attr_name}: {file_path}")
            return

        try:
            content = self.file_system_client.quick_read(str(file_path))
            setattr(message.details, attr_name, content)
        except Exception as e:
            logging.error(f"Failed to read offloaded attribute {attr_name}: {e}")

    def _verbose_log(self, message: "Message", function_name: str, when: str) -> None:
        """Handles verbose logging based on the configuration."""
        if not self.full_verbose or not hasattr(message, "details"):
            return

        try:
            logging.debug(f"LargeAttributeManager.{function_name}()/{when}: {message.details}")
        except Exception:
            pass  # Suppress logging errors due to unserializable message contents
