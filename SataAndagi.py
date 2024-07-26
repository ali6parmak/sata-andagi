import sys
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QDesktopWidget
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QCursor
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QSoundEffect


class SataAndagi(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.pixmap = QPixmap('osaka250.png')

        self.setMask(self.pixmap.mask())

        self.resize(self.pixmap.size())
        self.position_window()

        self.sound = QSoundEffect()
        self.sound.setSource(QUrl.fromLocalFile('sata-andagi.wav'))

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('osaka250.ico'))

        tray_menu = QMenu()
        show_action = tray_menu.addAction("Show")
        hide_action = tray_menu.addAction("Hide")
        quit_action = tray_menu.addAction("Quit")

        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(QApplication.instance().quit)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.dragging = False
        self.drag_threshold = 5  # pixels
        self.click_pos = None

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.click_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if not self.dragging:
                if (event.pos() - self.click_pos).manhattanLength() > self.drag_threshold:
                    self.dragging = True
                    self.setCursor(QCursor(Qt.ClosedHandCursor))
            if self.dragging:
                self.move(self.mapToParent(event.pos() - self.click_pos))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.dragging:
                self.dragging = False
                self.setCursor(QCursor(Qt.ArrowCursor))
            else:
                self.play_sound()
            self.click_pos = None

    def position_window(self):
        screen = QDesktopWidget().screenNumber(QDesktopWidget().cursor().pos())
        screen_geometry = QDesktopWidget().screenGeometry(screen)
        taskbar_height = QDesktopWidget().availableGeometry().height() - screen_geometry.height()

        x = screen_geometry.width() - self.width()
        y = screen_geometry.height() - self.height() - taskbar_height

        self.move(x, y)

    def play_sound(self):
        self.sound.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    ex = SataAndagi()
    sys.exit(app.exec_())
