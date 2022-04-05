# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 19:36:46 2021

@author: Lenovo
"""

import numpy as np
import pandas as pd

def loadIris(address):#加载数据
    spf=pd.read_csv(address,sep=',',index_col=False,header=None)
    print(spf)
    strs=spf[4]
    spf.drop([0,4],axis=1,inplace=True)
    print(spf)
    return spf.values,strs

def normalization(data_matrix):#归一化
    e=1e-5
    for c in range(4):
        maxNum=np.max(data_matrix[:,c])
        minNum=np.min(data_matrix[:,c])
        data_matrix[:,c]=(data_matrix[:,c]-minNum+e)/(maxNum-minNum+e)
    return data_matrix

if __name__=='__main__':#主函数
    filepath='G:\\大学\\数据挖掘\\实验1\\iris.txt'
    writepath='G:\\大学\\数据挖掘\\实验1\\iris_normal.txt'
    data_matrix,str_name=loadIris(filepath)
    data_matrix=normalization(data_matrix)
    spf=pd.DataFrame(data_matrix)
    strs=str_name.values
    spf.insert(4,4,strs)
    #spf.to_csv(writepath,index=False,header=False)#将归一化的数据写入txt
    
