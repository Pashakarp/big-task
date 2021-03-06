import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]
delta = 15.005
longitude, lattitude = "133.165599", "-26.757718"


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.delta = 10
        self.getImage()
        self.initUI()

    def getImage(self):
        map_params = {
            "ll": ",".join([longitude, lattitude]),
            "spn": ",".join([str(self.delta), str(self.delta)]),
            "l": "map"
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, e):
        global delta
        if e.key() == Qt.Key_Escape:
            self.close()

        if e.key() == Qt.Key_PageDown:
            if self.delta <= 98:
                self.delta += 2
                self.getImage()
                self.update_map()

        if e.key() == Qt.Key_PageUp:
            if self.delta >= 2.005:
                self.delta -= 2
                self.getImage()
                self.update_map()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def update_map(self):
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
