import concurrent.futures
import io
import logging
from collections.abc import Callable
from dataclasses import dataclass
from queue import Queue
from threading import Thread
from typing import IO

__all__ = []


@dataclass
class PathData:
    """Manages an I
    O job queue and polling thread for a single path.

    Notes
    -----
    Ensures writes to the same path are serialized.

    """

    queue: Queue
    thread: Thread


class NonBlockingIOManager:
    """Manages all async I
    O calls made by `opena` calls.

    Notes
    -----
    Assigns each path to a polling thread and queue.

    """

    def __init__(
        self,
        buffered: bool | None = False,
        executor: concurrent.futures.Executor | None = None,
    ) -> None:
        """Args:
        buffered (bool): IO instances will be `NonBlockingBufferedIO`
            or `NonBlockingIO` based on this value. This bool is set
            manually for each `PathHandler` in `_opena`.
        executor: User can optionally attach a custom executor to
            perform async operations through `PathHandler.__init__`.

        """
        self._path_to_data = {}  # Map from path to `PathData` object
        self._buffered = buffered
        self._IO = NonBlockingBufferedIO if self._buffered else NonBlockingIO

        self._pool = executor or concurrent.futures.ThreadPoolExecutor()

    def get_non_blocking_io(
        self,
        path: str,
        io_obj: IO[str] | IO[bytes],
        callback_after_file_close: Callable[[None], None] | None = None,
        buffering: int | None = -1,
    ) -> io.IOBase:
        """Return a NonBlockingIO instance for asynchronous operations.

        Parameters
        ----------
        path : str
        io_obj : IO
        callback_after_file_close : Callable or None
        buffering : int

        Returns
        -------
        io.IOBase
            A non-blocking IO object

        """
        if not self._buffered and buffering != -1:
            msg = (
                "NonBlockingIO is not using a buffered writer but `buffering` "
                f"arg is set to non-default value of {buffering} != -1."
            )
            raise ValueError(
                msg,
            )

        if path not in self._path_to_data:
            # Initialize job queue and a polling thread
            queue = Queue()
            t = Thread(target=self._poll_jobs, args=(queue,))
            t.start()
            # Store the `PathData`
            self._path_to_data[path] = PathData(queue, t)

        kwargs = {} if not self._buffered else {"buffering": buffering}

        #  a function.
        return self._IO(
            notify_manager=lambda io_callable: (  # Pass async jobs to manager
                self._path_to_data[path].queue.put(io_callable)
            ),
            io_obj=io_obj,
            callback_after_file_close=callback_after_file_close,
            **kwargs,
        )

    def _poll_jobs(self, queue: Callable[[], None] | None) -> None:
        """Process queued I
        O jobs sequentially.

        Parameters
        ----------
        queue : Queue
            Queue of I/O callables

        """
        while True:
            # `func` is a callable function (specifically a lambda function)
            # and can be any of:
            #   - func = file.write(b)
            #   - func = file.close()
            #   - func = None

            func = queue.get()  # Blocks until item read.
            if func is None:  # Thread join signal.
                break
            self._pool.submit(func).result()  # Wait for job to finish.

    def _join(self, path: str | None = None) -> bool:
        """Wait for write jobs to finish.

        Parameters
        ----------
        path : str or None
            Specific path or all paths

        Returns
        -------
        bool
            True on success

        """
        if path and path not in self._path_to_data:
            msg = (
                f"{path} has no async IO associated with it. "
                f"Make sure `opena({path})` is called first."
            )
            raise ValueError(
                msg,
            )
        # If a `_close` call fails, we print the error and continue
        # closing the rest of the IO objects.
        paths_to_close = [path] if path else list(self._path_to_data.keys())
        success = True
        for _path in paths_to_close:
            try:
                path_data = self._path_to_data.pop(_path)
                path_data.queue.put(None)
                path_data.thread.join()
            except Exception:
                logger = logging.getLogger(__name__)
                logger.exception(f"`NonBlockingIO` thread for {_path} failed to join.")
                success = False
        return success

    def _close_thread_pool(self) -> bool:
        """Close the thread pool for this manager.

        Returns
        -------
        bool
            True on success

        """
        try:
            self._pool.shutdown()
        except Exception:
            logger = logging.getLogger(__name__)
            logger.exception("`NonBlockingIO` thread pool failed to close.")
            return False
        return True


# NOTE: We currently only support asynchronous writes (not reads).


