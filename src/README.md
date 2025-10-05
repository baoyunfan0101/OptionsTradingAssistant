# 期权交易助手

## 项目说明
软件名称：期权交易助手  
理论依据：B-S期权定价模型和基于B-S期权定价模型的权证交易模型  
作者：包云帆

## 文件列表
main.py：main模块  
widget.py：widget模块  
k_line.py：k_line模块  
solution.py：solution模块  
LSTM.py：LSTM模块  
crawler.py：crawler模块  
logo.ico：软件图标  
（详见毕业论文“4.3 模块设计”部分）

## 使用说明
### 开发环境使用
软件的开发环境为Python3.8以及tensorflow2.8.0，其余主要调用的库包括PyQt5、pyqtgraph、requests、sklearn等。

根据实际的硬件条件请选择合适的版本。

环境配置完成后，请先执行LSTM.py，训练软件运行所需的模型。

执行main.py，启动软件。

### 运行环境使用
首先配置上述的软件开发环境。

环境配置完成后，请先执行LSTM.py，训练软件运行所需的模型。

安装并使用pyinstaller打包main.py，并将训练完成的模型文件移动至打包的同一目录。

执行打包目录下的exe文件，启动软件。

应用程序的运行环境为Windows XP及更高版本操作系统，推荐分辨率在1600×900以上。

### 软件的详细使用说明
（详见毕业论文“4.4 使用说明”部分）