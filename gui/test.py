from PyQt5.QtWidgets import QApplication, QLabel

class main_window(object):
    def __init__(self):
        self.label = QLabel('Hello World!')
        self.label.show()
        input()

if __name__ == "__main__":
    program = QApplication([])
    window = main_window()
