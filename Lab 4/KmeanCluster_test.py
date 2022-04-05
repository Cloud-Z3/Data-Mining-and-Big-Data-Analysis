import os
import turtle
from random import*
from KmeanCluster import*

def pointsget(requirement):
    pointlist=[]
    for i in range(len(requirement)):
        for j in range(requirement[i][3]):
            x=requirement[i][2]*random()+requirement[i][0]-requirement[i][2]/2
            y=requirement[i][2]*random()+requirement[i][1]-requirement[i][2]/2
            pointlist.append([x,y])
    return pointlist

def drawgragh(points,pen_size,color):
    expo=points
    for i in range(len(expo)):
        for j in range(len(expo[i])):
            expo[i][j]*=1
    turtle.hideturtle()
    a=expo
    turtle.setup(3600,1000,0,0)
    turtle.speed(0)
    turtle.pensize(pen_size)
    turtle.pencolor(color)
    turtle.up()
    for m in a:
        turtle.goto(m[0],m[1])
        turtle.down()
        turtle.goto(m[0],m[1])
        turtle.up()

f = open('data.txt')
points = []
for i in f:
    a = i.split()
    points.append([eval(a[0]), eval(a[1])])
k=3                                                           #在这里输入簇数k的值
#建议k的值不超过7
####

colorlist=['red','peru','gold','lawngreen','cyan','navy','purple','hotpink']
lastcluster=Kmean(points,k)
#drawgragh(pointlist,2,'white')
print(lastcluster)
for i in range(len(lastcluster)):
    drawgragh(lastcluster[i],4,colorlist[i])
turtle.done()
os.system('pause')


