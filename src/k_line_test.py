import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui
from PyQt5.QtWidgets import QApplication


## Create a subclass of GraphicsObject.
## The only required methods are paint() and boundingRect()
## (see QGraphicsItem documentation)


class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  ## data must have fields: time, open, close, min, max
        self.bar_width = (self.data[1][0] - self.data[0][0]) * 2. / 3.  # K线的宽是间距的2/3
        self.generatePicture()

    def generatePicture(self):
        ## pre-computing a QPicture object allows paint() to run much more quickly,
        ## rather than re-drawing the shapes every time.
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        w = self.bar_width / 2
        for (t, open, close, min, max) in self.data:
            p.drawLine(QtCore.QPointF(t, min), QtCore.QPointF(t, max))
            if open > close:
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setBrush(pg.mkBrush('g'))
            p.drawRect(QtCore.QRectF(t - w, open, w * 2, close - open))
        p.end()

    def paint(self, p, *args):

        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QtCore.QRectF(self.picture.boundingRect())


if __name__ == '__main__':

    # 定义鼠标移动事件响应函数
    def mouseMoved(evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        w = bar.bar_width / 2
        if p1.sceneBoundingRect().contains(pos):
            mousePoint = vb.mapSceneToView(pos)
            index = int(mousePoint.x() - w)
            if mousePoint.x() > (index - w) and index < len(data):
                bar_data = data[index]
                label.setText("X: %.1f \t id=%d \
                    <span style='color: red'>\
                    open=%.1f \t high=%.1f \t low=%.1f \t close=%.1f\
                        </span>"
                              % (mousePoint.x(), bar_data[0], bar_data[1], bar_data[2], bar_data[3], bar_data[4]))


    data = [  ## fields are (time, open, close, min, max).
        (1, 10, 13, 5, 15),
        (2, 13, 17, 9, 20),
        (3, 17, 14, 11, 23),
        (4, 14, 15, 5, 19),
        (5, 15, 9, 8, 22),
        (6, 9, 15, 8, 16),
    ]
    app = QApplication([])
    bar = CandlestickItem(data)

    w = pg.GraphicsLayoutWidget(show=True)

    # 添加图顶部左侧的标签，显示开盘价等
    label = w.addLabel('', row=0, col=0, justify='left')

    p1 = w.addPlot(row=1, col=0)
    p1.addItem(bar)

    w.setWindowTitle('K线示意图')
    vb = p1.vb
    proxy = pg.SignalProxy(vb.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)

    w.show()
    app.exec()