from contextlib import contextmanager
from types import TracebackType
from typing import Iterator, Optional, Type, overload

from rich.progress import Progress, SpinnerColumn, TextColumn

from src.logs.task_progress import TaskProgressManager


class ProgressManager:

    def __init__(self):
        self.spinner = SpinnerColumn(style="bold yellow")
        self.progress = Progress(
            self.spinner,
            TextColumn("{task.fields[status]} {task.description}"),
        )
        self.indent_level = 0

    def __enter__(self):
        self.progress.__enter__()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        self.progress.__exit__(exc_type, exc_val, exc_tb)

    @contextmanager
    def task(self, desc) -> Iterator[TaskProgressManager]:
        task_ctx = TaskProgressManager(
            progress=self.progress,
            desc=desc,
            indent_level=self.indent_level
        )

        self.indent_level += 1
        try:
            with task_ctx:
                yield task_ctx
        finally:
            self.indent_level -= 1