class NonBlockingIO(io.IOBase):
    """Asynchronous write
    only IO wrapper.

    Notes
    -----
    Uses a queue to schedule writes in order.

    """

    def __init__(
        self,
        notify_manager: Callable[[Callable[[], None]], None],
        io_obj: IO[str] | IO[bytes],
        callback_after_file_close: Callable[[None], None] | None = None,
    ) -> None:
        """Returned to the user on an `opena` call. Uses a Queue to manage the
        IO jobs that need to be run to ensure order preservation and a
        polling Thread that checks the Queue. Implementation for these are
        lifted to `NonBlockingIOManager` since `NonBlockingIO` closes upon
        leaving the context block.

        NOTE: Writes to the same path are serialized so they are written in
        the same order as they were called but writes to distinct paths can
        happen concurrently.

        Args:
            notify_manager (Callable): a callback function passed in from the
                `NonBlockingIOManager` so that all IO jobs can be stored in
                the manager. It takes in a single argument, namely another
                callable function.
                Example usage:
                ```
                    notify_manager(lambda: file.write(data))
                    notify_manager(lambda: file.close())
                ```
                Here, we tell `NonBlockingIOManager` to add a write callable
                to the path's Queue, and then to add a close callable to the
                path's Queue. The path's polling Thread then executes the write
                callable, waits for it to finish, and then executes the close
                callable. Using `lambda` allows us to pass callables to the
                manager.
            io_obj (IO): a reference to the IO object returned by the
                `PathHandler._open` function.
            callback_after_file_close (Callable): An optional argument that can
                be passed to perform operations that depend on the asynchronous
                writes being completed. The file is first written to the local
                disk and then the callback is executed.

        """
        super().__init__()
        self._notify_manager = notify_manager
        self._io = io_obj
        self._callback_after_file_close = callback_after_file_close

        self._close_called = False

    def readable(self) -> bool:
        return False

    def writable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return True

    def write(self, b: bytes | bytearray) -> None:
        """Schedule a write operation.

        Parameters
        ----------
        b : bytes or bytearray
            Data to write

        """
        #  bytes]`.
        self._notify_manager(lambda: self._io.write(b))

    def seek(self, offset: int, whence: int = 0) -> int:
        """Called on `f.seek()`."""
        self._notify_manager(lambda: self._io.seek(offset, whence))

    def tell(self) -> int:
        """Called on `f.tell()`."""
        msg = "ioPath async writes does not support `tell` calls."
        raise ValueError(msg)

    def truncate(self, size: int | None = None) -> int:
        """Called on `f.truncate()`."""
        self._notify_manager(lambda: self._io.truncate(size))

    def close(self) -> None:
        """Called on `f.close()` or automatically by the context manager.
        We add the `close` call to the file's queue to make sure that
        the file is not closed before all of the write jobs are complete.
        """
        # `ThreadPool` first closes the file and then executes the callback.
        # We only execute the callback once even if there are multiple
        # `f.close` calls.
        self._notify_manager(lambda: self._io.close())
        if not self._close_called and self._callback_after_file_close:
            #  None`.
            self._notify_manager(self._callback_after_file_close)
        self._close_called = True


# NOTE: To use this class, use `buffered=True` in `NonBlockingIOManager`.
# NOTE: This class expects the IO mode to be buffered.


class NonBlockingBufferedIO(io.IOBase):
    """Buffered version of NonBlockingIO.

    Notes
    -----
    Writes are accumulated in a buffer before being queued.

    """

    MAX_BUFFER_BYTES = 10 * 1024 * 1024  # 10 MiB

    def __init__(
        self,
        notify_manager: Callable[[Callable[[], None]], None],
        io_obj: IO[str] | IO[bytes],
        callback_after_file_close: Callable[[None], None] | None = None,
        buffering: int = -1,
    ) -> None:
        """Buffered version of `NonBlockingIO`. All write data is stored in an
        IO buffer until the buffer is full, or `flush` or `close` is called.

        Args:
            Same as `NonBlockingIO` args.
            buffering (int): An optional argument to set the buffer size for
                buffered asynchronous writing.

        """
        super().__init__()
        self._notify_manager = notify_manager
        self._io = io_obj
        self._callback_after_file_close = callback_after_file_close

        self._buffers = [io.BytesIO()]

        self._buffer_size = buffering if buffering > 0 else self.MAX_BUFFER_BYTES
        self._close_called = False

    def readable(self) -> bool:
        return False

    def writable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return False

    def write(self, b: bytes | bytearray) -> None:
        """Called on `f.write()`. Gives the manager the write job to call."""
        buffer = self._buffers[-1]
        with memoryview(b) as view:
            buffer.write(view)
        if buffer.tell() < self._buffer_size:
            return
        self.flush()

    def close(self) -> None:
        """Called on `f.close()` or automatically by the context manager.
        We add the `close` call to the file's queue to make sure that
        the file is not closed before all of the write jobs are complete.
        """
        self.flush()
        # Close the last buffer created by `flush`.
        self._notify_manager(lambda: self._buffers[-1].close())
        # `ThreadPool` first closes the file and then executes the callback.
        self._notify_manager(lambda: self._io.close())
        if not self._close_called and self._callback_after_file_close:
            #  None`.
            self._notify_manager(self._callback_after_file_close)
        self._close_called = True

    def flush(self) -> None:
        """Called on `f.write()` if the buffer is filled (or overfilled). Can
        also be explicitly called by user.
        NOTE: Buffering is used in a strict manner. Any buffer that exceeds
        `self._buffer_size` will be broken into multiple write jobs where
        each has a write call with `self._buffer_size` size.
        """
        buffer = self._buffers[-1]
        if buffer.tell() == 0:
            return
        pos = 0
        total_size = buffer.seek(0, io.SEEK_END)
        view = buffer.getbuffer()
        # Chunk the buffer in case it is larger than the buffer size.
        while pos < total_size:
            item = view[pos : pos + self._buffer_size]
            # `item=item` is needed due to Python's late binding closures.

            #  = ...) -> int`.
            self._notify_manager(lambda item=item: self._io.write(item))
            pos += self._buffer_size
        # Close buffer immediately after being written to file and create
        # a new buffer.
        self._notify_manager(lambda: buffer.close())
        self._buffers.append(io.BytesIO())
