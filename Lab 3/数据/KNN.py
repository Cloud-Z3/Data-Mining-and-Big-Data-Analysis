import math

def findNN(dataset,testData,k):                 #找到原数据中距测试数据最近的k个值并返回
    distances=[]
    i=0
    for data in dataset:
        distances.append([computeDis(testData,data),i])
        i+=1
    distances_s=sorted(distances,key=lambda m: m[0])[:k]     #距离最小的k个数据
    id=[distances_s[i][1] for i in range(len(distances_s))]  #距离最小的k个数据的序号
    return id

def computeDis(x,y):                                         #计算欧氏距离
    return math.sqrt(math.pow(float(x[0])-float(y[0]),2)+math.pow(float(x[1])-float(y[1]),2))

def vote(dataset,indexs,votes):                              #返回k个最邻近数据中相同标签数最多的值
    for i in indexs:
        label=dataset[i][2]
        if label not in votes.keys():
            votes[label]=1
        else:
            votes[label]+=1
    return (max(votes,key=votes.get))

if __name__=='__main__':                #主函数入口
    dataset = []
    distances = []
    testdataset=[]


    with open(r'G:\大学\数据挖掘\实验3\数据\forKNN\iris.2D.train.txt', 'r') as fin:     #打开训练集文件
        for line in fin.readlines():
            data=(line.strip().split(','))
            dataset.append(data)

    with open(r'G:\大学\数据挖掘\实验3\数据\forKNN\iris.2D.test.txt', 'r') as fin:      #打开测试集文件
        for line in fin.readlines():
            data=(line.strip().split(','))
            testdataset.append(data)
    vote_result=[]
    for i in range(len(testdataset)):                                               #计算得到每个测试数据的分类
        votes={}
        indexs=findNN(dataset,[testdataset[i][0],testdataset[i][1]],3)
        vote_result.append(vote(dataset,indexs,votes))

    for i in range(len(testdataset)):
        print('data:'+testdataset[i][0]+' '+testdataset[i][1])                       #将数据打印处理
        print('real_label:'+testdataset[i][2]+'\nestimated_label:'+vote_result[i]+'\n') #将数据真实标签和预测标签作比较
    all_right_num=sum([vote_result[i]==testdataset[i][2] for i in range(len(testdataset))])
    print('Rightrate:',str(all_right_num/len(testdataset)*100)+'%')                  #计算分类正确的百分比