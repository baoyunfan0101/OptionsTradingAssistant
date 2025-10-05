import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(6, 3), dpi=200)
plt.xlabel('标的物价格x')
plt.ylabel('盈亏')
x = ['权利金C', 2, 3, 4, 5, 6]
y = [-1, -1, -1, 0, 1, 2]
plt.plot(x, y)
plt.axhline(0, color='0', linestyle='--')
plt.gcf().subplots_adjust(bottom=0.2)
plt.annotate('执行价格k', xy=(2, 0),
             xycoords='data', xytext=(-70, +20),
             textcoords='offset points',
             arrowprops=dict(facecolor='black'))
plt.annotate('盈亏平衡点(k+C)', xy=(3, 0),
             xycoords='data', xytext=(-90, +50),
             textcoords='offset points',
             arrowprops=dict(facecolor='black'))
plt.show()

plt.figure(figsize=(6, 3), dpi=200)
plt.xlabel('标的物价格x')
plt.ylabel('盈亏')
x = ['权利金P', 2, 3, 4, 5, 6]
y = [2, 1, 0, -1, -1, -1]
plt.plot(x, y)
plt.axhline(0, color='0', linestyle='--')
plt.gcf().subplots_adjust(bottom=0.2)
plt.annotate('执行价格k', xy=(3, 0),
             xycoords='data', xytext=(-20, +30),
             textcoords='offset points',
             arrowprops=dict(facecolor='black'))
plt.annotate('盈亏平衡点(k-P)', xy=(2, 0),
             xycoords='data', xytext=(-20, +50),
             textcoords='offset points',
             arrowprops=dict(facecolor='black'))
plt.show()