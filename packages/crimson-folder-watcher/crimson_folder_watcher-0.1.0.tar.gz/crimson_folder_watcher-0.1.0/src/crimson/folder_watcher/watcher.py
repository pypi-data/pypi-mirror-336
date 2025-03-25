import os
from typing import List, Union
from watchdog.observers import Observer

from .watch_handler import WatchHandler
from .file_editor import FileEditor, FileEditorFunc


class FolderWatcher:
    """
    Watches a source directory and processes file changes by copying
    to an output directory with optional editing.
    """

    def __init__(
        self,
        source_dir: str,
        output_dir: str,
        include: Union[str, List[str], None] = None,
        exclude: Union[str, List[str], None] = None,
    ):
        """
        Initialize the folder watcher.

        Args:
            source_dir: Directory to watch for changes
            output_dir: Directory to copy files to
            include: Pattern(s) of files to include
            exclude: Pattern(s) of files to exclude
        """
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.include = include
        self.exclude = exclude

        # Initialize the file editor
        self.file_editor = FileEditor()

        # Create handler and observer
        self.handler = WatchHandler(
            source_dir=self.source_dir,
            output_dir=self.output_dir,
            include=self.include,
            exclude=self.exclude,
            file_editor=self.file_editor,
        )

        self.observer = Observer()
        self.observer.schedule(self.handler, path=self.source_dir, recursive=True)

    def register_editor(self, pattern: str, edit_func: FileEditorFunc) -> None:
        """
        Register a file editor function for files matching a pattern.

        Args:
            pattern: File pattern to match (uses fnmatch syntax)
            edit_func: Function that accepts (src_path, content) and returns modified content
        """
        self.file_editor.register(pattern, edit_func)

    def start(self) -> None:
        """Start watching the source directory."""
        if not os.path.exists(self.source_dir):
            raise FileNotFoundError(
                f"Source directory '{self.source_dir}' does not exist."
            )

        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

        self.observer.start()
        print(f"Watching '{self.source_dir}' for changes...")

    def stop(self) -> None:
        """Stop watching the source directory."""
        self.observer.stop()
        self.observer.join()
        print("Stopped watching for changes.")

    def process_existing_files(self) -> None:
        """
        Process all existing files in the source directory.

        Args:
            force: If True, process all files even if they already
                  exist in the output directory.
        """
        print("Processing existing files...")
        processed_count = 0

        for root, _, files in os.walk(self.source_dir):
            for file in files:
                src_path = os.path.join(root, file)

                self.handler._process_file(src_path)
                processed_count += 1

        print(f"Processed {processed_count} existing files.")

    def get_status(self) -> dict:
        """
        Get detailed status information about the watcher.

        Returns:
            dict: A dictionary containing status information:
                - running: Whether the watcher is running
                - source_dir: The source directory being watched
                - output_dir: The output directory for processed files
                - observer_alive: Whether the observer thread is alive
                - include_patterns: File patterns to include
                - exclude_patterns: File patterns to exclude
        """
        return {
            "running": self.observer.is_alive() if hasattr(self.observer, "is_alive") else False,
            "source_dir": self.source_dir,
            "output_dir": self.output_dir,
            "observer_alive": (
                self.observer.is_alive() if hasattr(self.observer, "is_alive") else None
            ),
            "include_patterns": self.include,
            "exclude_patterns": self.exclude,
        }


def create_watcher(
    source_dir: str,
    output_dir: str,
    include: Union[str, List[str], None] = None,
    exclude: Union[str, List[str], None] = None,
    process_existing: bool = False,
    auto_start: bool = False,
) -> FolderWatcher:
    """
    Create and configure a FolderWatcher instance.

    Args:
        source_dir: Directory to watch for changes
        output_dir: Directory to copy files to
        include: Pattern(s) of files to include
        exclude: Pattern(s) of files to exclude
        process_existing: Whether to process existing files immediately
        auto_start: Whether to start watching immediately

    Returns:
        Configured FolderWatcher instance
    """
    watcher = FolderWatcher(
        source_dir=source_dir,
        output_dir=output_dir,
        include=include,
        exclude=exclude,
    )

    if process_existing:
        watcher.process_existing_files()

    if auto_start:
        watcher.start()

    return watcher
