from PyQt5 import QtCore, QtGui
import pyqtgraph as pg


# K线图
class k_line():
    def __init__(self, data=None, label_x=None, label_y=None):
        # data索引: d-日期(datetime类型)
        # date字段: o-开盘价, h-最高价, l-最低价, c-收盘价, v-成交量, ma5/10/20-5/10/20收盘价日均线
        self.data = data
        self.len = len(data)

        if not self.len:
            return

        self.y_min = self.data['l'].min()
        self.y_max = self.data['h'].max()

        self.label_x = label_x
        self.label_y = label_y

    def draw_chart(self):
        if not self.len:
            res = pg.PlotWidget()

            res.hideButtons()  # 隐藏左下角的A
            res.setMouseEnabled(x=False, y=False)  # 禁止轴向操作
            res.showGrid(x=False, y=False)  # 不显示网格

            res.getAxis('left').setTextPen(QtGui.QColor(115, 125, 135))
            res.getAxis('left').setPen(QtGui.QColor(115, 125, 135))
            res.getAxis('bottom').setTextPen(QtGui.QColor(115, 125, 135))
            res.getAxis('bottom').setPen(QtGui.QColor(115, 125, 135))
            return res

        # x轴索引
        if self.len > 2:
            self.xdict = {0: str(self.data.index[0])[0:10:],
                          int((self.len + 1) / 2): str(self.data.index[int((self.len + 1) / 2)])[0:10:],
                          self.len - 1: str(self.data.index[-1])[0:10:]}
        else:
            self.xdict = {0: str(self.data.index[0])[0:10:]}

        self.stringaxis = pg.AxisItem(orientation='bottom')
        self.stringaxis.setTicks([self.xdict.items()])

        # 创建plt
        self.plt = pg.PlotWidget(axisItems={'bottom': self.stringaxis}, enableMenu=False)

        # 修改plt属性
        self.plt.hideButtons()  # 隐藏左下角的A
        self.plt.setMouseEnabled(x=False, y=False)  # 禁止轴向操作
        self.plt.showGrid(x=False, y=False)  # 不显示网格

        self.plt.getAxis('left').setTextPen(QtGui.QColor(115, 125, 135))
        self.plt.getAxis('left').setPen(QtGui.QColor(115, 125, 135))
        self.plt.getAxis('bottom').setTextPen(QtGui.QColor(115, 125, 135))
        self.plt.getAxis('bottom').setPen(QtGui.QColor(115, 125, 135))

        if self.len < 30:
            x_max = 29
        else:
            x_max = self.len - 1
        self.plt.setXRange(0, x_max)
        self.plt.setYRange(self.y_min, self.y_max)

        # 绘制k线图
        self.item = candle_stick(self.data)
        self.plt.addItem(self.item)

        # 绘制十字光标
        pen = pg.mkPen(QtGui.QColor(255, 255, 255), width=0.5, style=QtCore.Qt.SolidLine)
        self.vline = pg.InfiniteLine(angle=90, movable=False, pen=pen)  # 垂直线
        self.hline = pg.InfiniteLine(angle=0, movable=False, pen=pen)  # 水平线
        self.vline.setPos(-128)
        self.hline.setPos(-8)
        self.plt.addItem(self.vline, ignoreBounds=True)
        self.plt.addItem(self.hline, ignoreBounds=True)

        # 鼠标位置变化
        self.plt.scene().sigMouseMoved.connect(self.plot_cursor)
        self.plt.leaveEvent = self.leaveEvent

        return self.plt

    def plot_cursor(self, pos):
        if isinstance(pos, tuple):
            pos = pos[0]
        if self.plt.sceneBoundingRect().contains(pos):
            mouse_point = self.plt.plotItem.vb.mapSceneToView(pos)  # 转换坐标系

            # 绘制十字光标
            self.vline.setPos(mouse_point.x())
            self.hline.setPos(mouse_point.y())

            if -1 < int(mouse_point.x() + 0.5) < self.len and self.y_min < mouse_point.y() < self.y_max:
                self.label_x.setText(str(self.data.index[int(mouse_point.x() + 0.5)])[0:10:])
                self.label_x.move(5 + pos.x() - self.label_x.geometry().width() / 2,
                                  self.label_x.geometry().y())

                self.label_y.setText(str(round(mouse_point.y(), 2)))
                self.label_y.move(self.label_y.geometry().x(),
                                  47 + pos.y() - self.label_y.geometry().height() / 2)
                if self.label_x.isHidden():
                    self.label_x.show()
                if self.label_y.isHidden():
                    self.label_y.show()
            else:
                self.label_x.hide()
                self.label_y.hide()

    def leaveEvent(self, a0):
        self.vline.setPos(-128)
        self.hline.setPos(-8)
        self.label_x.hide()
        self.label_y.hide()


