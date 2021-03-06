import csv, math, random, copy

def shuffle(array):
	for i in range(len(array)-1,0,-1):
		j=random.randint(0,i)
		array[i],array[j]=array[j],array[i]
	return array

def Euclid_distance(x,y):
	dist=0
	for i in range(len(x)):
		dist+=pow((x[i]-y[i]),2)
	dist=math.sqrt(dist)
	return dist

def mean_cluster(cluster):
	mean=[0 for i in range(len(cluster[0]))]
	for i in range(len(cluster[0])):
		for j in range(len(cluster)):
			mean[i]+=cluster[j][i]
		mean[i]=mean[i]/len(cluster)
	return mean

def k_mean_cluster(array,attributes,k):
	yes=0
	no=0
	for i in range(len(array)):
		if array[i][0]=="Yes":
			yes+=1
		elif array[i][0]=="No":
			no+=1
	print("Actual Yes : ",yes)
	print("Actual No : ",no)

	dataset=[]
	for i in range(len(array)):
		test=[]
		for j in range(1,len(attributes)):
			test.append(float(array[i][j]))
		dataset.append(test)
	#print(dataset)

	cluster_centre=[]
	a,b=random.sample(range(0,len(dataset)-1),2)
	cluster_centre.append(dataset[a])
	cluster_centre.append(dataset[b])

	epoch=1
	#for i in range(1000):
	while True:
		distance=[[0 for i in range(k)] for j in range(len(dataset))]
		for i in range(len(dataset)):
			for j in range(k):
				distance[i][j]=Euclid_distance(dataset[i],cluster_centre[j])

		yes_cluster=[]
		no_cluster=[]
		for i in range(len(distance)):
			m=min(distance[i])
			inde=distance[i].index(m)
			if inde==0:
				yes_cluster.append(dataset[i])
			elif inde==1:
				no_cluster.append(dataset[i])

		Mean=[]
		Mean.append(mean_cluster(yes_cluster))
		Mean.append(mean_cluster(no_cluster))

		#print("Mean : ",Mean)
		#print("Cluster Centre : ",cluster_centre)

		if cluster_centre==Mean:
			break

		cluster_centre=copy.deepcopy(Mean)
		epoch+=1

	print("Predicted Yes : ",max(len(yes_cluster),len(no_cluster)))
	print("Predicted No : ",min(len(no_cluster),len(yes_cluster)))
	acc=0

	y=0
	tp, tn, fp, fn=0, 0, 0, 0
	if len(yes_cluster)>len(no_cluster):
		for i in range(len(yes_cluster)):
				ind=dataset.index(yes_cluster[i])
				if array[ind][0]=="Yes":
					acc+=1
					tp+=1
				else:
					fp+=1
		for i in range(len(no_cluster)):
				ind=dataset.index(no_cluster[i])
				if array[ind][0]=="No":
					acc+=1
					tn+=1
				else:
					fn+=1
	else:
		for i in range(len(yes_cluster)):
				ind=dataset.index(yes_cluster[i])
				if array[ind][0]=="No":
					acc+=1
					fp+=1
				else:
					tp+=1
		for i in range(len(no_cluster)):
				ind=dataset.index(no_cluster[i])
				if array[ind][0]=="Yes":
					acc+=1
					fn+=1
				else:
					tn+=1

	acc=acc/len(dataset)*100
	precision=(tp/(tp+fp))*100
	recall=(tp/(tp+fn))*100

	print("Epoch : ",epoch)
	
	print("Accuracy : ",acc,"%")
	print("Precision : ",precision,"%")
	print("Recall : ", recall,"%")

def main():
	filename="SPECTF.csv"
	attributes=[]
	rows=[]
	with open(filename,'r') as csvfile:
		csvreader=csv.reader(csvfile)

		attributes=next(csvreader)
		for row in csvreader:
			rows.append(row)
	Rows=shuffle(rows)
	#Rows=list(rows)

	k=2
	k_mean_cluster(Rows,attributes,k)

if __name__ == '__main__':
	main()