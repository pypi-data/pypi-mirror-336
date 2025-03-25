from typing import List, Union, Optional
import fnmatch


def filter_path(
    path: str,
    include: Union[str, List[str], None] = None,
    exclude: Union[str, List[str], None] = None,
) -> Optional[str]:
    """
    Filter a path based on include and exclude patterns.

    Args:
        path: The path to filter.
        include: Pattern(s) to include. If None or empty, all paths are included.
        exclude: Pattern(s) to exclude. If None or empty, no paths are excluded.

    Returns:
        The original path if it passes the filter, None otherwise.
    """
    # Convert single string patterns to lists
    include_list = [include] if isinstance(include, str) else include or []
    exclude_list = [exclude] if isinstance(exclude, str) else exclude or []

    # Remove empty patterns
    include_list = [p for p in include_list if p]
    exclude_list = [p for p in exclude_list if p]

    # If include list is not empty, path must match at least one pattern
    if include_list and not any(
        fnmatch.fnmatch(path, pattern) for pattern in include_list
    ):
        return None

    # If path matches any exclude pattern, filter it out
    if any(fnmatch.fnmatch(path, pattern) for pattern in exclude_list):
        return None

    return path


def filter_paths(
    paths: List[str],
    include: Union[str, List[str], None] = None,
    exclude: Union[str, List[str], None] = None,
) -> List[str]:
    """
    Filter a list of paths based on include and exclude patterns.

    Args:
        paths: List of paths to filter.
        include: Pattern(s) to include.
        exclude: Pattern(s) to exclude.

    Returns:
        List of paths that pass the filter.
    """
    return [path for path in paths if filter_path(path, include, exclude) is not None]
