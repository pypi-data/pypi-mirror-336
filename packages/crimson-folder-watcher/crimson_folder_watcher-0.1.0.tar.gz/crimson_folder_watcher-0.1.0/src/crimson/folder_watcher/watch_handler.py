import os
from typing import List, Union, Optional
from watchdog.events import FileSystemEventHandler
from .filter import filter_path
from .file_editor import FileEditor


class WatchHandler(FileSystemEventHandler):
    """
    Handler for file system events to process file changes.
    """

    def __init__(
        self,
        source_dir: str,
        output_dir: str,
        include: Union[str, List[str], None] = None,
        exclude: Union[str, List[str], None] = None,
        file_editor: Optional[FileEditor] = None,
    ):
        """
        Initialize the watch handler.

        Args:
            source_dir: Directory to watch for changes
            output_dir: Directory to copy/edit files to
            include: Pattern(s) of files to include
            exclude: Pattern(s) of files to exclude
            file_editor: Optional FileEditor instance for editing files
        """
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.include = include
        self.exclude = exclude
        self.file_editor = file_editor or FileEditor()
        self.cwd = os.getcwd()

    def on_modified(self, event) -> None:
        """Handle file modification events."""
        if not event.is_directory:
            self._process_file(event.src_path)

    def on_created(self, event) -> None:
        """Handle file creation events."""
        if not event.is_directory:
            self._process_file(event.src_path)

    def on_deleted(self, event) -> None:
        """Handle file deletion events."""
        if not event.is_directory:
            self._delete_file(event.src_path)

    def _process_file(self, src_path: str) -> None:
        """Process a file change by copying or editing the file."""
        filtered_path = filter_path(src_path, self.include, self.exclude)
        if filtered_path is None:
            return

        if self.file_editor:
            edited, final_dest_path = self.file_editor.edit_file(
                src_path, self.source_dir, self.output_dir
            )

            if edited:
                print(f"Edited and saved '{src_path}' to '{final_dest_path}'")
                return

    def _delete_file(self, src_path: str) -> None:
        """Delete a file from the output directory when it's deleted from source."""
        filtered_path = filter_path(src_path, self.include, self.exclude)
        if filtered_path is None:
            return

        relative_path = os.path.relpath(src_path, self.source_dir)
        destination_path = os.path.join(self.output_dir, relative_path)

        if os.path.exists(destination_path):
            try:
                os.remove(destination_path)
                rel_dst_path = os.path.relpath(destination_path, self.cwd)
                print(f"Deleted './{rel_dst_path}'")
            except Exception as e:
                print(f"Error deleting file: {e}")
