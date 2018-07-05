#coding:utf-8
file = open("ex.txt","w+")
f = open("/home/hadoop/Desktop/u.data","r")
for line in f.readlines():
	file.write(str(line.split("\t")[0])+"\n")

file.close()
f.close()