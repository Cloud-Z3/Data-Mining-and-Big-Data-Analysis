# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 20:37:40 2021

@author: Lenovo
"""
import pandas as pd
import numpy as np
from collections import Counter


def loadLabor(address):  # 加载数据
    spf = pd.read_csv(address, sep=',', index_col=False, header=None)
    column = ['duration', 'wage-increase-first-year', 'wage-increase-second-year', 'wage-increase-third-year',
              'cost-of-living-adjustment', 'working-hours', 'pension', 'standby-pay',
              'shift-differential', 'education-allowance', 'statutory-holidays', 'vacation',
              'longterm-disability-assistance', 'contribution-to-dental-plan', 'bereavement-assistance',
              'contribution-to-health-plan', 'class']  # 所有标签
    spf.columns = column
    str_typeName = ['cost-of-living-adjustment', 'pension', 'education-allowance',
                    'vacation', 'longterm-disability-assistance', 'contribution-to-dental-plan',
                    'bereavement-assistance', 'contribution-to-health-plan', 'class']  # 字符数据标签

    str2numeric = {}
    str2numeric['?'] = '-1'
    return spf, str2numeric, str_typeName


def fillMissData(spf, str_typeName):  # 缺失值填充
    row, col = spf.shape
    columns = spf.columns
    for column_name in columns:  # 将'？'替换为'-1'
        if column_name not in str_typeName:
            tmp = spf[column_name]
            for i in range(len(tmp)):
                if tmp[i] != '?':
                    tmp[i] = float(tmp[i])
            ave = np.average(tmp[tmp != '?'])
            tmp[tmp == '?'] = ave
            spf[column_name] = tmp
        else:
            v = spf[column_name].values
            v1 = v[v != '-1']
            c = Counter(v1)
            cc = c.most_common(1)
            v[v == '-1'] = cc[0][0]
        return spf


if __name__ == '__main__':  # 主函数
    filepath = 'G:\\大学\\数据挖掘\\laborMissing.txt'
    fillFilepath = 'G:\\大学\\数据挖掘\\laborMissing_handle.txt'
    spf, str2numeric, str_typeName = loadLabor(filepath)
    spf = fillMissData(spf, str_typeName)
    spf.to_csv(fillFilepath, index=False, header=False)
