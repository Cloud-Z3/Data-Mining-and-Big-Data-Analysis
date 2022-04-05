import matplotlib.pyplot as plt
f=open('data.txt')
points=[]
for i in f:
    a=i.split()
    points.append([eval(a[0]),eval(a[1])])
l=len(points)
print(l)
x=[points[i][0] for i in range(l)]
y=[points[i][1] for i in range(l)]
plt.scatter(x,y,marker='.')
plt.show()