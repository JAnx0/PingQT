import sys

from shlex import split
from subprocess import check_output

from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Log(object):
    def __init__(self, edit):
        self.out = sys.stdout
        self.textEdit = edit

    def write(self, message):
        self.out.write(message)
        self.textEdit.append(message)

    def flush(self):
        self.out.flush()


class CSlider(QSlider):
    def __init__(self, default, parent=None):
        super(CSlider, self).__init__(parent)
        self.setOrientation(Qt.Horizontal)
        self.setMinimum(0)
        self.default = default

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.setValue(self.default)


class Window(QWidget):
    # Constants
    DEBUG: bool = False
    DEFAULT_PACKET_COUNT: int = 10
    IS_WINDOWS_HOST: bool = False
    PACKET_COUNT: int = DEFAULT_PACKET_COUNT
    TARGET: str = u"google.com"
    WINDOW_HEIGHT: int = 520
    WINDOW_WIDTH: int = 580
    WINDOW_TITLE: str = u"Ping"

    # Formats
    INFO: str = u"[ i ]"
    ERROR: str = u"[ ! ]"
    STEP: str = u"[ * ]"

    # Constructor
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi()
        self.show()
        sys.stdout = Log(self.outputEdit)

    def setupUi(self):
        # Set up the UI
        applicationForm = self

        if not applicationForm.objectName():
            applicationForm.setObjectName(u"applicationForm")
        applicationForm.setEnabled(True)
        applicationForm.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(applicationForm.sizePolicy().hasHeightForWidth())
        applicationForm.setSizePolicy(sizePolicy)
        # if QT_CONFIG(tooltip)
        applicationForm.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)

        exitAction = QAction(applicationForm)
        exitAction.setStatusTip(u"Exit")
        exitAction.setText(u"Exit")
        exitAction.setIcon(QIcon("assets/img/exit-icon.png"))
        exitAction.triggered.connect(self.close)

        showInfoAction = QAction(applicationForm)
        showInfoAction.setStatusTip(u"Show Info")
        showInfoAction.setText(u"Info")
        showInfoAction.triggered.connect(self.showInfo)

        menubar = QMenuBar(applicationForm)
        fileMenu = menubar.addMenu(QCoreApplication.translate("applicationForm", u"&File", None))
        fileMenu.addAction(exitAction)
        infoMenu = menubar.addAction(showInfoAction)


        self.ipAddressEdit = QLineEdit(applicationForm)
        self.ipAddressEdit.setObjectName(u"ipAddressEdit")
        self.ipAddressEdit.setGeometry(QRect(180, 30, 221, 21))
        self.ipAddressEdit.setText(self.TARGET)
        self.ipDnsLabel = QLabel(applicationForm)
        self.ipDnsLabel.setObjectName(u"ipDnsLabel")
        self.ipDnsLabel.setGeometry(QRect(20, 30, 161, 21))
        self.isWindowsHostCheckbox = QCheckBox(applicationForm)
        self.isWindowsHostCheckbox.setObjectName(u"isWindowsHostCheckbox")
        self.isWindowsHostCheckbox.setGeometry(QRect(420, 30, 141, 21))
        self.line = QFrame(applicationForm)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(10, 70, 561, 20))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.packetCountLabel = QLabel(applicationForm)
        self.packetCountLabel.setObjectName(u"packetCountLabel")
        self.packetCountLabel.setGeometry(QRect(20, 90, 131, 31))
        font = QFont()
        font.setPointSize(14)
        self.packetCountLabel.setFont(font)
        self.packetCountSlider = CSlider(default=self.DEFAULT_PACKET_COUNT, parent=applicationForm)
        self.packetCountSlider.setObjectName(u"packetCountSlider")
        self.packetCountSlider.setGeometry(QRect(20, 130, 251, 31))
        self.packetCountSlider.setCursor(QCursor(Qt.OpenHandCursor))
        self.packetCountSlider.setMaximum(100)
        self.packetCountSlider.setValue(10)
        self.packetCountSlider.setOrientation(Qt.Horizontal)
        self.packetCountDisplayLabel = QLabel(applicationForm)
        self.packetCountDisplayLabel.setObjectName(u"packetCountDisplayLabel")
        self.packetCountDisplayLabel.setGeometry(QRect(160, 90, 111, 31))
        self.packetCountDisplayLabel.setFont(font)
        self.packetCountDisplayLabel.setText(u"0")
        self.outputEdit = QTextEdit(applicationForm)
        self.outputEdit.setObjectName(u"outputEdit")
        self.outputEdit.setGeometry(QRect(20, 220, 541, 261))
        self.outputEdit.viewport().setProperty("cursor", QCursor(Qt.ForbiddenCursor))
        self.outputEdit.setReadOnly(True)
        self.outputLabel = QLabel(applicationForm)
        self.outputLabel.setObjectName(u"outputLabel")
        self.outputLabel.setGeometry(QRect(20, 185, 81, 21))
        self.outputLabel.setFont(font)
        self.startPingButton = QPushButton(applicationForm)
        self.startPingButton.setObjectName(u"startPingButton")
        self.startPingButton.setGeometry(QRect(290, 90, 271, 71))
        font1 = QFont()
        font1.setPointSize(25)
        self.startPingButton.setFont(font1)
        self.startPingButton.setCursor(QCursor(Qt.PointingHandCursor))

        # Signals
        self.packetCountDisplayLabel.setText(str(self.DEFAULT_PACKET_COUNT))

        self.packetCountSlider.sliderPressed.connect(self.sliderPressed)
        self.packetCountSlider.sliderReleased.connect(self.sliderReleased)
        self.packetCountSlider.valueChanged[int].connect(self.adjustPacketCountLabel)

        self.isWindowsHostCheckbox.toggled.connect(self.setWindowsHostStatus)

        self.ipAddressEdit.textChanged[str].connect(self.adjustPingTarget)

        self.startPingButton.clicked.connect(self.startPing)

        self.retranslateUi(applicationForm)

        QMetaObject.connectSlotsByName(applicationForm)

    def retranslateUi(self, applicationForm):
        applicationForm.setWindowTitle(QCoreApplication.translate("applicationForm", self.WINDOW_TITLE, None))
        # if QT_CONFIG(tooltip)
        self.ipAddressEdit.setToolTip(QCoreApplication.translate("applicationForm", u"Specify ping target.", None))
        # endif // QT_CONFIG(tooltip)
        self.ipDnsLabel.setText(QCoreApplication.translate("applicationForm", u"IP Address / DNS Name:", None))
        # if QT_CONFIG(tooltip)
        self.isWindowsHostCheckbox.setToolTip(
            QCoreApplication.translate("applicationForm", u"If you know,  that the target runs Windows, check.", None))
        # endif // QT_CONFIG(tooltip)
        self.isWindowsHostCheckbox.setText(QCoreApplication.translate("applicationForm", u"Windows Host", None))
        self.packetCountLabel.setText(QCoreApplication.translate("applicationForm", u"Packet Count:", None))
        # if QT_CONFIG(tooltip)
        self.packetCountSlider.setToolTip(
            QCoreApplication.translate("applicationForm", u"Specify number of ICMP Packets being sent.", None))
        # endif // QT_CONFIG(tooltip)
        self.outputLabel.setText(QCoreApplication.translate("applicationForm", u"Output:", None))
        # if QT_CONFIG(tooltip)
        self.startPingButton.setToolTip(
            QCoreApplication.translate("applicationForm", u"Start pinging the target.", None))
        # endif // QT_CONFIG(tooltip)
        self.startPingButton.setText(QCoreApplication.translate("applicationForm", u"PING!", None))

    # Slot Functions
    def showInfo(self):
        QMessageBox.information(self, self.WINDOW_TITLE, "Ping GUI\n(c) by JAnx0, 2021")

    def setDefaultPacketCount(self):
        self.packetCountSlider.setValue(self.DEFAULT_PACKET_COUNT)

    def sliderPressed(self):
        self.packetCountSlider.setCursor(QCursor(Qt.ClosedHandCursor))

    def sliderReleased(self):
        self.packetCountSlider.setCursor(QCursor(Qt.OpenHandCursor))

    def adjustPacketCountLabel(self, value):
        self.packetCountDisplayLabel.setText(str(value))
        self.PACKET_COUNT = value
        if self.DEBUG:
            print(f"{self.INFO} Packet count changed. New count: {value}")

    def setWindowsHostStatus(self):
        self.IS_WINDOWS_HOST = not self.IS_WINDOWS_HOST
        if self.IS_WINDOWS_HOST:
            print(f"{self.ERROR} Windows has ICMP disabled by default. Ping may not work.")
        if self.DEBUG:
            print(f"{self.INFO} Windows host: {self.IS_WINDOWS_HOST}")

    def adjustPingTarget(self, value):
        self.TARGET = value
        if self.DEBUG:
            print(f"{self.INFO} Target changed. New target: {value}")

    def startPing(self):
        self.outputEdit.clear()

        ping_command = f"ping -c {self.PACKET_COUNT} {self.TARGET}"

        print(f"{self.STEP} Starting. Sending {self.PACKET_COUNT} ICMP Packets to Target ({self.TARGET})")

        try:
            print(check_output(split(ping_command)).decode())

        except Exception as e:
            if self.DEBUG:
                print(f"{self.ERROR} Error: {e}")
