from types import TracebackType
from typing import Optional, Type

from rich.progress import Progress, TaskID

from src.logs.log import LogManager, LOG_SYMBOLS


class TaskProgressManager(LogManager):

    def __init__(
        self,
        progress: Progress,
        desc: str,
        indent_level: int = 0,
    ):
        super().__init__()
        self.progress: Progress = progress
        self.desc = desc
        self.indent_level = indent_level
        self.task_id: TaskID = TaskID(0)
        self.task_completed = False

    def __enter__(self):
        desc = self._get_indented_desc()
        self.task_id = self.progress.add_task(desc, total=1, status=" ")

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        if not self.task_completed:
            self.complete_task()

    def complete_task(self, desc=None, status="succeed"):

        if desc is None:
            desc = self._get_indented_desc(is_active_task=False)

        if status == "succeed":
            self.task_succees(desc)
        elif status == "info":
            self.task_info(desc)
        elif status == "warning":
            self.task_warning(desc)
        elif status == "error":
            self.task_error(desc)

    def task_info(self, desc):
        self.info_log(desc)
        self.update_task(desc, LOG_SYMBOLS["info"])

    def task_succees(self, desc):
        self.info_log(desc)
        self.update_task(desc, LOG_SYMBOLS["success"])

    def task_warning(self, desc):
        self.warn_log(desc)
        self.update_task(desc, LOG_SYMBOLS["warning"])

    def task_error(self, desc):
        self.err_log(desc)
        self.update_task(desc, LOG_SYMBOLS["error"])

    def update_task(self, desc, symbol):
        self.task_completed = True
        self.progress.update(self.task_id, description=desc, completed=1, status=symbol)

    def _get_indented_desc(self, is_active_task=True):
        indent = "  " * self.indent_level

        if is_active_task:
            return f"[yellow]{indent}{self.desc}[/]"

        return f"{indent}{self.desc}"
