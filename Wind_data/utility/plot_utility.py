import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from folder_utility import create_folder
import font_utility

plt.rcParams['font.sans-serif'] = [font_utility.select_chinese_font_by_os()]
plt.rcParams['axes.unicode_minus'] = False


def plot_2_series_in_one_figure(x1, y1, x2, y2, title, y1_label, y2_label, sub_folder_name, x_label='日期'):
    fig = plt.figure()

    # add_subplot(1, 1, 1) 意思：建立划分1行1列的子图，取第1幅子图
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.grid(ls='--', axis='both', which='both')

    ax1.plot(x1, y1, marker="o")
    ax1.set_ylabel(y1_label)
    ax1.set_title(title)
    ax1.set_xlabel(x_label)
    ax1.set_ylim([0, y1.max() * 1.1])

    ax2 = ax1.twinx()  # 两组数列画在同一张图的关键
    ax2.plot(x2, y2, 'r')
    ax2.set_ylabel(y2_label)
    ax2.set_ylim([0, y2.max() * 1.1])

    fig.autofmt_xdate()

    # 存储在启动文件所在路径，例如 application 为启动路径
    path = './pictures/' + sub_folder_name
    create_folder(path)
    plt.savefig(path + '/' + title + '.png')
    plt.close()


def plot_2_data_frame_in_one_figure(s_l, s_r, title, sub_folder_name,
                                    y_label_l, y_label_r, x_label='日期'):
    # 绘图
    ax = s_l.plot(title=title)
    s_r.plot(ax=ax, secondary_y=True)
    ax.set_ylim([0, s_l.max() * 1.1])
    ax.right_ax.set_ylim([0, s_r.max() * 1.1])
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label_l)
    ax.right_ax.set_ylabel(y_label_r)
    # 修改刻度定位器
    rule = mdates.rrulewrapper(mdates.MONTHLY, byeaster=1, interval=3)
    season = mdates.RRuleLocator(rule)
    # months = mdates.MonthLocator()  # every month
    years = mdates.YearLocator()  # every year
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_minor_locator(season)
    ax.grid(color='red', ls='-.')
    ax.grid(which='minor', color='orangered', linewidth=0.25, ls='-.')
    ax.figure.autofmt_xdate()

    # 存储在启动文件所在路径，例如 application 为启动路径
    plt.show()
    # path = './pictures/' + sub_folder_name
    # create_folder(path)
    # plt.savefig(path + '/' + title + '.png')
    plt.close()


print('end')
