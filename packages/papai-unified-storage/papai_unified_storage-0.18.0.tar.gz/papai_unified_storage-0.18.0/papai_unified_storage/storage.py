from contextlib import contextmanager
from io import BytesIO, StringIO, TextIOWrapper
from typing import Any, Callable, Literal, overload

import fsspec
import pandas as pd
import pyarrow
import pyarrow.parquet
from fsspec import AbstractFileSystem
from fsspec.spec import AbstractBufferedFile

from .utils import (
    GlobPath,
    StorageError,
    convert_decimal_columns_to_double_with_arrow_casting,
    create_dir_tree,
    dummy_fn,
)


def filesystem(
    protocol: str,
    logging_debug_function: Callable = dummy_fn,
    logging_error_function: Callable = dummy_fn,
    **storage_options,
):
    """Generate a supercharged fsspec storage instance for a given protocol.

    Parameters
    ----------
    protocol : str
        name of the protocol to use. See options at
        https://filesystem-spec.readthedocs.io/en/latest/api.html#built-in-implementations
    logging_debug_function : Callable, optional
        Function to use to log operations. Its first argument must be a
        string, by default dummy_fn, which does nothing.
    logging_error_function : Callable, optional
        Function to use to log errors. Its first argument must be a
        string, by default dummy_fn, which does nothing.
    Returns
    -------
    Storage(fsspec.AbstractFileSystem)
        Supercharged fsspec storage instance.
    """
    internal_fs_class = fsspec.get_filesystem_class(protocol)
    internal_fs = get_storage_wrapper(internal_fs_class, storage_options)
    fs = Storage(internal_fs, logging_debug_function, logging_error_function)
    return fs


def get_storage_wrapper(storage_class: AbstractFileSystem, storage_options):
    class FileSystemWrapper(storage_class):
        def get_file(self, rpath, lpath, **kwargs):
            create_dir_tree(fsspec.filesystem("file"), lpath)
            super().get_file(rpath, lpath, **kwargs)

        def put_file(self, lpath, rpath, **kwargs):
            create_dir_tree(self, rpath)
            super().put_file(lpath, rpath, **kwargs)

    return FileSystemWrapper(**storage_options)


