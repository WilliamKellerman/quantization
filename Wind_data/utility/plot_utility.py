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