# 绘制K线图
class candle_stick(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data
        self.generatePicture()

    # 绘制k线图
    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)

        # 蜡烛宽度: 2w
        w = 0.25

        # 记录均线的上一个值
        pre_ma5 = 0
        pre_ma10 = 0
        pre_ma20 = 0

        i = 0
        for date, row in self.data.iterrows():
            o, h, l, c, ma5, ma10, ma20 = row['o'], row['h'], row['l'], row['c'], row['ma5'], row['ma10'], row['ma20']

            # 绘制蜡烛: 开盘价>收盘价-绿色实心, 开盘价<收盘价-红色空心
            if o > c:
                p.setPen(pg.mkPen(QtGui.QColor(84, 255, 255)))
                p.setBrush(pg.mkBrush(QtGui.QColor(84, 255, 255)))
                p.drawLine(QtCore.QPointF(i, l), QtCore.QPointF(i, h))
                p.drawRect(QtCore.QRectF(i - w, o, w * 2, c - o))
            else:
                p.setPen(pg.mkPen(QtGui.QColor(255, 42, 42)))
                p.setBrush(pg.mkBrush(QtGui.QColor(255, 42, 42)))
                if h != c:
                    p.drawLine(QtCore.QPointF(i, h), QtCore.QPointF(i, c))
                if l != o:
                    p.drawLine(QtCore.QPointF(i, o), QtCore.QPointF(i, l))
                if c == o:
                    p.drawLine(QtCore.QPointF(i - w, o), QtCore.QPointF(i + w, o))
                else:
                    p.drawLines(QtCore.QLineF(QtCore.QPointF(i - w, c), QtCore.QPointF(i - w, o)),
                                QtCore.QLineF(QtCore.QPointF(i - w, o), QtCore.QPointF(i + w, o)),
                                QtCore.QLineF(QtCore.QPointF(i + w, o), QtCore.QPointF(i + w, c)),
                                QtCore.QLineF(QtCore.QPointF(i + w, c), QtCore.QPointF(i - w, c)))

            # 连接各均线: 5日-白, 10-黄, 20日-紫
            if pre_ma5 != 0:
                p.setPen(pg.mkPen(QtGui.QColor(255, 255, 255)))
                p.setBrush(pg.mkBrush(QtGui.QColor(255, 255, 255)))
                p.drawLine(QtCore.QPointF(i - 1, pre_ma5), QtCore.QPointF(i, ma5))
            pre_ma5 = ma5
            if pre_ma10 != 0:
                p.setPen(pg.mkPen(QtGui.QColor(255, 255, 0)))
                p.setBrush(pg.mkBrush(QtGui.QColor(255, 255, 0)))
                p.drawLine(QtCore.QPointF(i - 1, pre_ma10), QtCore.QPointF(i, ma10))
            pre_ma10 = ma10
            if pre_ma20 != 0:
                p.setPen(pg.mkPen(QtGui.QColor(255, 0, 255)))
                p.setBrush(pg.mkBrush(QtGui.QColor(255, 0, 255)))
                p.drawLine(QtCore.QPointF(i - 1, pre_ma20), QtCore.QPointF(i, ma20))
            pre_ma20 = ma20

            i += 1

        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())