class Storage:
    def __init__(
        self,
        filesystem: AbstractFileSystem,
        logging_debug_function: Callable = dummy_fn,
        logging_error_function: Callable = dummy_fn,
    ):
        """Create storage proxy to a remote file system.

        Parameters
        ----------
        logging_debug_function : Callable, optional
            Function to use to log operations. Its first argument must be a
            string, by default dummy_fn, which does nothing.
        logging_error_function : Callable, optional
            Function to use to log errors. Its first argument must be a
            string, by default dummy_fn, which does nothing.
        """
        self.filesystem = filesystem
        self.log_debug_fn = logging_debug_function
        self.log_error_fn = logging_error_function

    @contextmanager
    def disable_debug_logging(self):
        old_debug_fn = self.log_debug_fn
        self.log_debug_fn = dummy_fn
        yield
        self.log_debug_fn = old_debug_fn

    @contextmanager
    def error_logging(self, error_msg: str):
        try:
            yield
        except Exception as exc:
            self.log_error_fn(error_msg)
            raise StorageError(error_msg) from exc

    @overload
    def get(
        self,
        remote_path: str | list[str] | GlobPath | list[GlobPath],
        local_path: str,
        recursive: bool = False,
    ): ...
    @overload
    def get(self, remote_path: list[str], local_path: list[str], recursive: bool = False): ...
    def get(self, remote_path, local_path, recursive=False):
        """Copy remote file(s) to local.

        Copies a specific file or tree of files (if recursive=True). If
        rpath ends with a "/", it will be assumed to be a directory, and
        target files will go within. Can submit a list of paths, which may
        be glob-patterns and will be expanded.

        If both remote_path and local_path are lists, they must be the same
        length and paths will not be expanded. That means that you can't
        download a folder recursively to different location than the rest.

        If you set recursive=True, then remote_paths that are folders
        will be downloaded recursively. If you use a glob pattern in a
        remote_path (e.g. `folder/*`), it will download the folder `folder`
        recursively, but not the other non-glob pattern path of `remote_path`.

        Calls get_file for each source.

        Examples
        --------
        >>> fs.get(["file1", "folder"], "download", recursive=True)
        >>> pathlib.Path("download").rglob('*')
        [download/file1, download/folder/file2]
        >>> fs.get(["file1", "folder/**"], "download", recursive=False)
        >>> pathlib.Path("download").rglob('*')
        [download/file1, download/folder/file2]
        >>> # You can't download a folder at a different location than the rest
        >>> fs.get(["file1", "folder/*"], ["download/1/file1", "download/2/"])
        >>> pathlib.Path("download").rglob('*')
        [download/1/file1, download/2/]
        >>> fs.get("file1", "download/path/to/file")
        >>> pathlib.Path("download").rglob('*')
        [download/path/to/file]
        """
        base_log_msg = f"remote file(s) at {remote_path} to local at {local_path}"
        self.log_debug_fn(f"Copying {base_log_msg}")
        with self.error_logging(f"Failed to copy {base_log_msg}"):
            return self.filesystem.get(remote_path, local_path, recursive)

    def get_file(self, rpath, lpath, **kwargs):
        base_log_msg = f"remote file at {rpath} to local at {lpath}"
        self.log_debug_fn(f"Copying {base_log_msg}")
        with self.error_logging(f"Failed to copy {base_log_msg}"):
            return self.filesystem.get_file(rpath, lpath, **kwargs)

    def put(self, local_path: str | list[str], remote_path: str | list[str], recursive=False):
        """Copy file(s) from local to remote.

        Copies a specific file or tree of files (if recursive=True). If
        rpath ends with a "/", it will be assumed to be a directory, and
        target files will go within. Can submit a list of paths, which may
        be glob-patterns and will be expanded.

        If both remote_path and local_path are lists, they must be the same
        length and paths will not be expanded. That means that you can't
        upload a folder recursively to different location than the rest.

        If you set recursive=True, then local_paths that are folders
        will be uploaded recursively. If you use a glob pattern in a
        local_path (e.g. `folder/*`), it will upload the folder `folder`
        recursively, but not the other non-glob pattern path of `local_path`.

        Calls put_file for each source.

        Examples
        --------
        >>> fs.put(["file1", "folder"], "upload", recursive=True)
        >>> fs.glob('upload/**')
        [upload/file1, upload/folder/file2]
        >>> fs.put(["file1", "folder/**"], "upload", recursive=False)
        >>> fs.glob('upload/**')
        [upload/file1, upload/folder/file2]
        >>> # You can't upload a folder at a different location than the rest
        >>> fs.put(["file1", "folder/"], ["upload/1/file1", "upload/2/"], recursively=True)
        >>> fs.glob('upload/**')
        []
        >>> fs.put("file1", "upload/path/to/file")
        >>> fs.glob('upload/**')
        [upload/path/to/file]
        """
        base_log_msg = f"local file(s) at {local_path} to remote at {remote_path}"
        self.log_debug_fn(f"Copying {base_log_msg}")
        with self.error_logging(f"Failed to copy {base_log_msg}"):
            return self.filesystem.put(local_path, remote_path, recursive)

    def put_file(self, lpath, rpath, **kwargs):
        base_log_msg = f"local file at {lpath} to remote at {rpath}"
        self.log_debug_fn(f"Copying {base_log_msg}")
        with self.error_logging(f"Failed to copy {base_log_msg}"):
            return self.filesystem.put_file(lpath, rpath, **kwargs)

    def open(self, path: str, mode: str, **kwargs):
        base_log_msg = f"remote file at {path} with {mode=}"
        self.log_debug_fn(f"Opening {base_log_msg}")
        with self.error_logging(f"Failed to open {base_log_msg}"):
            return self.filesystem.open(path, mode, **kwargs)

    def open_for_writing(
        self, path: str, text: bool = False
    ) -> TextIOWrapper | AbstractBufferedFile:
        """Open a remote file for writing.

        Parameters
        ----------
        path : str
            Path to the file to open.
        text : bool, optional
            Whether to open it in text mode (when `text = True`) or binary mode
            (when `text = False`), by default False

        Examples
        --------
        >>> with fs.open_for_writing("file.txt") as f:
        ...     f.write("Hello, world!")
        >>> with fs.open_for_writing("model.joblib") as f:
        ...     joblib.dump(model, f)
        """
        mode = "wb" if text is False else "w"
        return self.open(path, mode)

    def open_for_reading(
        self, path: str, text: bool = False
    ) -> TextIOWrapper | AbstractBufferedFile:
        mode = "rb" if text is False else "r"
        return self.open(path, mode)

    def move(self, source_path: str, destination_path: str):
        """Move file(s) from one location to another.

        This fails if the target file system is not capable of creating the
        directory, for example if it is write-only or if auto_mkdir=False. There is
        no command line equivalent of this scenario without an explicit mkdir to
        create the new directory.
        See https://filesystem-spec.readthedocs.io/en/latest/copying.html for more
        information.
        """
        base_log_msg = f"remote file(s) from {source_path} to {destination_path}"
        self.log_debug_fn(f"Moving {base_log_msg}")
        with self.error_logging(f"Failed to move {base_log_msg}"):
            return self.filesystem.mv(source_path, destination_path)

    def _remove_prefix(
        self, files: list[str], remove_root_folder: bool = True, remove_prefix: str | None = None
    ):
        if remove_root_folder is True:
            files = [file.lstrip("/").partition("/")[2] for file in files]

        if remove_prefix is not None:
            files = [
                (file.replace(remove_prefix, "", 1) if file.startswith(remove_prefix) else file)
                for file in files
            ]

        return files

    @overload
    def list_files(
        self,
        path: str,
        recursive: bool = False,
        remove_root_folder: bool = False,
        remove_prefix: str | None = None,
        detail: Literal[False] = False,
    ) -> list[str]: ...
    @overload
    def list_files(
        self,
        path: str,
        recursive: bool = False,
        remove_root_folder: bool = False,
        remove_prefix: str | None = None,
        detail: Literal[True] = True,
    ) -> dict[str, dict[str, Any]]: ...
    def list_files(
        self, path, recursive=False, remove_root_folder=False, remove_prefix=None, detail=False
    ):
        """List files in a remote directory.

        Parameters
        ----------
        path : str
            Path at which to list objects.
        recursive : bool, optional
            Whether to list objects that are deeper than `path`,
            by default False.
        remove_root_folder : bool, optional
            Whether to remove the root folder of `path` in the results,
            by default False.
        remove_prefix : str, optional
            If not None, will remove prefix `remove_prefix` from the results,
            by default None.
        detail : bool, optional
            If True, return a list of dictionaries with details about the
            files. It also disables the `remove_root_folder` and
            `remove_prefix` options. By default False.

        Returns
        -------
        list[str]
            List of objects that exist under `path`.
        """
        if recursive is True:
            maxdepth = None
        else:
            maxdepth = 1

        base_log_msg = f"remote files at {path}"
        self.log_debug_fn(f"Listing {base_log_msg}")
        with self.error_logging(f"Failed to list {base_log_msg}"):
            files = self.filesystem.find(path, maxdepth, detail=detail)

        if detail is False:
            files = self._remove_prefix(files, remove_root_folder, remove_prefix)
        return files

    @overload
    def glob_files(
        self,
        pattern: str,
        remove_root_folder: bool = False,
        remove_prefix: str | None = None,
        detail: Literal[False] = False,
    ) -> list[str]: ...
    @overload
    def glob_files(
        self,
        pattern: str,
        remove_root_folder: bool = False,
        remove_prefix: str | None = None,
        detail: Literal[True] = True,
    ) -> dict[str, dict[str, Any]]: ...
    def glob_files(self, pattern, remove_root_folder=False, remove_prefix=None, detail=False):
        """List files in a remote directory that match a pattern.

        Parameters
        ----------
        pattern : str
            pattern to list objects with.
        remove_root_folder : bool, optional
            Whether to remove the root folder of `path` in the results,
            by default False.
        remove_prefix : str, optional
            If not None, will remove prefix `remove_prefix` from the results,
            by default None.
        detail : bool, optional
            If True, return a list of dictionaries with details about the
            files. It also disables the `remove_root_folder` and
            `remove_prefix` options. By default False.

        Returns
        -------
        list[str]
            List of objects that matches `pattern`.
        """
        base_log_msg = f"remote files matching {pattern}"
        self.log_debug_fn(f"Listing {base_log_msg}")
        with self.error_logging(f"Failed to list {base_log_msg}"):
            files = self.filesystem.glob(pattern, detail=detail)

        if detail is False:
            files = self._remove_prefix(files, remove_root_folder, remove_prefix)
        return files

    def remove_files(self, paths: str | list[str], recursive: bool = False):
        base_log_msg = f"remote file(s) at {paths}"
        self.log_debug_fn(f"Removing {base_log_msg}")
        with self.error_logging(f"Failed to remove {base_log_msg}"):
            return self.filesystem.rm(paths, recursive)

    def read_dataset_from_parquet(self, path: str) -> pd.DataFrame:
        base_log_msg = f"remote dataset from {path}"
        self.log_debug_fn(f"Reading {base_log_msg}")
        with self.error_logging(f"Failed to read {base_log_msg}"):
            parquet = pyarrow.parquet.ParquetDataset(path, filesystem=self.filesystem)

        table = parquet.read_pandas()
        table = convert_decimal_columns_to_double_with_arrow_casting(table)
        return table.to_pandas()

    def write_dataframe_to_parquet(self, path: str, df: pd.DataFrame):
        base_log_msg = f"remote dataset to {path}"
        self.log_debug_fn(f"Writing {base_log_msg}")

        table = pyarrow.Table.from_pandas(df)
        with self.error_logging(f"Failed to write {base_log_msg}"):
            return pyarrow.parquet.write_table(table, path, filesystem=self.filesystem)

    def loader(self, path: str, load_method: Callable, text: bool = False) -> object:
        """Loads an object from a remote file using the provided loading function.

        Parameters
        ----------
        path : str
            Path to the object to load.
        load_method : Callable
            Method to use to load the object.
        text : bool, optional
            Whether to open it in text mode (when `text = True`) or binary mode
            (when `text = False`), by default False

        Returns
        -------
        object
            object loaded by the `load_method`.

        Examples
        --------
        >>> data = fs.loader("file.json", json.load)
        >>> data
        {'key': 'value'}
        >>> dataset = fs.loader("file.parquet", pd.read_parquet)
        >>> type(dataset)
        <class 'pandas.core.frame.DataFrame'>
        """
        base_log_msg = f"object with {load_method.__name__} from remote file at {path}"
        self.log_debug_fn(f"Loading {base_log_msg}")

        mode = "rb" if text is False else "r"

        with self.disable_debug_logging():
            with self.error_logging(f"Failed to load {base_log_msg}"):
                with self.filesystem.open(path, mode) as f:
                    return load_method(f)

    def write_to_file(self, path: str, content: str | bytes | BytesIO | StringIO):
        """Write content to a remote file.

        Parameters
        ----------
        path : str
            Path to the file to write.
        content : str | bytes | BytesIO | StringIO
            Content to write to the file.
        """
        base_log_msg = f"content to remote file at {path}"
        self.log_debug_fn(f"Writing {base_log_msg}")

        if isinstance(content, (str, StringIO)):
            mode = "w"
        else:
            mode = "wb"

        if isinstance(content, (BytesIO, StringIO)):
            content.seek(0)
            content = content.read()

        create_dir_tree(self.filesystem, path)

        with self.disable_debug_logging():
            with self.error_logging(f"Failed to write {base_log_msg}"):
                with self.filesystem.open(path, mode) as f:
                    # f.write actually supports both str and bytes
                    f.write(content)  # type: ignore[arg-type]

    def exists(self, path: str) -> bool:
        """Check if a file exists in the remote file system."""
        return self.filesystem.exists(path)
