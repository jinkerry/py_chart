#encoding=utf-8
__author__ = 'jinfeng'

import numpy as np
import matplotlib as mpl
#关闭X-window
mpl.use('Agg')
import matplotlib.pyplot as plt

def process_data():
    #源文件
    source_file = 's3-yixin.csv'
    #当文件行数大于1000行，存放处理后的临时文件
    tmp_file = 'd3.csv'
    #交给numpy处理的数据文件
    dist_file = ''
    #每一张图最多画1000个数据点
    maxPoints = 1000

    count = -1
    for count, line in enumerate(open(source_file, 'rU')):
        pass
    count += 1
    print 'count: ', count

    step = count / maxPoints
    print 'step: ', step

    columns = ['timestamp', 'op_read', 'op_write', 'byte_read', 'byte_write', 'avg_read', 'avg_write',
               'throughout_read', 'throughout_write', 'band_read', 'band_write', 'succ_read', 'succ_write']
    #S=string, i=int, f=float           
    column_types = 'S12, i4, i4, i4, i4, f12, f12, f6, f6, i4, i4, S12, S12'         

    row = 0
    # if point more than lines, choose part of lines, write to dist csv file
    if (count > maxPoints):
        f_src_data = open(source_file, 'r')
        f_dst_data = open(dist_file, 'w')
        while(row <= count):
            line = f_src_data.readline()
            if (step == 0 or row % step == 0):
                f_dst_data.write(line)
            row += 1
        f_src_data.close()
        f_dst_data.close()

        dist_file = tmp_file
    else:
        dist_file = source_file

    #read the data by numpy
    np_data = np.genfromtxt(source_file, dtype=column_types, delimiter=',', 
        skip_header=1, names=columns, invalid_raise=False)

    return np_data

def draw_chart(np_data, title, x_column, y_column, unit=''):

    fig = plt.figure()
    #设置图片尺寸，1600x900
    fig.set_size_inches(16, 9)

    ax1 = fig.add_subplot(111)
    if unit:
        ax1.set_title(title + '(' + unit + ')')
    else:
        ax1.set_title(title)

    ax1.plot(np_data[x_column], c='red', label=title + ' read')

    ax2 = fig.add_subplot(111)
    ax2.plot(np_data[y_column], c='blue', label=title + ' write')

    #get and modify x axis label
    times = process_x_labels(ax1, np_data['timestamp'])

    #modify x axis label
    ax1.set_xticklabels(times, rotation=90)

    #display the legend label
    plt.legend()

    #display the figure
    #plt.show()

    # save as png
    plt.savefig(title + '.png')
    print 'saved chart to ' + title + '.png'

def draw_chart_percent(np_data, title, x_column, y_column):

    fig = plt.figure()
    fig.set_size_inches(16, 9)

    ax1 = fig.add_subplot(111)
    ax1.set_title(title)

    x_temp = []
    y_temp = []
    for t in np_data[x_column]:
        if t is None or t == 'N/A':
            x_temp.append(0)
        else:    
            x_temp.append(t.replace('%', ' ').strip())
    for t in np_data[y_column]:
        if t is None or t == 'N/A':
            y_temp.append(0)   
        else:
            y_temp.append(t.replace('%', ' ').strip())

    #set y axis max value is 101
    plt.ylim(ymin = 90, ymax = 101)
    plt.ylabel('% Percent')

    ax1.plot(x_temp, c='red', label=title + ' read')

    ax2 = fig.add_subplot(111)
    ax2.plot(y_temp, c='blue', label=title + ' write')

    #get and modify x axis label
    times = process_x_labels(ax1, np_data['timestamp'])
    #modify x axis label
    ax1.set_xticklabels(times, rotation=90)

    #display the legend label
    plt.legend()

    # save as png
    plt.savefig(title + '.png')
    print 'saved chart to ' + title + '.png'

def process_x_labels(ax1, t_temp):
    labels = [item.get_text() for item in ax1.get_xticklabels()]
    #print 'labels: ', labels

    idx = 0
    times = []
    length = len(t_temp)

    time_max_pt = len(labels)

    t_step=length / time_max_pt

    while(length > idx):
        times.append(t_temp[idx])
        idx += t_step

    return times

def draw_all_charts():
    #get data from csv file
    np_data = process_data()

    draw_chart(np_data, 'Op-Count', 'op_read', 'op_write')
    draw_chart(np_data, 'Byte-Count', 'byte_read', 'byte_write')
    draw_chart(np_data, 'Avg-ResTime', 'avg_read', 'avg_write', 'ms')
    draw_chart(np_data, 'Throughout', 'throughout_read', 'throughout_write')
    draw_chart(np_data, 'Bandwidth', 'band_read', 'band_write')
    draw_chart_percent(np_data, 'Succ-Ratio', 'succ_read', 'succ_write')

if __name__ == '__main__':
    draw_all_charts()