# 成交量柱状图
class v_bar():
    def __init__(self, data=None):
        # data索引: d-日期(datetime类型)
        # date字段: o-开盘价, h-最高价, l-最低价, c-收盘价, v-成交量, ma5/10/20-5/10/20收盘价日均线
        self.data = data
        self.len = len(data)

    def draw_chart(self):
        if not self.len:
            res = pg.PlotWidget()

            res.hideButtons()  # 隐藏左下角的A
            res.setMouseEnabled(x=False, y=False)  # 禁止轴向操作
            res.showGrid(x=False, y=False)  # 不显示网格

            res.getAxis('left').setTextPen(QtGui.QColor(115, 125, 135))
            res.getAxis('left').setPen(QtGui.QColor(115, 125, 135))
            res.getAxis('bottom').setTextPen(QtGui.QColor(115, 125, 135))
            res.getAxis('bottom').setPen(QtGui.QColor(115, 125, 135))
            return res

        # x轴索引
        self.stringaxis = pg.AxisItem(orientation='bottom')
        self.stringaxis.setTicks([{}.items()])

        # 创建plt
        self.plt = pg.PlotWidget(axisItems={'bottom': self.stringaxis}, enableMenu=False)

        # 修改plt属性
        self.plt.hideButtons()  # 隐藏左下角的A
        self.plt.setMouseEnabled(x=False, y=False)  # 禁止轴向操作
        self.plt.showGrid(x=False, y=False)  # 不显示网格

        self.plt.getAxis('left').setTextPen(QtGui.QColor(115, 125, 135))
        self.plt.getAxis('left').setPen(QtGui.QColor(115, 125, 135))
        self.plt.getAxis('bottom').setTextPen(QtGui.QColor(115, 125, 135))
        self.plt.getAxis('bottom').setPen(QtGui.QColor(115, 125, 135))

        if self.len < 30:
            x_max = 29
        else:
            x_max = self.len - 1
        self.plt.setXRange(0, x_max)
        self.plt.setYRange(0, self.data['v'].max())

        # 绘制柱状图
        self.item = volume(self.data)
        self.plt.addItem(self.item)

        return self.plt


# 绘制成交量柱状图
class volume(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data
        self.generatePicture()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)

        w = 0.25

        i = 0
        for _, row in self.data.iterrows():
            o, c, v = row['o'], row['c'], row['v']
            if o > c:
                p.setPen(pg.mkPen(QtGui.QColor(84, 255, 255)))
                p.setBrush(pg.mkBrush(QtGui.QColor(84, 255, 255)))
                p.drawRect(QtCore.QRectF(i - w, 0, w * 2, v))

            else:
                p.setPen(pg.mkPen(QtGui.QColor(255, 42, 42)))
                p.drawLines(QtCore.QLineF(QtCore.QPointF(i - w, 0), QtCore.QPointF(i - w, v)),
                            QtCore.QLineF(QtCore.QPointF(i - w, v), QtCore.QPointF(i + w, v)),
                            QtCore.QLineF(QtCore.QPointF(i + w, v), QtCore.QPointF(i + w, 0)),
                            QtCore.QLineF(QtCore.QPointF(i + w, 0), QtCore.QPointF(i - w, 0)))

            i += 1

        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())


