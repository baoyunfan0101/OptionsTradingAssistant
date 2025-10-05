# 主窗口ui
from PyQt5 import QtCore, QtGui, QtWidgets

import k_line
import solution


class Ui_Form(object):
    def __init__(self):
        self.open_flag = True  # 默认为True, 第一次load_tableWidget_1后改为False
        self.list1 = None  # 当前显示的股票期权(T型报价)代码列表
        self.list2 = None  # 当前显示的商品期权(T型报价)代码列表
        self.code = None  # 当前显示的合约分析代码

    def setupUi(self, Form):
        Form.setObjectName('Form')

        # tabWidget_1: 股票期权 / 商品期权 / 合约分析 / 价值潜力榜
        self.tabWidget_1 = QtWidgets.QTabWidget(Form)
        self.tabWidget_1.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget_1.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget_1.setObjectName('tabWidget_1')

        self.setup_tab_1()
        self.setup_tab_2()
        self.setup_tab_3()
        self.setup_tab_4()
        # /tabWidget_1

        self.tabWidget_1.setCurrentIndex(0)  # 默认选中: 股票期权
        self.tabWidget_2.setCurrentIndex(1)  # 默认选中: 股票期权 -> T型报价
        self.tabWidget_4.setCurrentIndex(0)  # 默认选中: 合约分析 -> 合约详情
        QtCore.QMetaObject.connectSlotsByName(Form)

    # tabWidget_1 -> tab_1: 股票期权
    def setup_tab_1(self):
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName('tab_1')

        # tabWidget_2: 分类报价 / T型报价
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tab_1)
        self.tabWidget_2.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget_2.setObjectName('tabWidget_2')

        # tabWidget_2 -> tab_11: 分类报价
        self.tab_11 = QtWidgets.QWidget()
        self.tab_11.setObjectName('tab_11')

        # 交易所
        self.label_ex11 = QtWidgets.QLabel(self.tab_11)
        self.label_ex11.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_ex11.setObjectName('label_ex11')
        self.label_ex11.setGeometry(QtCore.QRect(20, 20, 120, 30))
        self.label_ex11.setText('交易所：')

        self.comboBox_ex11 = QtWidgets.QComboBox(self.tab_11)
        self.comboBox_ex11.setObjectName('comboBox_ex11')
        self.comboBox_ex11.setGeometry(QtCore.QRect(140, 20, 120, 30))
        self.comboBox_ex11.addItems(['上交所', '深交所'])

        # tableWidget_1: 分类报价表格
        self.tableWidget_1 = QtWidgets.QTableWidget(self.tab_11)
        self.tableWidget_1.setObjectName('tableWidget_1')
        self.tableWidget_1.setShowGrid(True)  # 显示网格
        self.tableWidget_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  # 不显示水平滚动条
        self.tableWidget_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget_1.setColumnCount(17)  # 17列
        self.tableWidget_1.setRowCount(0)
        self.tableWidget_1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 禁止修改
        self.tableWidget_1.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # 选择行

        self.tableWidget_1.setHorizontalHeaderLabels(['合约代码', '合约简称', '涨幅', '最新价', '买价', '卖价', '买量', '卖量',
                                                      '持仓量', '成交量', '成交额', '振幅', 'Delta', 'Gamma', 'Theta', 'Vega',
                                                      '隐含波动率'])
        self.tableWidget_1.verticalHeader().setVisible(False)  # 不显示垂直表头

        self.tableWidget_1.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # 允许弹出菜单

        # 槽: tabWidget_2 -> tableWidget_1(当选中'分类报价'标签时再加载数据)
        self.tabWidget_2.currentChanged.connect(lambda: self.load_tableWidget_1())
        # 槽: comboBox_ex11 -> tableWidget_1
        self.comboBox_ex11.currentIndexChanged.connect(lambda: self.update_tableWidget_1())

        self.tabWidget_2.addTab(self.tab_11, '\t分类报价\t')
        # /tabWidget_2 -> tab_11

        # tabWidget_2 -> tab_12: T型报价
        self.tab_12 = QtWidgets.QWidget()
        self.tab_12.setObjectName('tab_12')

        self.label_c1 = QtWidgets.QLabel(self.tab_12)
        self.label_c1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_c1.setObjectName('label_c1')
        self.label_c1.setText('看涨合约')
        self.label_c1.setStyleSheet('color: #FF0000;')

        self.label_p1 = QtWidgets.QLabel(self.tab_12)
        self.label_p1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_p1.setObjectName('label_p1')
        self.label_p1.setText('看跌合约')
        self.label_p1.setStyleSheet('color: #00FF00;')

        # 交易所
        self.label_ex12 = QtWidgets.QLabel(self.tab_12)
        self.label_ex12.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_ex12.setObjectName('label_ex12')
        self.label_ex12.setGeometry(QtCore.QRect(20, 20, 120, 30))
        self.label_ex12.setText('交易所：')

        self.comboBox_ex12 = QtWidgets.QComboBox(self.tab_12)
        self.comboBox_ex12.setObjectName('comboBox_ex12')
        self.comboBox_ex12.setGeometry(QtCore.QRect(140, 20, 120, 30))
        # get_comboBox_ex12 from solution
        self.comboBox_ex12.addItems(solution.get_comboBox_ex12())

        # 期权品种
        self.label_pz12 = QtWidgets.QLabel(self.tab_12)
        self.label_pz12.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_pz12.setObjectName('label_pz12')
        self.label_pz12.setGeometry(QtCore.QRect(260, 20, 120, 30))
        self.label_pz12.setText('期权品种：')

        self.comboBox_pz12 = QtWidgets.QComboBox(self.tab_12)
        self.comboBox_pz12.setObjectName('comboBox_pz12')
        self.comboBox_pz12.setGeometry(QtCore.QRect(380, 20, 180, 30))
        # 槽: comboBox_ex12 -> comboBox_pz12
        self.comboBox_ex12.currentIndexChanged.connect(lambda: self.update_comboBox_pz12())
        self.update_comboBox_pz12()

        # 合约月份
        self.label_ym12 = QtWidgets.QLabel(self.tab_12)
        self.label_ym12.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_ym12.setObjectName('label_ym12')
        self.label_ym12.setGeometry(QtCore.QRect(560, 20, 120, 30))
        self.label_ym12.setText('合约月份：')

        self.comboBox_ym12 = QtWidgets.QComboBox(self.tab_12)
        self.comboBox_ym12.setObjectName('comboBox_ym12')
        self.comboBox_ym12.setGeometry(680, 20, 180, 30)
        # 槽: comboBox_ex12 -> comboBox_ym12
        self.comboBox_ex12.currentIndexChanged.connect(lambda: self.update_comboBox_ym12())
        self.update_comboBox_ym12()

        # 到期日
        self.label_da12 = QtWidgets.QLabel(self.tab_12)
        self.label_da12.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_da12.setObjectName('label_da12')
        self.label_da12.setGeometry(860, 20, 120, 30)
        self.label_da12.setText('到期日：')

        self.label_da12_text = QtWidgets.QLabel(self.tab_12)
        self.label_da12_text.setObjectName('label_da12_text')
        self.label_da12_text.setGeometry(980, 20, 180, 30)
        # 槽: comboBox_ym12 -> label_da12_text
        self.comboBox_ym12.currentIndexChanged.connect(lambda: self.update_label_da12_text())
        self.update_label_da12_text()

        # 标的资产
        self.label_ta12 = QtWidgets.QLabel(self.tab_12)
        self.label_ta12.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_ta12.setObjectName('label_ta12')
        self.label_ta12.setGeometry(1160, 20, 120, 30)
        self.label_ta12.setText('标的资产：')

        self.label_ta12_text = QtWidgets.QLabel(self.tab_12)
        self.label_ta12_text.setObjectName('label_ta12_text')
        self.label_ta12_text.setGeometry(1280, 20, 250, 30)
        # 槽: comboBox_pz12 -> label_ta12_text
        self.comboBox_pz12.currentIndexChanged.connect(lambda: self.update_label_ta12_text())
        self.update_label_ta12_text()

        # tableWidget_2: T型报价表格
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_12)
        self.tableWidget_2.setObjectName('tableWidget_2')
        self.tableWidget_2.setShowGrid(True)  # 显示网格
        self.tableWidget_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  # 不显示水平滚动条
        self.tableWidget_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget_2.setColumnCount(17)  # 17列
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 禁止修改
        self.tableWidget_2.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # 选择行

        self.tableWidget_2.setHorizontalHeaderLabels(['持仓量', '成交量', '卖量', '卖价', '买量', '买价', '涨幅', '最新价',
                                                      '行权价', '最新价', '涨幅', '买价', '买量', '卖价', '卖量', '成交量', '持仓量'])
        self.tableWidget_2.verticalHeader().setVisible(False)  # 不显示垂直表头

        self.tableWidget_2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # 允许弹出菜单

        # 槽: comboBox_pz12, comboBox_ym12 -> tableWidget_2
        self.comboBox_pz12.currentIndexChanged.connect(lambda: self.update_tableWidget_2())
        self.comboBox_ym12.currentIndexChanged.connect(lambda: self.update_tableWidget_2())
        self.update_tableWidget_2()

        self.tabWidget_2.addTab(self.tab_12, '\tT型报价\t')
        # /tabWidget_2 -> tab_12
        # /tabWidget_2

        self.tabWidget_1.addTab(self.tab_1, '\t股票期权\t')
        # /tabWidget_1 -> tab_1

    # tabWidget_1 -> tab_2: 商品期权
    def setup_tab_2(self):
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName('tab_2')

        # tabWidget_3: T型报价
        self.tabWidget_3 = QtWidgets.QTabWidget(self.tab_2)
        self.tabWidget_3.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget_3.setObjectName('tabWidget_3')

        # tabWidget_2 -> tab_21: T型报价
        self.tab_21 = QtWidgets.QWidget()
        self.tab_21.setObjectName('tab_21')

        self.label_c2 = QtWidgets.QLabel(self.tab_21)
        self.label_c2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_c2.setObjectName('label_c2')
        self.label_c2.setText('看涨合约')
        self.label_c2.setStyleSheet('color: #FF0000;')

        self.label_p2 = QtWidgets.QLabel(self.tab_21)
        self.label_p2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_p2.setObjectName('label_p2')
        self.label_p2.setText('看跌合约')
        self.label_p2.setStyleSheet('color: #00FF00;')

        # 期权品种
        self.label_pz21 = QtWidgets.QLabel(self.tab_21)
        self.label_pz21.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_pz21.setObjectName('label_pz21')
        self.label_pz21.setGeometry(QtCore.QRect(20, 20, 120, 30))
        self.label_pz21.setText('期权品种：')

        self.comboBox_pz21 = QtWidgets.QComboBox(self.tab_21)
        self.comboBox_pz21.setObjectName('comboBox_pz21')
        self.comboBox_pz21.setGeometry(QtCore.QRect(140, 20, 220, 30))
        # get_comboBox_pz21 from solution
        self.comboBox_pz21.addItems(solution.get_comboBox_pz21())

        # 到期月份
        self.label_ym21 = QtWidgets.QLabel(self.tab_21)
        self.label_ym21.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_ym21.setObjectName('label_ym21')
        self.label_ym21.setGeometry(QtCore.QRect(360, 20, 120, 30))
        self.label_ym21.setText('到期月份：')

        self.comboBox_ym21 = QtWidgets.QComboBox(self.tab_21)
        self.comboBox_ym21.setObjectName('comboBox_ym21')
        self.comboBox_ym21.setGeometry(QtCore.QRect(480, 20, 120, 30))
        # 槽: comboBox_pz21 -> comboBox_ym21
        self.comboBox_pz21.currentIndexChanged.connect(lambda: self.update_comboBox_ym21())
        self.update_comboBox_ym21()

        # 交易所
        self.label_ex21 = QtWidgets.QLabel(self.tab_21)
        self.label_ex21.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_ex21.setObjectName('label_ex21')
        self.label_ex21.setGeometry(QtCore.QRect(600, 20, 120, 30))
        self.label_ex21.setText('交易所：')

        self.label_ex21_text = QtWidgets.QLabel(self.tab_21)
        self.label_ex21_text.setObjectName('label_ex21_text')
        self.label_ex21_text.setGeometry(720, 20, 120, 30)
        # 槽: comboBox_pz21 -> label_ex21_text
        self.comboBox_pz21.currentIndexChanged.connect(lambda: self.update_label_ex21_text())
        self.update_label_ex21_text()

        # tableWidget_3: T型报价表格
        self.tableWidget_3 = QtWidgets.QTableWidget(self.tab_21)
        self.tableWidget_3.setObjectName('tableWidget_3')
        self.tableWidget_3.setShowGrid(True)  # 显示网格
        self.tableWidget_3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  # 不显示水平滚动条
        self.tableWidget_3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget_3.setColumnCount(15)  # 15列
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 禁止修改
        self.tableWidget_3.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # 选择行

        self.tableWidget_3.setHorizontalHeaderLabels(['持仓量', '卖量', '卖价', '买量', '买价', '涨幅', '最新价',
                                                      '行权价', '最新价', '涨幅', '买价', '买量', '卖价', '卖量', '持仓量'])
        self.tableWidget_3.verticalHeader().setVisible(False)  # 不显示垂直表头

        self.tableWidget_3.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # 允许弹出菜单

        # 槽: tabWidget_1 -> tableWidget_3(当选中'商品期权'标签时再加载数据)
        self.tabWidget_1.currentChanged.connect(lambda: self.load_tableWidget_3())
        # 槽: comboBox_ym21 -> tableWidget_3
        self.comboBox_ym21.currentIndexChanged.connect(lambda: self.update_tableWidget_3())

        self.tabWidget_3.addTab(self.tab_21, '\tT型报价\t')
        # /tabWidget_3 -> tab_21
        # /tabWidget_3

        self.tabWidget_1.addTab(self.tab_2, '\t商品期权\t')
        # /tabWidget_1 -> tab_2

    # tabWidget_1 -> tab_3: 合约分析
    def setup_tab_3(self):
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName('tab_3')

        # 合约代码
        self.label_code = QtWidgets.QLabel(self.tab_3)
        self.label_code.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_code.setGeometry(QtCore.QRect(20, 20, 120, 30))
        self.label_code.setObjectName('label_code')
        self.label_code.setText('合约代码：')

        self.lineEdit_code = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_code.setGeometry(QtCore.QRect(140, 20, 180, 30))
        self.lineEdit_code.setObjectName('lineEdit_code')

        self.pushButton_code = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_code.setGeometry(QtCore.QRect(350, 20, 80, 30))
        self.pushButton_code.setObjectName('pushButton_code')
        self.pushButton_code.setText('查询')

        self.label_err = QtWidgets.QLabel(self.tab_3)
        self.label_err.setGeometry(QtCore.QRect(480, 20, 500, 30))
        self.label_err.setObjectName('label_err')
        self.label_err.setStyleSheet('color: #FF0000;')

        # tabWidget_4: 合约详情 / K线数据
        self.tabWidget_4 = QtWidgets.QTabWidget(self.tab_3)
        self.tabWidget_4.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget_4.setObjectName('tabWidget_4')

        # tabWidget_4 -> tab_31: 合约详情
        self.tab_31 = QtWidgets.QWidget()
        self.tab_31.setObjectName('tab_31')

        # 基础信息
        self.label_d1 = QtWidgets.QLabel(self.tab_31)
        self.label_d1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_d1.setObjectName('label_d1')
        self.label_d1.setText('基础信息')

        self.textBrowser_1 = QtWidgets.QTextBrowser(self.tab_31)
        self.textBrowser_1.setObjectName('textBrowser_1')

        # 价值分析
        self.label_d2 = QtWidgets.QLabel(self.tab_31)
        self.label_d2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_d2.setObjectName('label_d2')
        self.label_d2.setText('价值分析')

        self.textBrowser_2 = QtWidgets.QTextBrowser(self.tab_31)
        self.textBrowser_2.setObjectName('textBrowser_2')

        # 风险分析
        self.label_d3 = QtWidgets.QLabel(self.tab_31)
        self.label_d3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_d3.setObjectName('label_d3')
        self.label_d3.setText('风险分析')

        self.textBrowser_3 = QtWidgets.QTextBrowser(self.tab_31)
        self.textBrowser_3.setObjectName('textBrowser_3')

        # 调整字体 / 字号
        font = QtGui.QFont()
        font.setFamily('黑体')
        font.setPointSize(11)
        self.label_d1.setFont(font)
        self.label_d2.setFont(font)
        self.label_d3.setFont(font)
        font.setFamily('宋体')
        font.setPointSize(10)
        self.textBrowser_1.setFont(font)
        self.textBrowser_2.setFont(font)
        self.textBrowser_3.setFont(font)

        self.tabWidget_4.addTab(self.tab_31, '\t合约详情\t')
        # /tabWidget_4 -> tab_31

        # tabWidget_4 -> tab_32: K线数据
        self.tab_32 = QtWidgets.QWidget()
        self.tab_32.setObjectName('tab_32')

        # tabWidget_5: 分时 / 日线 / 周线 / 月线
        self.tabWidget_5 = QtWidgets.QTabWidget(self.tab_32)
        self.tabWidget_5.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget_5.setObjectName('tabWidget_5')

        # K线图标签
        self.label_hour_x = QtWidgets.QLabel(self.tab_32)
        self.label_hour_x.setAlignment(QtCore.Qt.AlignCenter)
        self.label_hour_x.setObjectName('label_hour_x')
        self.label_hour_x.hide()

        self.label_hour_y = QtWidgets.QLabel(self.tab_32)
        self.label_hour_y.setAlignment(QtCore.Qt.AlignCenter)
        self.label_hour_y.setObjectName('label_hour_y')
        self.label_hour_y.hide()

        self.label_x = QtWidgets.QLabel(self.tab_32)
        self.label_x.setAlignment(QtCore.Qt.AlignCenter)
        self.label_x.setObjectName('label_x')
        self.label_x.hide()

        self.label_y = QtWidgets.QLabel(self.tab_32)
        self.label_y.setAlignment(QtCore.Qt.AlignCenter)
        self.label_y.setObjectName('label_y')
        self.label_y.hide()

        # tabWidget_5 -> tab_hour: 分时
        self.tab_hour = QtWidgets.QWidget()
        self.tab_hour.setObjectName('tab_hour')

        # 分时标签
        self.label_hour = QtWidgets.QLabel(self.tab_hour)
        self.label_hour.setGeometry(QtCore.QRect(0, 0, 100, 20))
        self.label_hour.setObjectName('label_hour')
        self.label_hour.setText('分时')

        self.label_hour_v = QtWidgets.QLabel(self.tab_hour)
        self.label_hour_v.setObjectName('label_hour_v')
        self.label_hour_v.setText('成交量')

        self.label_hour_a = QtWidgets.QLabel(self.tab_hour)
        self.label_hour_a.setGeometry(QtCore.QRect(100, 0, 100, 20))
        self.label_hour_a.setObjectName('label_hour_a')
        self.label_hour_a.setText('均线')
        self.label_hour_a.setStyleSheet('color: #FFFF00;')

        # 分时K线
        self.LayoutWidget_hour = QtWidgets.QWidget(self.tab_hour)
        self.LayoutWidget_hour.setObjectName('LayoutWidget_hour')

        self.Layout_hour = QtWidgets.QVBoxLayout(self.LayoutWidget_hour)
        self.Layout_hour.setContentsMargins(0, 0, 0, 0)
        self.Layout_hour.setObjectName('Layout_hour')

        self.k_line_hour = k_line.hour_line(solution.get_empty_k_line(),
                                            self.label_hour_x, self.label_hour_y)
        self.exrwidget_hour = self.k_line_hour.draw_chart()

        self.Layout_hour.addWidget(self.exrwidget_hour)

        # 分时成交
        self.LayoutWidget_hour_v = QtWidgets.QWidget(self.tab_hour)
        self.LayoutWidget_hour_v.setObjectName('LayoutWidget_hour_v')

        self.Layout_hour_v = QtWidgets.QVBoxLayout(self.LayoutWidget_hour_v)
        self.Layout_hour_v.setContentsMargins(0, 0, 0, 0)
        self.Layout_hour_v.setObjectName('Layout_hour_v')

        self.volume_hour = k_line.v_bar_hour(solution.get_empty_k_line())
        self.exrwidget_hour_v = self.volume_hour.draw_chart()

        self.Layout_hour_v.addWidget(self.exrwidget_hour_v)

        self.tabWidget_5.addTab(self.tab_hour, '\t分时\t')
        # /tabWidget_5 -> tab_hour

        # tabWidget_5 -> tab_d: 日线
        self.tab_d = QtWidgets.QWidget()
        self.tab_d.setObjectName('tab_d')

        # 日线标签
        self.label_d = QtWidgets.QLabel(self.tab_d)
        self.label_d.setGeometry(QtCore.QRect(0, 0, 150, 20))
        self.label_d.setObjectName('label_d')
        self.label_d.setText('日线')

        self.label_d_v = QtWidgets.QLabel(self.tab_d)
        self.label_d_v.setObjectName('label_d_v')
        self.label_d_v.setText('成交量')

        self.label_d_ma5 = QtWidgets.QLabel(self.tab_d)
        self.label_d_ma5.setGeometry(QtCore.QRect(150, 0, 100, 20))
        self.label_d_ma5.setObjectName('label_d_ma5')
        self.label_d_ma5.setText('MA5:')
        self.label_d_ma5.setStyleSheet('color: #FFFFFF;')

        self.label_d_ma10 = QtWidgets.QLabel(self.tab_d)
        self.label_d_ma10.setGeometry(QtCore.QRect(250, 0, 100, 20))
        self.label_d_ma10.setObjectName('label_d_ma10')
        self.label_d_ma10.setText('MA10:')
        self.label_d_ma10.setStyleSheet('color: #FFFF00;')

        self.label_d_ma20 = QtWidgets.QLabel(self.tab_d)
        self.label_d_ma20.setGeometry(QtCore.QRect(350, 0, 100, 20))
        self.label_d_ma20.setObjectName('label_d_ma20')
        self.label_d_ma20.setText('MA20:')
        self.label_d_ma20.setStyleSheet('color: #FF00FF;')

        self.label_d_MACD = QtWidgets.QLabel(self.tab_d)
        self.label_d_MACD.setObjectName('label_d_MACD')
        self.label_d_MACD.setText('MACD(12,26,9)')

        self.label_d_diff = QtWidgets.QLabel(self.tab_d)
        self.label_d_diff.setObjectName('label_d_diff')
        self.label_d_diff.setText('DIF:')
        self.label_d_diff.setStyleSheet('color: #FFFFFF;')

        self.label_d_dea = QtWidgets.QLabel(self.tab_d)
        self.label_d_dea.setObjectName('label_d_dea')
        self.label_d_dea.setText('DEA:')
        self.label_d_dea.setStyleSheet('color: #FFFF00;')

        self.label_d_macd = QtWidgets.QLabel(self.tab_d)
        self.label_d_macd.setObjectName('label_d_macd')
        self.label_d_macd.setText('MACD:')
        self.label_d_macd.setStyleSheet('color: #FF00FF;')

        # 日线K线
        self.LayoutWidget_d = QtWidgets.QWidget(self.tab_d)
        self.LayoutWidget_d.setObjectName('LayoutWidget_d')

        self.Layout_d = QtWidgets.QVBoxLayout(self.LayoutWidget_d)
        self.Layout_d.setContentsMargins(0, 0, 0, 0)
        self.Layout_d.setObjectName('Layout_d')

        self.k_line_d = k_line.k_line(solution.get_empty_k_line(), self.label_x, self.label_y)
        self.exrwidget_d = self.k_line_d.draw_chart()

        self.Layout_d.addWidget(self.exrwidget_d)

        # 日线成交
        self.LayoutWidget_d_v = QtWidgets.QWidget(self.tab_d)
        self.LayoutWidget_d_v.setObjectName('LayoutWidget_d_v')

        self.Layout_d_v = QtWidgets.QVBoxLayout(self.LayoutWidget_d_v)
        self.Layout_d_v.setContentsMargins(0, 0, 0, 0)
        self.Layout_d_v.setObjectName('Layout_d_v')

        self.volume_d = k_line.v_bar(solution.get_empty_k_line())
        self.exrwidget_d_v = self.volume_d.draw_chart()

        self.Layout_d_v.addWidget(self.exrwidget_d_v)

        # 日线MACD
        self.LayoutWidget_d_MACD = QtWidgets.QWidget(self.tab_d)
        self.LayoutWidget_d_MACD.setObjectName('LayoutWidget_d_MACD')

        self.Layout_d_MACD = QtWidgets.QVBoxLayout(self.LayoutWidget_d_MACD)
        self.Layout_d_MACD.setContentsMargins(0, 0, 0, 0)
        self.Layout_d_MACD.setObjectName('Layout_d_MACD')

        self.MACD_d = k_line.MACD(solution.get_empty_k_line())
        self.exrwidget_d_MACD = self.MACD_d.draw_chart()

        self.Layout_d_MACD.addWidget(self.exrwidget_d_MACD)

        self.tabWidget_5.addTab(self.tab_d, '\t日线\t')
        # /tabWidget_5 -> tab_d

        # tabWidget_5 -> tab_w: 周线
        self.tab_w = QtWidgets.QWidget()
        self.tab_w.setObjectName('tab_w')

        # 周线标签
        self.label_w = QtWidgets.QLabel(self.tab_w)
        self.label_w.setGeometry(QtCore.QRect(0, 0, 150, 20))
        self.label_w.setObjectName('label_w')
        self.label_w.setText('周线')

        self.label_w_v = QtWidgets.QLabel(self.tab_w)
        self.label_w_v.setObjectName('label_w_v')
        self.label_w_v.setText('成交量')

        self.label_w_ma5 = QtWidgets.QLabel(self.tab_w)
        self.label_w_ma5.setGeometry(QtCore.QRect(150, 0, 100, 20))
        self.label_w_ma5.setObjectName('label_w_ma5')
        self.label_w_ma5.setText('MA5:')
        self.label_w_ma5.setStyleSheet('color: #FFFFFF;')

        self.label_w_ma10 = QtWidgets.QLabel(self.tab_w)
        self.label_w_ma10.setGeometry(QtCore.QRect(250, 0, 100, 20))
        self.label_w_ma10.setObjectName('label_w_ma10')
        self.label_w_ma10.setText('MA10:')
        self.label_w_ma10.setStyleSheet('color: #FFFF00;')

        self.label_w_ma20 = QtWidgets.QLabel(self.tab_w)
        self.label_w_ma20.setGeometry(QtCore.QRect(350, 0, 100, 20))
        self.label_w_ma20.setObjectName('label_w_ma20')
        self.label_w_ma20.setText('MA20:')
        self.label_w_ma20.setStyleSheet('color: #FF00FF;')

        self.label_w_MACD = QtWidgets.QLabel(self.tab_w)
        self.label_w_MACD.setObjectName('label_w_MACD')
        self.label_w_MACD.setText('MACD(12,26,9)')

        self.label_w_diff = QtWidgets.QLabel(self.tab_w)
        self.label_w_diff.setObjectName('label_w_diff')
        self.label_w_diff.setText('DIF:')
        self.label_w_diff.setStyleSheet('color: #FFFFFF;')

        self.label_w_dea = QtWidgets.QLabel(self.tab_w)
        self.label_w_dea.setObjectName('label_w_dea')
        self.label_w_dea.setText('DEA:')
        self.label_w_dea.setStyleSheet('color: #FFFF00;')

        self.label_w_macd = QtWidgets.QLabel(self.tab_w)
        self.label_w_macd.setObjectName('label_w_macd')
        self.label_w_macd.setText('MACD:')
        self.label_w_macd.setStyleSheet('color: #FF00FF;')

        # 周线K线
        self.LayoutWidget_w = QtWidgets.QWidget(self.tab_w)
        self.LayoutWidget_w.setObjectName('LayoutWidget_w')

        self.Layout_w = QtWidgets.QVBoxLayout(self.LayoutWidget_w)
        self.Layout_w.setContentsMargins(0, 0, 0, 0)
        self.Layout_w.setObjectName('Layout_w')

        self.k_line_w = k_line.k_line(solution.get_empty_k_line(), self.label_x, self.label_y)
        self.exrwidget_w = self.k_line_w.draw_chart()

        self.Layout_w.addWidget(self.exrwidget_w)

        # 周线成交
        self.LayoutWidget_w_v = QtWidgets.QWidget(self.tab_w)
        self.LayoutWidget_w_v.setObjectName('LayoutWidget_w_v')

        self.Layout_w_v = QtWidgets.QVBoxLayout(self.LayoutWidget_w_v)
        self.Layout_w_v.setContentsMargins(0, 0, 0, 0)
        self.Layout_w_v.setObjectName('Layout_w_v')

        self.volume_w = k_line.v_bar(solution.get_empty_k_line())
        self.exrwidget_w_v = self.volume_w.draw_chart()

        self.Layout_w_v.addWidget(self.exrwidget_w_v)

        # 周线MACD
        self.LayoutWidget_w_MACD = QtWidgets.QWidget(self.tab_w)
        self.LayoutWidget_w_MACD.setObjectName('LayoutWidget_w_MACD')

        self.Layout_w_MACD = QtWidgets.QVBoxLayout(self.LayoutWidget_w_MACD)
        self.Layout_w_MACD.setContentsMargins(0, 0, 0, 0)
        self.Layout_w_MACD.setObjectName('Layout_w_MACD')

        self.MACD_w = k_line.MACD(solution.get_empty_k_line())
        self.exrwidget_w_MACD = self.MACD_w.draw_chart()

        self.Layout_w_MACD.addWidget(self.exrwidget_w_MACD)

        self.tabWidget_5.addTab(self.tab_w, '\t周线\t')
        # /tabWidget_5 -> tab_w

        # tabWidget_5 -> tab_m: 月线
        self.tab_m = QtWidgets.QWidget()
        self.tab_m.setObjectName('tab_m')

        # 月线标签
        self.label_m = QtWidgets.QLabel(self.tab_m)
        self.label_m.setGeometry(QtCore.QRect(0, 0, 150, 20))
        self.label_m.setObjectName('label_m')
        self.label_m.setText('月线')

        self.label_m_v = QtWidgets.QLabel(self.tab_m)
        self.label_m_v.setObjectName('label_m_v')
        self.label_m_v.setText('成交量')

        self.label_m_ma5 = QtWidgets.QLabel(self.tab_m)
        self.label_m_ma5.setGeometry(QtCore.QRect(150, 0, 100, 20))
        self.label_m_ma5.setObjectName('label_m_ma5')
        self.label_m_ma5.setText('MA5:')
        self.label_m_ma5.setStyleSheet('color: #FFFFFF;')

        self.label_m_ma10 = QtWidgets.QLabel(self.tab_m)
        self.label_m_ma10.setGeometry(QtCore.QRect(250, 0, 100, 20))
        self.label_m_ma10.setObjectName('label_m_ma10')
        self.label_m_ma10.setText('MA10:')
        self.label_m_ma10.setStyleSheet('color: #FFFF00;')

        self.label_m_ma20 = QtWidgets.QLabel(self.tab_m)
        self.label_m_ma20.setGeometry(QtCore.QRect(350, 0, 100, 20))
        self.label_m_ma20.setObjectName('label_m_ma20')
        self.label_m_ma20.setText('MA20:')
        self.label_m_ma20.setStyleSheet('color: #FF00FF;')

        self.label_m_MACD = QtWidgets.QLabel(self.tab_m)
        self.label_m_MACD.setObjectName('label_m_MACD')
        self.label_m_MACD.setText('MACD(12,26,9)')

        self.label_m_diff = QtWidgets.QLabel(self.tab_m)
        self.label_m_diff.setObjectName('label_m_diff')
        self.label_m_diff.setText('DIF:')
        self.label_m_diff.setStyleSheet('color: #FFFFFF;')

        self.label_m_dea = QtWidgets.QLabel(self.tab_m)
        self.label_m_dea.setObjectName('label_m_dea')
        self.label_m_dea.setText('DEA:')
        self.label_m_dea.setStyleSheet('color: #FFFF00;')

        self.label_m_macd = QtWidgets.QLabel(self.tab_m)
        self.label_m_macd.setObjectName('label_m_macd')
        self.label_m_macd.setText('MACD:')
        self.label_m_macd.setStyleSheet('color: #FF00FF;')

        # 月线K线
        self.LayoutWidget_m = QtWidgets.QWidget(self.tab_m)
        self.LayoutWidget_m.setObjectName('LayoutWidget_m')

        self.Layout_m = QtWidgets.QVBoxLayout(self.LayoutWidget_m)
        self.Layout_m.setContentsMargins(0, 0, 0, 0)
        self.Layout_m.setObjectName('Layout_m')

        self.k_line_m = k_line.k_line(solution.get_empty_k_line(), self.label_x, self.label_y)
        self.exrwidget_m = self.k_line_m.draw_chart()

        self.Layout_m.addWidget(self.exrwidget_m)

        # 月线成交
        self.LayoutWidget_m_v = QtWidgets.QWidget(self.tab_m)
        self.LayoutWidget_m_v.setObjectName('LayoutWidget_m_v')

        self.Layout_m_v = QtWidgets.QVBoxLayout(self.LayoutWidget_m_v)
        self.Layout_m_v.setContentsMargins(0, 0, 0, 0)
        self.Layout_m_v.setObjectName('Layout_m_v')

        self.volume_m = k_line.v_bar(solution.get_empty_k_line())
        self.exrwidget_m_v = self.volume_m.draw_chart()

        self.Layout_m_v.addWidget(self.exrwidget_m_v)

        # 月线MACD
        self.LayoutWidget_m_MACD = QtWidgets.QWidget(self.tab_m)
        self.LayoutWidget_m_MACD.setObjectName('LayoutWidget_m_MACD')

        self.Layout_m_MACD = QtWidgets.QVBoxLayout(self.LayoutWidget_m_MACD)
        self.Layout_m_MACD.setContentsMargins(0, 0, 0, 0)
        self.Layout_m_MACD.setObjectName('Layout_m_MACD')

        self.MACD_m = k_line.MACD(solution.get_empty_k_line())
        self.exrwidget_m_MACD = self.MACD_m.draw_chart()

        self.Layout_m_MACD.addWidget(self.exrwidget_m_MACD)

        self.tabWidget_5.addTab(self.tab_m, '\t月线\t')
        # /tabWidget_5 -> tab_m
        # /tabWidget_5

        self.tabWidget_4.addTab(self.tab_32, '\tK线数据\t')
        # /tabWidget_4 -> tab_32
        # /tabWidget_4

        # 槽: pushButton_code -> tab_3
        self.pushButton_code.clicked.connect(lambda: self.update_tab_3())

        self.tabWidget_1.addTab(self.tab_3, '\t合约分析\t')
        # /tabWidget_1 -> tab_3

    # tabWidget_1 -> tab_4: 价值潜力榜
    def setup_tab_4(self):
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName('tab_4')

        # 最低买量
        self.label_rank_buy = QtWidgets.QLabel(self.tab_4)
        self.label_rank_buy.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_rank_buy.setObjectName('label_rank_buy')
        self.label_rank_buy.setGeometry(QtCore.QRect(20, 20, 100, 30))
        self.label_rank_buy.setText('最低买量：')

        self.spinBox_rank_buy = QtWidgets.QSpinBox(self.tab_4)
        self.spinBox_rank_buy.setGeometry(QtCore.QRect(120, 20, 80, 30))
        self.spinBox_rank_buy.setObjectName('spinBox_rank_buy')
        self.spinBox_rank_buy.setMinimum(0)
        self.spinBox_rank_buy.setValue(0)

        # 最低卖量
        self.label_rank_sell = QtWidgets.QLabel(self.tab_4)
        self.label_rank_sell.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_rank_sell.setObjectName('label_rank_sell')
        self.label_rank_sell.setGeometry(QtCore.QRect(220, 20, 100, 30))
        self.label_rank_sell.setText('最低卖量：')

        self.spinBox_rank_sell = QtWidgets.QSpinBox(self.tab_4)
        self.spinBox_rank_sell.setGeometry(QtCore.QRect(320, 20, 80, 30))
        self.spinBox_rank_sell.setObjectName('spinBox_rank_sell')
        self.spinBox_rank_sell.setMinimum(0)
        self.spinBox_rank_sell.setValue(0)

        # 最低成交量
        self.label_rank_v = QtWidgets.QLabel(self.tab_4)
        self.label_rank_v.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_rank_v.setObjectName('label_rank_v')
        self.label_rank_v.setGeometry(QtCore.QRect(440, 20, 100, 30))
        self.label_rank_v.setText('最低成交量：')

        self.spinBox_rank_v = QtWidgets.QSpinBox(self.tab_4)
        self.spinBox_rank_v.setGeometry(QtCore.QRect(520, 20, 80, 30))
        self.spinBox_rank_v.setObjectName('spinBox_rank_v')
        self.spinBox_rank_v.setMinimum(0)
        self.spinBox_rank_v.setValue(50)

        # 交易类型
        self.label_rank_bs = QtWidgets.QLabel(self.tab_4)
        self.label_rank_bs.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_rank_bs.setObjectName('label_rank_bs')
        self.label_rank_bs.setGeometry(QtCore.QRect(620, 20, 100, 30))
        self.label_rank_bs.setText('交易类型：')

        self.radioButton_buy = QtWidgets.QRadioButton(self.tab_4)
        self.radioButton_buy.setGeometry(QtCore.QRect(720, 20, 90, 30))
        self.radioButton_buy.setObjectName('radioButton_buy')
        self.radioButton_buy.setText('买进期权')
        self.radioButton_buy.setChecked(True)

        self.radioButton_sell = QtWidgets.QRadioButton(self.tab_4)
        self.radioButton_sell.setGeometry(QtCore.QRect(820, 20, 90, 30))
        self.radioButton_sell.setObjectName('radioButton_sell')
        self.radioButton_sell.setText('卖出期权')

        # 交易偏好
        self.label_rank_w = QtWidgets.QLabel(self.tab_4)
        self.label_rank_w.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_rank_w.setObjectName('label_rank_w')
        self.label_rank_w.setGeometry(QtCore.QRect(940, 20, 100, 30))
        self.label_rank_w.setText('交易偏好：')

        self.label_rank_w_l = QtWidgets.QLabel(self.tab_4)
        self.label_rank_w_l.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_rank_w_l.setObjectName('label_rank_w_l')
        self.label_rank_w_l.setGeometry(QtCore.QRect(1040, 10, 40, 20))
        self.label_rank_w_l.setText('长期')

        self.label_rank_w_s = QtWidgets.QLabel(self.tab_4)
        self.label_rank_w_s.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_rank_w_s.setObjectName('label_rank_w_s')
        self.label_rank_w_s.setGeometry(QtCore.QRect(1120, 10, 40, 20))
        self.label_rank_w_s.setText('短期')

        self.horizontalSlider_rank = QtWidgets.QSlider(self.tab_4)
        self.horizontalSlider_rank.setGeometry(QtCore.QRect(1040, 30, 120, 20))
        self.horizontalSlider_rank.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_rank.setObjectName('horizontalSlider_rank')

        # 筛选按钮
        self.pushButton_rank = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_rank.setGeometry(QtCore.QRect(1220, 20, 80, 30))
        self.pushButton_rank.setObjectName('pushButton_rank')
        self.pushButton_rank.setText('筛选')

        # tableWidget_rank: 价值潜力榜表格
        self.tableWidget_rank = QtWidgets.QTableWidget(self.tab_4)
        self.tableWidget_rank.setObjectName('tableWidget_rank')
        self.tableWidget_rank.setShowGrid(True)  # 显示网格
        self.tableWidget_rank.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  # 不显示水平滚动条
        self.tableWidget_rank.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget_rank.setColumnCount(17)  # 17列
        self.tableWidget_rank.setRowCount(0)
        self.tableWidget_rank.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 禁止修改
        self.tableWidget_rank.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # 选择行

        self.tableWidget_rank.setHorizontalHeaderLabels(['合约代码', '合约简称', '标的股票', '涨幅', '最新价', '买价', '卖价', '买量', '卖量',
                                                         '持仓量', '成交量', '振幅', '内在价值', '时间价值', '行权概率',
                                                         '隐含波动率', '价值潜力'])
        self.tableWidget_rank.verticalHeader().setVisible(False)  # 不显示垂直表头

        self.tableWidget_rank.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # 允许弹出菜单

        # 槽: tabWidget_1 -> tableWidget_rank(当选中'价值潜力榜'标签时再加载数据)
        self.tabWidget_1.currentChanged.connect(lambda: self.load_tableWidget_rank())
        # 槽: pushButton_rank -> tableWidget_rank
        self.pushButton_rank.clicked.connect(lambda: self.update_tableWidget_rank())

        self.tabWidget_1.addTab(self.tab_4, '\t价值潜力榜\t')
        # /tabWidget_1 -> tab_4

    '''
    股票期权
    '''

    # 加载tableWidget_1(分类报价表格)
    def load_tableWidget_1(self):
        # 启动时第一次setupUi, 暂不加载
        if self.open_flag:
            self.open_flag = False
            return
        # 未选中'分类报价'标签 / 表格中已经存在数据: 不再加载
        if self.tabWidget_2.currentIndex() != 0 or self.tableWidget_1.rowCount():
            return
        self.update_tableWidget_1()

    # 更新tableWidget_1(分类报价表格)
    def update_tableWidget_1(self):
        data = solution.get_tableWidget_1(self.comboBox_ex11.currentText())
        self.tableWidget_1.setRowCount(len(data))
        for i in range(len(data)):
            for j in range(17):
                if j == 2:  # 涨幅, 保留两位小数
                    t = float(data[i][2])
                    self.tableWidget_1.setItem(i, 2, QtWidgets.QTableWidgetItem(format(t, '.2f') + '%'))
                    if t > 0:
                        self.tableWidget_1.item(i, 2).setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
                    elif t < 0:
                        self.tableWidget_1.item(i, 2).setForeground(QtGui.QBrush(QtGui.QColor(0, 255, 0)))
                else:
                    self.tableWidget_1.setItem(i, j, QtWidgets.QTableWidgetItem(data[i][j]))

                # 居中
                self.tableWidget_1.item(i, j).setTextAlignment(QtCore.Qt.AlignCenter)

    # 更新comboBox_pz12(期权品种)
    def update_comboBox_pz12(self):
        self.comboBox_pz12.clear()
        self.comboBox_pz12.addItems(solution.get_comboBox_pz12(self.comboBox_ex12.currentText()))

    # 更新comboBox_ym12(合约月份)
    def update_comboBox_ym12(self):
        self.comboBox_ym12.clear()
        self.comboBox_ym12.addItems(solution.get_comboBox_ym12(self.comboBox_ex12.currentText()))

    # 更新label_da12_text(到期日)
    def update_label_da12_text(self):
        if not self.comboBox_ym12.count():
            self.label_da12_text.setText('')
            return
        date, day = solution.get_label_da12_text(self.comboBox_ex12.currentText(), self.comboBox_ym12.currentText())
        self.label_da12_text.setText(date + '（' + str(day) + '天）')

    # 更新label_ta12_text(标的资产)
    def update_label_ta12_text(self):
        if not self.comboBox_pz12.count():
            self.label_ta12_text.setText('')
            return
        self.label_ta12_text.setText(solution.get_label_ta12_text(self.comboBox_pz12.currentText()))

    # 更新tableWidget_2(T型报价表格)
    def update_tableWidget_2(self):
        if not self.comboBox_pz12.count() or not self.comboBox_ym12.count():
            self.tableWidget_2.clearContents()
            return
        self.list1, data, flag = solution.get_tableWidget_2(self.comboBox_pz12.currentText(),
                                                            self.comboBox_ym12.currentText())
        self.tableWidget_2.setRowCount(len(data))
        for i in range(len(data)):
            for j in range(17):
                if j == 6 or j == 10:  # 涨幅, 保留两位小数
                    t = float(data[i][j])
                    self.tableWidget_2.setItem(i, j, QtWidgets.QTableWidgetItem(format(t, '.2f') + '%'))
                    if t > 0:
                        self.tableWidget_2.item(i, j).setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
                    elif t < 0:
                        self.tableWidget_2.item(i, j).setForeground(QtGui.QBrush(QtGui.QColor(0, 255, 0)))
                else:
                    self.tableWidget_2.setItem(i, j, QtWidgets.QTableWidgetItem(data[i][j]))

                # 居中
                self.tableWidget_2.item(i, j).setTextAlignment(QtCore.Qt.AlignCenter)

                # 根据虚实值标记染色
                if flag:
                    if flag[i] == '2':
                        if j < 8:
                            self.tableWidget_2.item(i, j).setBackground(QtGui.QBrush(QtGui.QColor(35, 5, 5)))
                        elif j == 8:
                            self.tableWidget_2.item(i, 8).setBackground(QtGui.QBrush(QtGui.QColor(35, 45, 55)))
                        else:
                            self.tableWidget_2.item(i, j).setBackground(QtGui.QBrush(QtGui.QColor(5, 35, 5)))
                    else:
                        if j < 8:
                            self.tableWidget_2.item(i, j).setBackground(QtGui.QBrush(QtGui.QColor(5, 35, 5)))
                        elif j == 8:
                            self.tableWidget_2.item(i, 8).setBackground(QtGui.QBrush(QtGui.QColor(35, 45, 55)))
                        else:
                            self.tableWidget_2.item(i, j).setBackground(QtGui.QBrush(QtGui.QColor(35, 5, 5)))

    # 展示tableWidget_1菜单
    def show_tableWidget_1_menu(self, pos):
        # 未选中表格中的一行 / 选中多行
        if not self.tableWidget_1.selectionModel().selection().indexes() or \
                self.tableWidget_1.selectionModel().selection().indexes()[-1].row() - \
                self.tableWidget_1.selectionModel().selection().indexes()[0].row():
            menu_r = QtWidgets.QMenu()
            item_r = menu_r.addAction('刷新')

            action = menu_r.exec_(self.tableWidget_1.mapToGlobal(pos))

            if action == item_r:
                self.update_tableWidget_1()
            return

        menu = QtWidgets.QMenu()
        item1 = menu.addAction('刷新')
        item2 = menu.addAction('分析合约')

        action = menu.exec_(self.tableWidget_1.mapToGlobal(pos))
        idx = self.tableWidget_1.selectionModel().selection().indexes()[0].row()

        if action == item1:  # 刷新
            self.update_tableWidget_1()
        elif action == item2:  # 分析合约
            self.lineEdit_code.setText(self.tableWidget_1.item(idx, 0).text())
            self.update_tab_3()

            self.tabWidget_1.setCurrentIndex(2)
            self.tabWidget_4.setCurrentIndex(0)
        else:  # 未选择菜单选项
            return

    # 展示tableWidget_2菜单
    def show_tableWidget_2_menu(self, pos):
        # 当前未显示 / 未选中表格中的一行 / 选中多行
        if not self.list1 or not self.tableWidget_2.selectionModel().selection().indexes() or \
                self.tableWidget_2.selectionModel().selection().indexes()[-1].row() - \
                self.tableWidget_2.selectionModel().selection().indexes()[0].row():
            menu_r = QtWidgets.QMenu()
            item_r = menu_r.addAction('刷新')

            action = menu_r.exec_(self.tableWidget_2.mapToGlobal(pos))

            if action == item_r:
                self.update_tableWidget_2()
            return

        menu = QtWidgets.QMenu()
        item1 = menu.addAction('刷新')
        item2 = menu.addAction('分析看涨合约')
        item3 = menu.addAction('分析看跌合约')

        action = menu.exec_(self.tableWidget_2.mapToGlobal(pos))
        idx = self.tableWidget_2.selectionModel().selection().indexes()[0].row()

        if action == item1:  # 刷新
            self.update_tableWidget_2()
        elif action == item2:  # 分析看涨合约
            self.lineEdit_code.setText(self.list1[idx])
            self.update_tab_3()

            self.tabWidget_1.setCurrentIndex(2)
            if self.comboBox_ex12.currentText() == '中金所':
                self.tabWidget_4.setCurrentIndex(1)
            else:
                self.tabWidget_4.setCurrentIndex(0)
        elif action == item3:  # 分析看跌合约
            self.lineEdit_code.setText(self.list1[int(len(self.list1) / 2) + idx])
            self.update_tab_3()

            self.tabWidget_1.setCurrentIndex(2)
            if self.comboBox_ex12.currentText() == '中金所':
                self.tabWidget_4.setCurrentIndex(1)
            else:
                self.tabWidget_4.setCurrentIndex(0)
        else:  # 未选择菜单选项
            return

    '''
    商品期权
    '''

    # 更新到期月份
    def update_comboBox_ym21(self):
        self.comboBox_ym21.clear()
        self.comboBox_ym21.addItems(solution.get_comboBox_ym21(self.comboBox_pz21.currentIndex()))

    # 更新交易所
    def update_label_ex21_text(self):
        self.label_ex21_text.setText(solution.get_label_ex21_text(self.comboBox_pz21.currentIndex()))

    # 加载tableWidget_3(T型报价表格)
    def load_tableWidget_3(self):
        # 未选中'商品期权'标签 / 表格中已经存在数据: 不再加载
        if self.tabWidget_1.currentIndex() != 1 or self.tableWidget_3.rowCount():
            return
        self.update_tableWidget_3()

    # 更新tableWidget_3(T型报价表格)
    def update_tableWidget_3(self):
        if not self.comboBox_ym21.count():
            self.tableWidget_3.clearContents()
            return
        self.list2, data = solution.get_tableWidget_3(self.comboBox_pz21.currentIndex(),
                                                      self.comboBox_ym21.currentText())
        self.tableWidget_3.setRowCount(len(data))
        for i in range(len(data)):
            for j in range(15):
                if data[i][j] == 'nan':
                    self.tableWidget_3.setItem(i, j, QtWidgets.QTableWidgetItem('-'))
                    self.tableWidget_3.item(i, j).setTextAlignment(QtCore.Qt.AlignCenter)
                    continue
                if j == 5 or j == 9:  # 涨幅, 保留两位小数
                    t = float(data[i][j])
                    self.tableWidget_3.setItem(i, j, QtWidgets.QTableWidgetItem(format(t, '.2f') + '%'))
                    if t > 0:
                        self.tableWidget_3.item(i, j).setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
                    elif t < 0:
                        self.tableWidget_3.item(i, j).setForeground(QtGui.QBrush(QtGui.QColor(0, 255, 0)))
                else:
                    self.tableWidget_3.setItem(i, j, QtWidgets.QTableWidgetItem(data[i][j]))

                # 居中
                self.tableWidget_3.item(i, j).setTextAlignment(QtCore.Qt.AlignCenter)

                if j == 7:
                    self.tableWidget_3.item(i, 7).setBackground(QtGui.QBrush(QtGui.QColor(35, 45, 55)))

    # 展示tableWidget_3菜单
    def show_tableWidget_3_menu(self, pos):
        # 当前未显示 / 未选中表格中的一行 / 选中多行
        if not self.list2 or not self.tableWidget_3.selectionModel().selection().indexes() or \
                self.tableWidget_3.selectionModel().selection().indexes()[-1].row() - \
                self.tableWidget_3.selectionModel().selection().indexes()[0].row():
            menu_r = QtWidgets.QMenu()
            item_r = menu_r.addAction('刷新')

            action = menu_r.exec_(self.tableWidget_3.mapToGlobal(pos))

            if action == item_r:
                self.update_tableWidget_3()
            return

        menu = QtWidgets.QMenu()
        item1 = menu.addAction('刷新')
        item2 = menu.addAction('分析看涨合约')
        item3 = menu.addAction('分析看跌合约')

        action = menu.exec_(self.tableWidget_3.mapToGlobal(pos))
        idx = self.tableWidget_3.selectionModel().selection().indexes()[0].row()

        if action == item1:  # 刷新
            self.update_tableWidget_3()
        elif action == item2:  # 分析看涨合约
            self.lineEdit_code.setText(self.list2[idx])
            self.update_tab_3()

            self.tabWidget_1.setCurrentIndex(2)
            self.tabWidget_4.setCurrentIndex(1)
            self.tabWidget_5.setCurrentIndex(1)
        elif action == item3:  # 分析看跌合约
            self.lineEdit_code.setText(self.list2[int(len(self.list2) / 2) + idx])
            self.update_tab_3()

            self.tabWidget_1.setCurrentIndex(2)
            self.tabWidget_4.setCurrentIndex(1)
            self.tabWidget_5.setCurrentIndex(1)
        else:  # 未选择菜单选项
            return

    '''
    合约分析
    '''

    # 更新合约分析
    def update_tab_3(self):
        # 查询的合约即当前显示的合约
        if self.code == self.lineEdit_code.text():
            return

        flag = self.update_tab_31()

        self.update_tab_32(flag)

        if flag <= 0:
            self.code = None
        else:
            self.code = self.lineEdit_code.text()

    # 更新合约详情
    def update_tab_31(self):
        flag, text1, text2, text3 = solution.get_tab_31(self.lineEdit_code.text())
        if flag == 0:
            self.label_err.setText('合约代码不能为空！')
        elif flag < 0:
            self.label_err.setText('您查询的期权合约不存在！')
        else:
            self.label_err.setText('')
        self.textBrowser_1.setText(text1)
        self.textBrowser_2.setText(text2)
        self.textBrowser_3.setText(text3)
        return flag

    # 更新K线数据
    def update_tab_32(self, flag):
        if flag <= 0:
            data_hour = solution.get_empty_k_line()
            data_d = solution.get_empty_k_line()
            data_w = solution.get_empty_k_line()
            data_m = solution.get_empty_k_line()
        else:
            data_hour, data_d, data_w, data_m = solution.get_k_line(self.lineEdit_code.text())

        # 分时K线
        self.k_line_hour = k_line.hour_line(data_hour, self.label_hour_x, self.label_hour_y)
        self.exrwidget_hour = self.k_line_hour.draw_chart()

        self.Layout_hour.itemAt(0).widget().deleteLater()
        self.Layout_hour.addWidget(self.exrwidget_hour)

        # 分时成交
        if len(data_hour):
            max = data_hour['v'].max()
            i = 0
            pow = 1
            while max > 9999:
                max = max / 10
                i += 1
                pow *= 10
            if i > 0:
                self.label_hour_v.setText('成交量(*10^{:})'.format(i))
            else:
                self.label_hour_v.setText('成交量')
            data_hour['v'] = data_hour['v'].map(lambda x: x / pow)

        self.volume_hour = k_line.v_bar_hour(data_hour)
        self.exrwidget_hour_v = self.volume_hour.draw_chart()

        self.Layout_hour_v.itemAt(0).widget().deleteLater()
        self.Layout_hour_v.addWidget(self.exrwidget_hour_v)

        # 日线标签
        if not len(data_d):
            self.label_d_ma5.setText('MA5:')
            self.label_d_ma10.setText('MA10:')
            self.label_d_ma20.setText('MA20:')
            self.label_d_diff.setText('DIF:')
            self.label_d_dea.setText('DEA:')
            self.label_d_macd.setText('MACD:')
        else:
            self.label_d_ma5.setText('MA5:' + str(round(data_d['ma5'][-1], 4)))
            self.label_d_ma10.setText('MA10:' + str(round(data_d['ma10'][-1], 4)))
            self.label_d_ma20.setText('MA20:' + str(round(data_d['ma20'][-1], 4)))
            self.label_d_diff.setText('DIF:' + str(round(data_d['diff'][-1], 4)))
            self.label_d_dea.setText('DEA:' + str(round(data_d['dea'][-1], 4)))
            self.label_d_macd.setText('MACD:' + str(round(data_d['macd'][-1], 4)))

        # 日线K线
        self.k_line_d = k_line.k_line(data_d, self.label_x, self.label_y)
        self.exrwidget_d = self.k_line_d.draw_chart()

        self.Layout_d.itemAt(0).widget().deleteLater()
        self.Layout_d.addWidget(self.exrwidget_d)

        # 日线成交
        if len(data_d):
            max = data_d['v'].max()
            i = 0
            pow = 1
            while max > 9999:
                max = max / 10
                i += 1
                pow *= 10
            if i > 0:
                self.label_d_v.setText('成交量(*10^{:})'.format(i))
            else:
                self.label_d_v.setText('成交量')
            data_d['v'] = data_d['v'].map(lambda x: x / pow)

        self.volume_d = k_line.v_bar(data_d)
        self.exrwidget_d_v = self.volume_d.draw_chart()

        self.Layout_d_v.itemAt(0).widget().deleteLater()
        self.Layout_d_v.addWidget(self.exrwidget_d_v)

        # 日线MACD
        self.MACD_d = k_line.MACD(data_d)
        self.exrwidget_d_MACD = self.MACD_d.draw_chart()

        self.Layout_d_MACD.itemAt(0).widget().deleteLater()
        self.Layout_d_MACD.addWidget(self.exrwidget_d_MACD)

        # 周线标签
        if not len(data_w):
            self.label_w_ma5.setText('MA5:')
            self.label_w_ma10.setText('MA10:')
            self.label_w_ma20.setText('MA20:')
            self.label_w_diff.setText('DIF:')
            self.label_w_dea.setText('DEA:')
            self.label_w_macd.setText('MACD:')
        else:
            self.label_w_ma5.setText('MA5:' + str(round(data_w['ma5'][-1], 4)))
            self.label_w_ma10.setText('MA10:' + str(round(data_w['ma10'][-1], 4)))
            self.label_w_ma20.setText('MA20:' + str(round(data_w['ma20'][-1], 4)))
            self.label_w_diff.setText('DIF:' + str(round(data_w['diff'][-1], 4)))
            self.label_w_dea.setText('DEA:' + str(round(data_w['dea'][-1], 4)))
            self.label_w_macd.setText('MACD:' + str(round(data_w['macd'][-1], 4)))

        # 周线K线
        self.k_line_w = k_line.k_line(data_w, self.label_x, self.label_y)
        self.exrwidget_w = self.k_line_w.draw_chart()

        self.Layout_w.itemAt(0).widget().deleteLater()
        self.Layout_w.addWidget(self.exrwidget_w)

        # 周线成交
        if len(data_w):
            max = data_w['v'].max()
            i = 0
            pow = 1
            while max > 9999:
                max = max / 10
                i += 1
                pow *= 10
            if i > 0:
                self.label_w_v.setText('成交量(*10^{:})'.format(i))
            else:
                self.label_w_v.setText('成交量')
            data_w['v'] = data_w['v'].map(lambda x: x / pow)

        self.volume_w = k_line.v_bar(data_w)
        self.exrwidget_w_v = self.volume_w.draw_chart()

        self.Layout_w_v.itemAt(0).widget().deleteLater()
        self.Layout_w_v.addWidget(self.exrwidget_w_v)

        # 周线MACD
        self.MACD_w = k_line.MACD(data_w)
        self.exrwidget_w_MACD = self.MACD_w.draw_chart()

        self.Layout_w_MACD.itemAt(0).widget().deleteLater()
        self.Layout_w_MACD.addWidget(self.exrwidget_w_MACD)

        # 月线标签
        if not len(data_m):
            self.label_m_ma5.setText('MA5:')
            self.label_m_ma10.setText('MA10:')
            self.label_m_ma20.setText('MA20:')
            self.label_m_diff.setText('DIF:')
            self.label_m_dea.setText('DEA:')
            self.label_m_macd.setText('MACD:')
        else:
            self.label_m_ma5.setText('MA5:' + str(round(data_m['ma5'][-1], 4)))
            self.label_m_ma10.setText('MA10:' + str(round(data_m['ma10'][-1], 4)))
            self.label_m_ma20.setText('MA20:' + str(round(data_m['ma20'][-1], 4)))
            self.label_m_diff.setText('DIF:' + str(round(data_m['diff'][-1], 4)))
            self.label_m_dea.setText('DEA:' + str(round(data_m['dea'][-1], 4)))
            self.label_m_macd.setText('MACD:' + str(round(data_m['macd'][-1], 4)))

        # 月线K线
        if len(data_m):
            max = data_m['v'].max()
            i = 0
            pow = 1
            while max > 9999:
                max = max / 10
                i += 1
                pow *= 10
            if i > 0:
                self.label_m_v.setText('成交量(*10^{:})'.format(i))
            else:
                self.label_m_v.setText('成交量')
            data_m['v'] = data_m['v'].map(lambda x: x / pow)

        self.k_line_m = k_line.k_line(data_m, self.label_x, self.label_y)
        self.exrwidget_m = self.k_line_m.draw_chart()

        self.Layout_m.itemAt(0).widget().deleteLater()
        self.Layout_m.addWidget(self.exrwidget_m)

        # 月线成交
        self.volume_m = k_line.v_bar(data_m)
        self.exrwidget_m_v = self.volume_m.draw_chart()

        self.Layout_m_v.itemAt(0).widget().deleteLater()
        self.Layout_m_v.addWidget(self.exrwidget_m_v)

        # 月线MACD
        self.MACD_m = k_line.MACD(data_m)
        self.exrwidget_m_MACD = self.MACD_m.draw_chart()

        self.Layout_m_MACD.itemAt(0).widget().deleteLater()
        self.Layout_m_MACD.addWidget(self.exrwidget_m_MACD)

    '''
    价值潜力榜
    '''

    # 加载tableWidget_rank
    def load_tableWidget_rank(self):
        # 未选中'价值潜力榜'标签 / 表格中已经存在数据: 不再加载
        if self.tabWidget_1.currentIndex() != 3 or self.tableWidget_rank.rowCount():
            return
        self.update_tableWidget_rank()

    # 更新tableWidget_rank
    def update_tableWidget_rank(self):
        data = solution.get_tableWidget_rank(self.spinBox_rank_buy.value(), self.spinBox_rank_sell.value(), self.spinBox_rank_v.value(),
                                             self.radioButton_buy.isChecked(), self.horizontalSlider_rank.value())
        self.tableWidget_rank.setRowCount(len(data))
        for i in range(len(data)):
            for j in range(17):
                if j == 3:  # 涨幅, 保留两位小数
                    t = float(data[i][3])
                    self.tableWidget_rank.setItem(i, 3, QtWidgets.QTableWidgetItem(format(t, '.2f') + '%'))
                    if t > 0:
                        self.tableWidget_rank.item(i, 3).setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
                    elif t < 0:
                        self.tableWidget_rank.item(i, 3).setForeground(QtGui.QBrush(QtGui.QColor(0, 255, 0)))
                else:
                    self.tableWidget_rank.setItem(i, j, QtWidgets.QTableWidgetItem(data[i][j]))

                # 居中
                self.tableWidget_rank.item(i, j).setTextAlignment(QtCore.Qt.AlignCenter)

    # 展示tableWidget_rank菜单
    def show_tableWidget_rank_menu(self, pos):
        # 未选中表格中的一行 / 选中多行
        if not self.tableWidget_rank.selectionModel().selection().indexes() or \
                self.tableWidget_rank.selectionModel().selection().indexes()[-1].row() - \
                self.tableWidget_rank.selectionModel().selection().indexes()[0].row():
            menu_r = QtWidgets.QMenu()
            item_r = menu_r.addAction('刷新')

            action = menu_r.exec_(self.tableWidget_rank.mapToGlobal(pos))

            if action == item_r:
                self.update_tableWidget_rank()
            return

        menu = QtWidgets.QMenu()
        item1 = menu.addAction('刷新')
        item2 = menu.addAction('分析合约')

        action = menu.exec_(self.tableWidget_rank.mapToGlobal(pos))
        idx = self.tableWidget_rank.selectionModel().selection().indexes()[0].row()

        if action == item1:  # 刷新
            self.update_tableWidget_rank()
        elif action == item2:  # 分析合约
            self.lineEdit_code.setText(self.tableWidget_rank.item(idx, 0).text())
            self.update_tab_3()

            self.tabWidget_1.setCurrentIndex(2)
            self.tabWidget_4.setCurrentIndex(0)
        else:  # 未选择菜单选项
            return

    '''
    通用函数
    '''

    # 窗口大小改变
    def resize(self, w, h):
        self.tabWidget_1.setGeometry(QtCore.QRect(0, 0, w, h))

        # 股票期权
        self.tabWidget_2.setGeometry(QtCore.QRect(0, 0, w - 31, h - 8))

        # 股票期权 -> 分类报价
        self.tableWidget_1.setGeometry(QtCore.QRect(30, 60, w - 100, h - 120))
        width_add = [8, 99, -3, -3, -3, -3, -23, -23, -23, -23, 17, -3, -8, -8, -8, -8, -3]
        for i in range(0, 17):
            self.tableWidget_1.setColumnWidth(i, int(self.tableWidget_1.width() / 17) + width_add[i])

        # 股票期权 -> T型报价
        self.label_c1.setGeometry(QtCore.QRect(30, 70, w / 2 - 70, 20))
        self.label_p1.setGeometry(QtCore.QRect(w / 2 - 40, 70, w / 2 - 70, 20))
        self.tableWidget_2.setGeometry(QtCore.QRect(30, 90, w - 100, h - 150))
        for i in range(17):
            self.tableWidget_2.setColumnWidth(i, int(self.tableWidget_2.width() / 17) - 1)

        # 商品期权
        self.tabWidget_3.setGeometry(QtCore.QRect(0, 0, w - 31, h - 8))

        # 商品期权 -> T型报价
        self.label_c2.setGeometry(QtCore.QRect(30, 70, w / 2 - 70, 20))
        self.label_p2.setGeometry(QtCore.QRect(w / 2 - 40, 70, w / 2 - 70, 20))
        self.tableWidget_3.setGeometry(QtCore.QRect(30, 90, w - 100, h - 150))
        for i in range(15):
            self.tableWidget_3.setColumnWidth(i, int(self.tableWidget_3.width() / 15) - 1)

        # 合约分析
        self.tabWidget_4.setGeometry(QtCore.QRect(0, 70, w - 31, h - 78))

        # 合约分析 -> 合约详情
        self.label_d1.setGeometry(QtCore.QRect(50, 30, w - 150, 30))
        self.textBrowser_1.setGeometry(QtCore.QRect(50, 60, w - 150, int(h / 7) + 70))
        self.label_d2.setGeometry(QtCore.QRect(50, int(2 * h / 7) + 80, w - 150, 30))
        self.textBrowser_2.setGeometry(QtCore.QRect(50, int(2 * h / 7) + 110, w - 150, int(h / 7) + 20))
        self.label_d3.setGeometry(QtCore.QRect(50, int(4 * h / 7) + 80, w - 150, 30))
        self.textBrowser_3.setGeometry(QtCore.QRect(50, int(4 * h / 7) + 110, w - 150, int(h / 7) - 30))

        # 合约分析 -> K线数据
        self.tabWidget_5.setGeometry(QtCore.QRect(0, 0, w - 39, h - 109))

        self.label_hour_x.setGeometry(QtCore.QRect(0, h - 321, 85, 16))
        self.label_hour_y.setGeometry(QtCore.QRect(5, 0, 38, 15))
        self.label_x.setGeometry(QtCore.QRect(0, h - 401, 85, 16))
        self.label_y.setGeometry(QtCore.QRect(5, 0, 38, 15))

        self.label_hour_v.setGeometry(QtCore.QRect(0, h - 330, 200, 20))
        self.label_d_v.setGeometry(QtCore.QRect(0, h - 410, 200, 20))
        self.label_d_MACD.setGeometry(QtCore.QRect(0, h - 280, 150, 20))
        self.label_d_diff.setGeometry(QtCore.QRect(150, h - 280, 100, 20))
        self.label_d_dea.setGeometry(QtCore.QRect(250, h - 280, 100, 20))
        self.label_d_macd.setGeometry(QtCore.QRect(350, h - 280, 100, 20))
        self.label_w_v.setGeometry(QtCore.QRect(0, h - 410, 200, 20))
        self.label_w_MACD.setGeometry(QtCore.QRect(0, h - 280, 150, 20))
        self.label_w_diff.setGeometry(QtCore.QRect(150, h - 280, 100, 20))
        self.label_w_dea.setGeometry(QtCore.QRect(250, h - 280, 100, 20))
        self.label_w_macd.setGeometry(QtCore.QRect(350, h - 280, 100, 20))
        self.label_m_v.setGeometry(QtCore.QRect(0, h - 410, 200, 20))
        self.label_m_MACD.setGeometry(QtCore.QRect(0, h - 280, 150, 20))
        self.label_m_diff.setGeometry(QtCore.QRect(150, h - 280, 100, 20))
        self.label_m_dea.setGeometry(QtCore.QRect(250, h - 280, 100, 20))
        self.label_m_macd.setGeometry(QtCore.QRect(350, h - 280, 100, 20))

        self.LayoutWidget_hour.setGeometry(QtCore.QRect(0, 20, w - 47, h - 350))
        self.LayoutWidget_hour_v.setGeometry(QtCore.QRect(0, h - 310, w - 47, 170))
        self.LayoutWidget_d.setGeometry(QtCore.QRect(0, 20, w - 47, h - 430))
        self.LayoutWidget_d_v.setGeometry(QtCore.QRect(0, h - 390, w - 47, 110))
        self.LayoutWidget_d_MACD.setGeometry(QtCore.QRect(0, h - 260, w - 47, 120))
        self.LayoutWidget_w.setGeometry(QtCore.QRect(0, 20, w - 47, h - 430))
        self.LayoutWidget_w_v.setGeometry(QtCore.QRect(0, h - 390, w - 47, 110))
        self.LayoutWidget_w_MACD.setGeometry(QtCore.QRect(0, h - 260, w - 47, 120))
        self.LayoutWidget_m.setGeometry(QtCore.QRect(0, 20, w - 47, h - 430))
        self.LayoutWidget_m_v.setGeometry(QtCore.QRect(0, h - 390, w - 47, 110))
        self.LayoutWidget_m_MACD.setGeometry(QtCore.QRect(0, h - 260, w - 47, 120))

        # 价值潜力榜
        self.tableWidget_rank.setGeometry(QtCore.QRect(30, 70, w - 100, h - 100))
        width_add = [8, 99, -3, -3, -3, -3, -3, -23, -23, -13, -13, -3, -8, -8, -8, -8, -3]
        for i in range(0, 17):
            self.tableWidget_rank.setColumnWidth(i, int(self.tableWidget_rank.width() / 17) + width_add[i])