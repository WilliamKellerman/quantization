import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
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


def plot_2_series_in_one_figure(s_l, s_r, title, sub_folder_name,
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
    year_locator = mdates.YearLocator(month=12, day=31)  # 每年最后一天
    season_locator = mdates.MonthLocator(bymonth=[3, 6, 9, 12], bymonthday=-1)  # 每季度最后一天
    ax.xaxis.set_major_locator(year_locator)
    ax.xaxis.set_minor_locator(season_locator)
    ax.grid(which='major', color='red', ls='-.')
    ax.grid(which='minor', color='orangered', linewidth=0.25, ls='-.')
    ax.figure.autofmt_xdate()

    # 存储在启动文件所在路径，例如 application 为启动路径
    # plt.show()
    path = './pictures/' + sub_folder_name
    create_folder(path)
    plt.savefig(path + '/' + title + '.png')
    plt.close()


# 绘制3个series在上下两幅图，上图2个series，下图1个
def plot_3_series_in_one_figure(s_l, s_r, s_low,
                                title, sub_folder_name,
                                y_label_l, y_label_r, y_label_low, x_label='日期'):
    # 创建绘图对象和2个坐标轴
    fig = plt.figure(figsize=(12, 6))
    left, width = 0.1, 0.8
    ax = fig.add_axes([left, 0.4, width, 0.5])  # left, bottom, width, height
    ax_low = fig.add_axes([left, 0.2, width, 0.2], sharex=ax)  # 共享ax1轴
    # fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True)
    # ax = axes[0]
    # ax_low = axes[1]
    plt.setp(ax.get_xticklabels(), visible=False)  # 使x轴刻度文本不可见，因为共享，不需要显示

    # 绘图
    s_l.plot(ax=ax, kind='line', title=title)
    s_r.plot(ax=ax, kind='line', secondary_y=True)
    s_low.plot(ax=ax_low, kind='line')
    ax_low.fill_between(x=s_low.index, y1=s_low.values, y2=0)

    # 坐标轴极限与标签
    ax.set_ylim([0, s_l.max() * 1.1])
    ax.right_ax.set_ylim([0, s_r.max() * 1.1])
    ax.set_ylabel(y_label_l)
    ax.right_ax.set_ylabel(y_label_r)
    ax_low.set_ylim([0, s_low.max() * 1.1])
    ax_low.yaxis.tick_right()
    ax_low.yaxis.set_label_position('right')
    ax_low.set_ylabel(y_label_low)
    ax_low.set_xlabel(xlabel=x_label)

    # 坐标轴主辅刻度
    year_locator = mdates.YearLocator(month=12, day=31)  # 每年最后一天
    season_locator = mdates.MonthLocator(bymonth=[3, 6, 9, 12], bymonthday=-1)  # 每季度最后一天
    ax.xaxis.set_major_locator(year_locator)
    ax.xaxis.set_minor_locator(season_locator)
    ax.grid(which='major', color='red', ls='-.')
    ax.grid(which='minor', color='orangered', linewidth=0.25, ls='-.')

    ax_low.xaxis.set_major_locator(year_locator)
    ax_low.xaxis.set_minor_locator(season_locator)
    ax_low.grid(which='major', color='red', ls='-.')
    ax_low.grid(which='minor', color='orangered', linewidth=0.25, ls='-.')
    # ax_low.figure.autofmt_xdate()
    for label in ax_low.get_xticklabels(which='major'):
        label.set_rotation(30)
    # 存储在启动文件所在路径，例如 application 为启动路径
    # plt.show()
    path = './pictures/' + sub_folder_name
    create_folder(path)
    plt.savefig(path + '/' + title + '.png')
    plt.close()


def plot_kline_with_hold(s_hold, df_price, title, y_label, y_label_lower):
    color = mpf.make_marketcolors(up='red', down='green', edge='inherit', wick='inherit', volume='inherit')
    style = mpf.make_mpf_style(marketcolors=color, gridaxis='both', gridstyle='-.', y_on_right=True,
                               rc={'font.family': [font_utility.select_chinese_font_by_os()]})

    # 绘图
    add_plot = mpf.make_addplot(s_hold, type='line', secondary_y='auto', ylabel='持仓')
    mpf.plot(df_price, type='candle', volume=True, style=style, title=title, addplot=add_plot,
             ylabel=y_label, ylabel_lower=y_label_lower,
             xrotation=30,
             datetime_format='%Y-%m-%d',
             )

    print('end')


print('end')