# 分时线图
class hour_line():
    def __init__(self, data=None, label_x=None, label_y=None):
        # data字段: i-时间，p-价格，v-成交，t-持仓，a-均价, d-日期(仅第一项有)
        self.data = data
        self.len = len(data)

        if not self.len:
            return

        self.y_min = self.data['p'].min()
        self.y_max = self.data['p'].max()

        self.label_x = label_x
        self.label_y = label_y

    def draw_chart(self):
        if not self.len:
            res = pg.PlotWidget()

            res.hideButtons()  # 隐藏左下角的A
            res.setMouseEnabled(x=False, y=False)  # 禁止轴向操作
            res.showGrid(x=False, y=True)  # 不显示网格

            res.getAxis('left').setTextPen(QtGui.QColor(115, 125, 135))
            res.getAxis('left').setPen(QtGui.QColor(115, 125, 135))
            res.getAxis('bottom').setTextPen(QtGui.QColor(115, 125, 135))
            res.getAxis('bottom').setPen(QtGui.QColor(115, 125, 135))
            return res

        # x轴索引
        if self.len > 2:
            self.xdict = {0: str(self.data['d'][0]),
                          int((self.len + 1) / 2): self.data['i'][int((self.len + 1) / 2)][0:5:],
                          self.len - 1: self.data['i'][self.len - 1][0:5:]}
        else:
            self.xdict = {0: str(self.data['d'][0])}

        self.stringaxis = pg.AxisItem(orientation='bottom')
        self.stringaxis.setTicks([self.xdict.items()])

        # 创建plt
        self.plt = pg.PlotWidget(axisItems={'bottom': self.stringaxis}, enableMenu=False)

        # 修改plt属性
        self.plt.hideButtons()  # 隐藏左下角的A
        self.plt.setMouseEnabled(x=False, y=False)  # 禁止轴向操作
        self.plt.showGrid(x=False, y=False)  # 不显示网格

        self.plt.getAxis('left').setTextPen(QtGui.QColor(115, 125, 135))
        self.plt.getAxis('left').setPen(QtGui.QColor(115, 125, 135))
        self.plt.getAxis('bottom').setTextPen(QtGui.QColor(115, 125, 135))
        self.plt.getAxis('bottom').setPen(QtGui.QColor(115, 125, 135))

        self.plt.setXRange(0, self.len - 1)
        self.plt.setYRange(self.y_min, self.y_max)

        # 绘制k线图
        self.item = fold_line(self.data)
        self.plt.addItem(self.item)

        # 绘制十字光标
        pen = pg.mkPen(QtGui.QColor(255, 255, 255), width=0.5, style=QtCore.Qt.SolidLine)
        self.vline = pg.InfiniteLine(angle=90, movable=False, pen=pen)  # 垂直线
        self.hline = pg.InfiniteLine(angle=0, movable=False, pen=pen)  # 水平线
        self.vline.setPos(-128)
        self.hline.setPos(-8)
        self.plt.addItem(self.vline, ignoreBounds=True)
        self.plt.addItem(self.hline, ignoreBounds=True)

        # 鼠标位置变化
        self.plt.scene().sigMouseMoved.connect(self.plot_cursor)
        self.plt.leaveEvent = self.leaveEvent

        return self.plt

    def plot_cursor(self, pos):
        if isinstance(pos, tuple):
            pos = pos[0]
        if self.plt.sceneBoundingRect().contains(pos):
            mouse_point = self.plt.plotItem.vb.mapSceneToView(pos)  # 转换坐标系

            # 绘制十字光标
            self.vline.setPos(mouse_point.x())
            self.hline.setPos(mouse_point.y())

            if -1 < int(mouse_point.x() + 0.5) < self.len and self.y_min < mouse_point.y() < self.y_max:
                self.label_x.setText(str(self.data['i'][int(mouse_point.x() + 0.5)])[0:5:])
                self.label_x.move(5 + pos.x() - self.label_x.geometry().width() / 2,
                                  self.label_x.geometry().y())

                self.label_y.setText(str(round(mouse_point.y(), 2)))
                self.label_y.move(self.label_y.geometry().x(),
                                  47 + pos.y() - self.label_y.geometry().height() / 2)
                if self.label_x.isHidden():
                    self.label_x.show()
                if self.label_y.isHidden():
                    self.label_y.show()
            else:
                self.label_x.hide()
                self.label_y.hide()

    def leaveEvent(self, a0):
        self.vline.setPos(-128)
        self.hline.setPos(-8)
        self.label_x.hide()
        self.label_y.hide()


