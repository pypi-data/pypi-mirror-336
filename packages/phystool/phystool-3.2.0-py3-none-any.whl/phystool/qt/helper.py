from collections.abc import Callable

from PySide6.QtCore import (
    Signal,
    Slot,
    QObject,
    Qt,
    QRunnable,
    QThreadPool,
)
from PySide6.QtWidgets import QProgressDialog


class WorkerSignals(QObject):
    finished = Signal(str)


class Worker(QRunnable):
    # https://www.pythonguis.com/tutorials/multithreading-pyside6-applications-qthreadpool/  # noqa

    def __init__(self, fn: Callable[[None], str]) -> None:
        super().__init__()
        self.fn = fn
        self.signals = WorkerSignals()

    def run(self):
        try:
            msg = self.fn()
        except Exception as e:
            msg = str(e)
        self.signals.finished.emit(msg)


class QBusyDialog(QProgressDialog):
    def __init__(self, label: str, parent: QObject):
        super().__init__(label, None, 0, 0, parent)
        self.setWindowModality(Qt.WindowModality.WindowModal)

    @Slot(str)
    def _finished(self, msg: str) -> None:
        self.setCancelButtonText("Ok")
        self.setLabelText(msg)

    def run(self, task) -> None:
        self.show()
        worker = Worker(task)
        worker.signals.finished.connect(self._finished)
        QThreadPool.globalInstance().start(worker)
