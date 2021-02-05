import matplotlib.pyplot as plt
import numpy as np

date1 = np.arange(start=0.01, stop=np.e, step=0.01)
date2 = np.arange(start=0.01, stop=np.e, step=0.5)
price = np.exp(date1)
vol = np.log(date2)


def plot_2_series_in_same_figure(x1, y1, x2, y2):
    fig = plt.figure()

    # add_subplot(1, 1, 1) 意思：建立划分1行1列的子图，取第1幅子图
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(x1, y1)
    ax1.set_ylabel('Y values for exp(-x)')
    ax1.set_title("Double Y axis")
    ax1.set_xlabel('Same X for both exp(-x) and ln(x)...1')

    ax2 = ax1.twinx()  # 两组数列画在同一张图的关键
    ax2.plot(x2, y2, 'r')
    ax2.set_xlim([0, np.e])
    ax2.set_ylabel('Y values for ln(x)')
    ax2.set_xlabel('Same X for both exp(-x) and ln(x)...2')  # 实测发现本行不起作用

    plt.show()
    plt.savefig('./this_is_a_plot.png')


def point_df_test():
    plt.figure()
    ax = plt.gca()
    # 修改刻度定位器
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(0.1))
    ax.yaxis.set_major_locator(plt.MultipleLocator(250))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(50))

    ax.grid(which='major', axis='both',
            color='orangered', linewidth=0.75)
    ax.grid(which='minor', axis='both',
            color='orangered', linewidth=0.25)

    # 绘制曲线
    y = [1, 10, 100, 1000, 100, 10, 1]
    plt.plot(y, 'o-', color='dodgerblue')
    plt.show()

    print('end')


# plot_2_series_in_same_figure(x1=date1, y1=price, x2=date2, y2=vol)
point_df_test()

print('end')