# 绘制分时线图
class fold_line(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data
        self.generatePicture()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        pen = QtGui.QPainter(self.picture)

        pre_p = 0
        pre_a = 0

        i = 0
        for _, row in self.data.iterrows():
            p, a = row['p'], row['a']

            if pre_p != 0:
                pen.setPen(pg.mkPen(QtGui.QColor(255, 255, 255)))
                pen.setBrush(pg.mkBrush(QtGui.QColor(255, 255, 255)))
                pen.drawLine(QtCore.QPointF(i - 1, pre_p), QtCore.QPointF(i, p))
            pre_p = p
            if pre_a != 0:
                pen.setPen(pg.mkPen(QtGui.QColor(255, 255, 0)))
                pen.setBrush(pg.mkBrush(QtGui.QColor(255, 255, 0)))
                pen.drawLine(QtCore.QPointF(i - 1, pre_a), QtCore.QPointF(i, a))
            pre_a = a

            i += 1

        pen.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())


# 分时线对应的成交量柱状图
class v_bar_hour():
    def __init__(self, data=None):
        # data字段: i-时间，p-价格，v-成交，t-持仓，a-均价, d-日期(仅第一项有)
        self.data = data
        self.len = len(data)

    def draw_chart(self):
        if not self.len:
            res = pg.PlotWidget()

            res.hideButtons()  # 隐藏左下角的A
            res.setMouseEnabled(x=False, y=False)  # 禁止轴向操作
            res.showGrid(x=False, y=False)  # 不显示网格

            res.getAxis('left').setTextPen(QtGui.QColor(115, 125, 135))
            res.getAxis('left').setPen(QtGui.QColor(115, 125, 135))
            res.getAxis('bottom').setTextPen(QtGui.QColor(115, 125, 135))
            res.getAxis('bottom').setPen(QtGui.QColor(115, 125, 135))
            return res

        # x轴索引
        self.stringaxis = pg.AxisItem(orientation='bottom')
        self.stringaxis.setTicks([{}.items()])

        # 创建plt
        self.plt = pg.PlotWidget(axisItems={'bottom': self.stringaxis}, enableMenu=False)

        # 修改plt属性
        self.plt.hideButtons()  # 隐藏左下角的A
        self.plt.setMouseEnabled(x=False, y=False)  # 禁止轴向操作
        self.plt.showGrid(x=False, y=False)  # 不显示网格

        self.plt.getAxis('left').setTextPen(QtGui.QColor(115, 125, 135))
        self.plt.getAxis('left').setPen(QtGui.QColor(115, 125, 135))
        self.plt.getAxis('bottom').setTextPen(QtGui.QColor(115, 125, 135))
        self.plt.getAxis('bottom').setPen(QtGui.QColor(115, 125, 135))

        self.plt.setXRange(0, self.len - 1)
        self.plt.setYRange(0, self.data['v'].max())

        # 绘制柱状图
        self.item = volume_hour(self.data)
        self.plt.addItem(self.item)

        return self.plt


# 绘制分时线对应的成交量柱状图
class volume_hour(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data
        self.generatePicture()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        pen = QtGui.QPainter(self.picture)

        w = 0.25

        pre_p = self.data['a'][0]

        i = 0
        for _, row in self.data.iterrows():
            p, v = row['p'], row['v']
            if p > pre_p:
                pen.setPen(pg.mkPen(QtGui.QColor(255, 42, 42)))
                pen.setBrush(pg.mkBrush(QtGui.QColor(255, 42, 42)))
                pen.drawLine(QtCore.QPointF(i, 0), QtCore.QPointF(i, v))

            elif p < pre_p:
                pen.setPen(pg.mkPen(QtGui.QColor(0, 126, 42)))
                pen.setBrush(pg.mkBrush(QtGui.QColor(0, 126, 42)))
                pen.drawLine(QtCore.QPointF(i, 0), QtCore.QPointF(i, v))

            else:
                pen.setPen(pg.mkPen(QtGui.QColor(255, 255, 255)))
                pen.setBrush(pg.mkBrush(QtGui.QColor(255, 255, 255)))
                pen.drawLine(QtCore.QPointF(i, 0), QtCore.QPointF(i, v))

            i += 1
            pre_p = p

        pen.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())


