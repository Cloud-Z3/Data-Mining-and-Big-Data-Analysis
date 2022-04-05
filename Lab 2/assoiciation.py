import collections
import itertools

class Apriori:
    traDatas=[]
    traLen=0
    k=1
    traCount={}
    freTran={}          #k一定时的频繁项集
    sup=0
    conf=0
    freAllTran={}       #所有频繁项集
    rules=[]

    def __init__(self,traDatas,sup,conf): #初始化，将数据、最小支持度、最小置信度赋给生成的Apriori类
        self.traDatas=traDatas
        self.traLen=len(traDatas)
        self.sup=sup
        self.conf=conf

    def scanFirDatas(self):              #扫描数据，将数据中所有字母及其频数的键值对存在字典类型的traCount中
        tmpStr=''.join(traDatas)
        self.traCount=dict(collections.Counter(tmpStr))
        return self.traCount

    def getFreset(self):                 #得到频繁项集及其频数，此键值对存在freAllTran中
        self.freTran={}
        for tra in self.traCount.keys():
            if self.traCount[tra]>=self.sup and len(tra)==self.k:
                self.freTran[tra]=self.traCount[tra]
                self.freAllTran[tra]=self.traCount[tra]

    def cmpTwoSet(self,setA,setB):       #判断两个k元集的并是否恰为k+1元集（众所周知，如果|A-B|=|B-A|=1，则k元集A、B的并恰为k+1元集）
        setA=set(setA)
        setB=set(setB)
        if len(setA-setB)==1 and len(setB-setA)==1:
            return True
        else:
            return False

    def selfConn(self):                  #自连接，从k元频繁项集生成k+1元频繁项集
        self.traCount={}
        for item in itertools.combinations(self.freTran.keys(),2):   #生成所有k元频繁项集的两两组合
            if self.cmpTwoSet(item[0],item[1]) == True:
                key=''.join(sorted(''.join(set(item[0]).union(set(item[1])))))  #key为满足条件的k+1元频繁项集（候选）
                if self.cutBranch(key) != False:                     #如果key是频繁项集，则先将其对应的频数置为0（创建键值对）
                    self.traCount[key]=0

    def scanDatas(self):                 #扫描所有数据（事务），更新新产生key对应的频数
        self.k=self.k+1
        for tra in traDatas:
            for key in self.traCount.keys():
                self.traCount[key]=self.traCount[key]+self.findChars(tra,key)

    def cutBranch(self,key):             #剪枝，如果k+1元候选频繁项集有非频繁的k项子集，则返回False
        for subKey in list(itertools.combinations(key,self.k)):
            if ''.join(list(subKey)) not in self.freTran.keys():
                return False

    def findChars(self,str,chars):       #如果chars所有字母都在str中，则返回1，否则返回0
        for char in list(chars):
            if char not in str:
                return 0
        return 1

    def permutation(self,string,pre_str,container):
        if len(string)==1:
            container.append(pre_str+string)

        for idx,str in enumerate(string):     #生成string的索引序列
            new_str=string[:idx]+string[idx+1:]
            new_pre_str=pre_str+str

            self.permutation(new_str,new_pre_str,container)

    def genAssRule(self):        #产生关联规则
        container=[]
        ruleSet=set()            #关联规则的集合
        for item in self.freTran.keys():
            self.permutation(item,'',container)
        for item in container:
            for i in range(1,len(item)):
                #print(item[:i]+" "+item[i:])
                ruleSet.add((''.join(sorted(item[:i])),''.join(sorted(item[i:])))) #在关联规则集合中添加规则（键值对）
            for rule in ruleSet:
                if self.calcConfi(rule[0],rule[1])>self.conf:                      #打印置信度大于最小置信度的规则
                    #continue
                    if rule[0]+"---->>>"+rule[1] not in self.rules:
                        self.rules.append(rule[0]+"---->>>"+rule[1])
                    #print(rule[0]+"---->>>"+rule[1])

    def calcConfi(self,first,last):                   #计算置信度
        return self.freAllTran[''.join(sorted((first+last)))]/self.freAllTran[''.join(sorted(first))]

    def algorithm(self):                              #Apriori算法
        self.scanFirDatas()
        while self.traCount != {}:
            self.getFreset()
            self.selfConn()
            self.scanDatas()
        #print(self.freAllTran)
        #print(self.freTran)
        self.genAssRule()
        print(self.rules)

traDatas=['abc','ae','abc','ade']                   #使用的数据集，用于挖掘关联规则
apriori=Apriori(traDatas,2,0.7)
apriori.algorithm()