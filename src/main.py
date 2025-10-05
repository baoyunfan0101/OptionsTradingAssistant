# 定义主窗口
import os
import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
import qdarkstyle

import widget


class main_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('期权交易助手')
        self.setWindowIcon(QIcon('logo.ico'))
        self.resize(1600, 900)
        self.setMinimumSize(1600, 900)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())  # 应用QDarkStyleSheet样式表
        self.ui = widget.Ui_Form()  # 主窗口ui
        self.ui.setupUi(self)

        # 槽: ui.tableWidget_1 -> tableWidget_1_menu
        self.ui.tableWidget_1.customContextMenuRequested.connect(self.tableWidget_1_menu)
        # 槽: ui.tableWidget_2 -> tableWidget_2_menu
        self.ui.tableWidget_2.customContextMenuRequested.connect(self.tableWidget_2_menu)
        # 槽: ui.tableWidget_3 -> tableWidget_3_menu
        self.ui.tableWidget_3.customContextMenuRequested.connect(self.tableWidget_3_menu)
        # 槽: ui.tableWidget_rank -> tableWidget_rank_menu
        self.ui.tableWidget_rank.customContextMenuRequested.connect(self.tableWidget_rank_menu)

    # 调整窗口大小, 重新定义resizeEvent事件
    def resizeEvent(self, QResizeEvent):
        self.ui.resize(self.width(), self.height())

    # tableWidget_1右键弹出菜单
    def tableWidget_1_menu(self, pos):
        self.ui.show_tableWidget_1_menu(pos)

    # tableWidget_2右键弹出菜单
    def tableWidget_2_menu(self, pos):
        self.ui.show_tableWidget_2_menu(pos)

    # tableWidget_3右键弹出菜单
    def tableWidget_3_menu(self, pos):
        self.ui.show_tableWidget_3_menu(pos)

    # tableWidget_rank右键弹出菜单
    def tableWidget_rank_menu(self, pos):
        self.ui.show_tableWidget_rank_menu(pos)


if __name__ == '__main__':
    # 补充应用程序运行缺少的依赖
    # os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')

    app = QApplication(sys.argv)

    w = main_window()
    w.show()

    sys.exit(app.exec_())