# MACD
class MACD():
    def __init__(self, data=None):
        # data索引: d-日期(datetime类型)
        # date字段: o-开盘价, h-最高价, l-最低价, c-收盘价, v-成交量, ma5/10/20-5/10/20收盘价日均线, dif/dea/macd
        self.data = data
        self.len = len(data)

    def draw_chart(self):
        if not self.len:
            res = pg.PlotWidget()

            res.hideButtons()  # 隐藏左下角的A
            res.setMouseEnabled(x=False, y=False)  # 禁止轴向操作
            res.showGrid(x=False, y=False)  # 不显示网格

            res.getAxis('left').setTextPen(QtGui.QColor(115, 125, 135))
            res.getAxis('left').setPen(QtGui.QColor(115, 125, 135))
            res.getAxis('bottom').setTextPen(QtGui.QColor(115, 125, 135))
            res.getAxis('bottom').setPen(QtGui.QColor(115, 125, 135))
            return res

        # x轴索引
        self.stringaxis = pg.AxisItem(orientation='bottom')
        self.stringaxis.setTicks([{}.items()])

        # 创建plt
        self.plt = pg.PlotWidget(axisItems={'bottom': self.stringaxis}, enableMenu=False)

        # 修改plt属性
        self.plt.hideButtons()  # 隐藏左下角的A
        self.plt.setMouseEnabled(x=False, y=False)  # 禁止轴向操作
        self.plt.showGrid(x=False, y=False)  # 不显示网格

        self.plt.getAxis('left').setTextPen(QtGui.QColor(115, 125, 135))
        self.plt.getAxis('left').setPen(QtGui.QColor(115, 125, 135))
        self.plt.getAxis('bottom').setTextPen(QtGui.QColor(115, 125, 135))
        self.plt.getAxis('bottom').setPen(QtGui.QColor(115, 125, 135))

        if self.len < 30:
            x_max = 29
        else:
            x_max = self.len - 1
        self.plt.setXRange(0, x_max)
        self.plt.setYRange(self.data['macd'].min(), self.data['macd'].max())

        # 绘制MACD
        self.item = MACD_line(self.data)
        self.plt.addItem(self.item)

        return self.plt


# 绘制MACD
class MACD_line(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data
        self.generatePicture()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)

        pre_diff = 0
        pre_dea = 0

        i = 0
        for _, row in self.data.iterrows():
            diff, dea, macd = row['diff'], row['dea'], row['macd']

            if macd > 0:
                p.setPen(pg.mkPen(QtGui.QColor(255, 42, 42)))
                p.setBrush(pg.mkBrush(QtGui.QColor(255, 42, 42)))
                p.drawLine(QtCore.QPointF(i, 0), QtCore.QPointF(i, macd))
            elif macd < 0:
                p.setPen(pg.mkPen(QtGui.QColor(84, 255, 255)))
                p.setBrush(pg.mkBrush(QtGui.QColor(84, 255, 255)))
                p.drawLine(QtCore.QPointF(i, macd), QtCore.QPointF(i, 0))

            if i > 0:
                p.setPen(pg.mkPen(QtGui.QColor(255, 255, 255)))
                p.setBrush(pg.mkBrush(QtGui.QColor(255, 255, 255)))
                p.drawLine(QtCore.QPointF(i - 1, pre_diff), QtCore.QPointF(i, diff))
                pre_diff = diff

                p.setPen(pg.mkPen(QtGui.QColor(255, 255, 0)))
                p.setBrush(pg.mkBrush(QtGui.QColor(255, 255, 0)))
                p.drawLine(QtCore.QPointF(i - 1, pre_dea), QtCore.QPointF(i, dea))
                pre_dea = dea

            i += 1

        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())
