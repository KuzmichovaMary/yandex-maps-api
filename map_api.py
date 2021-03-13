# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'map_api.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import sys
from io import BytesIO

import requests
from PIL import Image, ImageQt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow, QButtonGroup
from search_by_address import search
from PyQt5.QtCore import Qt
from samples.geocoder import geocode, get_ll_span
from samples.distance import lonlat_distance
from map_api_dialog import Dialog


def search_organizations(curr_lonlat, spn, results=1):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    for i in ["магазин", "столовая", "кафе", "ресторан", "библиотека", "школа",
              "институт", "больница", "аптека", "церковь", "страховое агенство", "супермаркет"]:
        search_params = {
            "apikey": api_key,
            "text": i,
            "ll": ",".join(map(str, curr_lonlat)),
            "spn": "0.00035,0.00035",
            "lang": "ru_RU",
            # "results": results,
            "type": "biz"
        }

        response = requests.get(search_api_server, params=search_params)
        json_response = response.json()
        print(json_response)

        if json_response["features"]:
            # Получаем первую найденную организацию.
            organization = json_response["features"][0]
            # Название организации.
            bbox = json_response["properties"]["ResponseMetaData"]["SearchRequest"]["boundedBy"]
            org_name = organization["properties"]["CompanyMetaData"]["name"]
            # Адрес организации.
            org_address = organization["properties"]["CompanyMetaData"]["address"]

            # Получаем координаты ответа.
            point = organization["geometry"]["coordinates"]
            ll = tuple(map(float, point))

            # левая, нижняя, правая и верхняя границы из координат углов:
            l, b = bbox[0]
            r, t = bbox[1]

            # Вычисляем полуразмеры по вертикали и горизонтали
            dx = abs(float(l) - float(r)) / 2.0
            dy = abs(float(t) - float(b)) / 2.0

            # Собираем размеры в параметр span
            spn = f"{dx},{dy}"
            return ",".join(map(str, ll)), spn, org_name, org_address
    return None, None, None, None


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(818, 586)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.map_label = QtWidgets.QLabel(self.centralwidget)
        self.map_label.setGeometry(QtCore.QRect(60, 60, 450, 450))
        self.map_label.setText("")
        self.map_label.setObjectName("map_label")
        self.address_to_search = QtWidgets.QLineEdit(self.centralwidget)
        self.address_to_search.setGeometry(QtCore.QRect(570, 100, 201, 31))
        self.address_to_search.setObjectName("address_to_search")
        self.search = QtWidgets.QPushButton(self.centralwidget)
        self.search.setGeometry(QtCore.QRect(780, 100, 31, 31))
        self.search.setStyleSheet("height: 30px;\n"
"width: 30px;\n"
"border-radius: 15px;\n"
"background-color: rgb(194, 255, 82);")
        self.search.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/Mary/Downloads/search.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search.setIcon(icon)
        self.search.setObjectName("search")
        self.bin = QtWidgets.QPushButton(self.centralwidget)
        self.bin.setGeometry(QtCore.QRect(780, 140, 31, 31))
        self.bin.setStyleSheet("height: 30px;\n"
"width: 30px;\n"
"border-radius: 15px;\n"
"background-color: rgb(194, 255, 82);")
        self.bin.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("C:/Users/Mary/Downloads/trash-2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bin.setIcon(icon1)
        self.bin.setObjectName("bin")
        self.info = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.info.setGeometry(QtCore.QRect(570, 250, 231, 271))
        self.info.setObjectName("info")
        self.show_index = QtWidgets.QCheckBox(self.centralwidget)
        self.show_index.setGeometry(QtCore.QRect(569, 139, 201, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.show_index.setFont(font)
        self.show_index.setObjectName("show_index")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(570, 190, 231, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.showmap = QtWidgets.QRadioButton(self.centralwidget)
        self.showmap.setGeometry(QtCore.QRect(570, 0, 200, 20))
        self.showmap.setChecked(True)
        self.showmap.setObjectName("showmap")
        self.show_sat = QtWidgets.QRadioButton(self.centralwidget)
        self.show_sat.setGeometry(QtCore.QRect(570, 30, 200, 20))
        self.show_sat.setObjectName("show_sat")
        self.show_map_sat = QtWidgets.QRadioButton(self.centralwidget)
        self.show_map_sat.setGeometry(QtCore.QRect(570, 60, 200, 20))
        self.show_map_sat.setObjectName("show_map_sat")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 818, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Maps Api"))
        self.show_index.setText(_translate("MainWindow", "Показывать почтовый индекс"))
        self.label_2.setText(_translate("MainWindow", "Информация об объекте"))
        self.showmap.setText(_translate("MainWindow", "Схема"))
        self.show_sat.setText(_translate("MainWindow", "Спутник"))
        self.show_map_sat.setText(_translate("MainWindow", "Гибрид"))


class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.d = 0
        self.map_label.setFocusPolicy(Qt.StrongFocus)
        self.map_label.setFocus()

        ll, spn = self.search_toponym("ул.Фотиевой, 18")
        self.map_params = {
            "ll": ll,
            "spn": spn,
            "l": "map",
            "pt": "",
            "rspn": 0,
            "size": "450,450"
        }
        self.pt = []
        self.get_image()

        self.group = QButtonGroup(self)
        self.group.addButton(self.showmap)
        self.group.addButton(self.show_map_sat)
        self.group.addButton(self.show_sat)
        self.group.buttonClicked.connect(self.btn_clicked)
        self.search.clicked.connect(self.search_)
        self.bin.clicked.connect(self.delete)
        self.show_index.stateChanged.connect(self.show_postal_code)
        self.toponym_postal_code = ""
        self.toponym_address = ""

    def show_postal_code(self):
        self.info.setPlainText(self.toponym_address)
        if self.show_index.isChecked():
            self.info.appendPlainText(self.toponym_postal_code)

    def delete(self):
        self.pt = []
        self.map_params["pt"] = ""
        self.get_image()
        self.info.setPlainText("")

    def search_(self):
        address = self.address_to_search.text()
        self.search_address(address)

    def search_address(self, address, ll=None, spn=None, rspn=0):
        toponym = geocode(address, ll, spn, rspn)
        if not toponym:
            print("Nothing found")
            return
        if toponym["metaDataProperty"]["GeocoderMetaData"]["kind"] == "house":
            if "postal_code" in toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]:
                self.toponym_postal_code = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
            else:
                self.toponym_postal_code = "No postal code"
            self.toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            ll, spn = get_ll_span(toponym)
            self.pt.append(f"{ll},comma")
            self.map_params["pt"] = "~".join(self.pt)
            if not rspn:
                self.map_params["ll"] = ll
                self.map_params["spn"] = spn
            self.get_image()
            to_show = self.toponym_address
            if self.show_index.isChecked():
                to_show += self.toponym_postal_code
            self.info.setPlainText(to_show)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            p = event.pos()
            # print(p.x() - 60, p.y() - 60)
            spn_1, spn_2 = map(float, self.map_params["spn"].split(","))
            lon, lat = map(float, self.map_params["ll"].split(","))
            left, top = lon - spn_1, lat + spn_2
            cur_ll = (left + spn_1 * ((p.x() - 60) / 225), top - spn_2 * ((p.y() - 60) / 225))
            self.delete()
            self.search_address(f"{cur_ll[0]},{cur_ll[1]}", rspn=1)
        if event.button() == Qt.RightButton:
            self.delete()
            p = event.pos()
            # print(p.x() - 60, p.y() - 60)
            spn_1, spn_2 = map(float, self.map_params["spn"].split(","))
            lon, lat = map(float, self.map_params["ll"].split(","))
            left, top = lon - spn_1, lat + spn_2
            cur_ll = (left + spn_1 * ((p.x() - 60) / 225), top - spn_2 * ((p.y() - 60) / 225))
            self.pt = [f"{cur_ll[0]},{cur_ll[1]},pm2rdl"]  # , f"{lon},{lat},pm2wtl"]
            self.map_params["pt"] = "~".join(self.pt)
            self.get_image()
            ll, spn, org_name, org_address = search_organizations(cur_ll, self.map_params["spn"])
            if ll:
                self.pt = [f"{ll},comma", f"{cur_ll[0]},{cur_ll[1]},pm2rdl"] #, f"{lon},{lat},pm2wtl"]
                self.map_params["pt"] = "~".join(self.pt)
                self.get_image()
                self.info.appendHtml(f"<h1>{org_name}</h1>\n{org_address}")

    def btn_clicked(self, btn):
        txt = btn.text()
        if txt == "Спутник":
            l = "sat"
        elif txt == "Схема":
            l = "map"
        else:
            l = "skl"
        self.map_params["l"] = l
        self.get_image()

    def search_toponym(self, toponym_to_find):
        toponym = geocode(toponym_to_find)
        ll, spn = get_ll_span(toponym)
        return ll, spn

    def to_static_maps(self):
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=self.map_params)

        return response.content

    def get_image(self):
        self.img = self.to_static_maps()
        pm = QPixmap(450, 450)
        pm.loadFromData(self.img)
        self.map_label.setPixmap(pm)

    def keyPressEvent(self, event):
        spn = tuple(map(lambda x: float(x), self.map_params["spn"].split(",")))
        lon, lat = map(float, self.map_params["ll"].split(","))
        if event.key() == Qt.Key_PageUp:
            self.map_params["spn"] = f"{spn[0] / 1.5},{spn[1] / 1.5}"
            self.get_image()
        if event.key() == Qt.Key_PageDown:
            self.map_params["spn"] = f"{spn[0] * 1.5},{spn[1] * 1.5}"
            self.get_image()
        if event.key() == Qt.Key_Up:
            self.map_params["ll"] = f"{lon},{lat + spn[1] / 2}"
            self.get_image()
        if event.key() == Qt.Key_Down:
            self.map_params["ll"] = f"{lon},{lat - spn[1] / 2}"
            self.get_image()
        if event.key() == Qt.Key_Right:
            self.map_params["ll"] = f"{lon + spn[0] / 2},{lat}"
            self.get_image()
        if event.key() == Qt.Key_Left:
            self.map_params["ll"] = f"{lon - spn[0] / 2},{lat}"
            self.get_image()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
