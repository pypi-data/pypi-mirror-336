import sys
from time import sleep

from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget, QMainWindow, QApplication
from PySide6.QtCore import QTimer, Slot

from phystool.qt.helper import QBusyDialog


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0
        layout = QVBoxLayout()
        b = QPushButton("DANGER!")
        b.pressed.connect(self.commit)
        self.l = QLabel("Start")
        layout.addWidget(self.l)
        layout.addWidget(b)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)
        self.show()

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def execute_this_fn(self):
        for n in range(0, 5):
            print(n)
            sleep(1)

        return "Done."

    @Slot()
    def commit(self):
        busy_dialog = QBusyDialog("coucou", self)
        busy_dialog.run(self.execute_this_fn)
        print("prou2")

    @Slot()
    def recurring_timer(self):
        self.counter += 1
        self.l.setText("Counter: %d" % self.counter)


def run_C() -> None:
    """
    coucou
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()


if __name__ == "__main__":
    run_C()
