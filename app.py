import sys
import time
import VirtualSteering as vs
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout
)

class MyWindow(QWidget):
    steering_state = False
    def __init__(self):
        super().__init__()
        self.initUI()
        app.aboutToQuit.connect(self.cleanup)

    def initUI(self):
        self.setWindowTitle("Virtual Steering ")
        self.setFixedWidth(300)  # Width in pixels
        self.setFixedHeight(100)  # Height in pixels
        self.button = QPushButton("Start Steering!")
        self.button.clicked.connect(self.handle_button_click)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def handle_button_click(self):
        if self.steering_state == False:
            self.steering_state = True
            self.button.setText("Stop Steering!")
            pTime=0
            while self.steering_state == True:
                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                vs.steering(fps)
                if self.steering_state==False:
                    break
        else:
            self.steering_state = False
            self.button.setText("Start Steering!")

    def cleanup(self):
        vs.cleanup()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())