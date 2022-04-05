# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 21:16:07 2021

@author: Lenovo
"""

import pandas as pd
import numpy as np
from collections import Counter

def loadIris(address):#加载数据
    spf=pd.read_csv(address,sep='   ',index_col=False,header=None)
    strs=spf[0]
    spf.drop([0],axis=1,inplace=True) #此处去除了class特征
    return spf.values,strs

def getEnergy(c,data,label):#计算增益
    dataLen=len(label)
    energy=0.0
    for key,value in c.items():
        c[key]/=float(dataLen)
        label_picked=label[data==key]
        l=Counter(label_picked)
        e=0.0
        for k,v in l.items():
            r=v/float(value)
            e-=r*np.log2(r)
            energy+=c[key]*e
    return energy

def featureSelection(features,label):#根据增益进行特征筛选
    featureLen=len(features[0,:])
    label_count=Counter(label)
    samples_energy=0.0
    data_len=len(label)
    for i in label_count.keys():
        label_count[i]/=float(data_len)
        samples_energy-=label_count[i]*np.log2(label_count[i])    
    informationGain=[]
    for f in range(featureLen):
        af=features[:,f]
        minf=np.min(af)
        maxf=np.max(af)+1e-4
        width=(maxf-minf)/10.0    
        d=(af-minf)/width
        dd=np.floor(d)
        c=Counter(dd)
        sub_energy=getEnergy(c,dd,label)
        
        informationGain.append(samples_energy-sub_energy)
        
    return informationGain#返回增益值

if __name__=='__main__':#主函数
    filepath='iris.txt'
    data_matrix,str_name=loadIris(filepath)
    informationGain=featureSelection(data_matrix,str_name.values)
    print(informationGain)