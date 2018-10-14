import csv
import math
import random
filename ="SPECT.csv"
res1="Yes"
res2="No"
bias=0
inputs=[]
no_of_rows=-1
result=0
def distance(l1,l2):    #dist betn each corresponding pts in l1 and l2
        ans=0
        for i in range(len(l1)-1):
                ans=ans+(l1[i]-l2[i])*(l1[i]-l2[i])
        return ans

def cross_validation(dataset, n_folds,k):  #returns cross fold validation
	dataset_split = list()
	dataset_copy = list(dataset)
	fold_size = int(len(dataset) / n_folds)
	for i in range(n_folds):
		fold = list()
		while len(fold) < fold_size:
			index = random.randrange(len(dataset_copy))
			fold.append(dataset_copy.pop(index))
		dataset_split.append(fold)
	folds=dataset_split
	return folds
	"""test_set=folds[0]
	train_set=[]
	for i in range(0,10):
		if i!=k:
			train_set.append(fold[i])
	
	return [train_set,test_set]"""

with open(filename,'r') as csvfile:
        csvreader=csv.reader(csvfile)       #format input dataset
        for row in csvreader:
                no_of_features=len(row)-1
                if(row[result]==res1):
                        row.pop(0)
                        row.append(1)
                if(row[result]==res2):
                        row.pop(0)
                        row.append(0)
                inputs.append(row)
                no_of_rows=no_of_rows+1
inputs.pop(0)

print("No of features in dataset:",no_of_features)
print("No of tuples in dataset:",no_of_rows)

def find(xx):
        return xx[0]     #return first element of list

for i in range(no_of_rows):
        for j in range(no_of_features+1):
                inputs[i][j]=float(inputs[i][j])

print("Enter the value of k:")
k=int(input())

inputs=cross_validation(inputs,10,k)
#print(len(x))
nfold=len(inputs)  #10
infold=len(inputs[0])  #26
feat=len(inputs[0][0])  #23

def find_knn(dist,k):
    l=len(dist)
    mini=1000000                         #find knn using distance
    ind=0
    for i in range(l-k+1):
        if(dist[i][0]-dist[i+k-1][0])<mini:
            mini=dist[i][0]-dist[i+k-1][0]
            ind=i
    p=0
    n=0
    for i in range(ind,ind+k):
        if(dist[ind][1]==0):
            n+=1
        else:
            p+=1
    if(p>=n):
        return 1
    else:
        return 0

pp=0.0
pm=0.0
rp=0.0
rm=0.0
    
accuracy=[0 for i in range(len(inputs))]
s_accur=0
for i in range(len(inputs)):                  #find the accuracy for each fold
    c_accur=0
    tp=0
    tn=0
    fp=0
    fn=0
    for m in range(infold):
        dist=[]
        for j in range(len(inputs)):
            if(j!=i):
                for p in range(infold):
                    a=distance(inputs[i][m],inputs[j][p])
                    dist.append([a,inputs[j][p][22]])
                    #inputs[j][p].append(a)
        dist.sort(key=find)
        cl=find_knn(dist,k)
        if(cl==inputs[i][m][22] and cl==1):
            tp+=1
        if(cl==inputs[i][m][22] and cl==0):
            tn+=1
        if(cl!=inputs[i][m][22] and cl==1):
            fp+=1
        if(cl!=inputs[i][m][22] and cl==0):
            fn+=1
    if(tp+fp!=0):
        #print("Precision(+):",tp/(tp+fp))
        pp+=(tp/(tp+fp))
    else:
        #print("Precision(+):INF")
        pp+=0
    if(tn+fn!=0):
        #print("Precision(-):",tn/(tn+fn))
        pm+=(tn/(tn+fn))
    else:
        #print("Precision(-):INF")
        pm+=0
    if(tp+fn!=0):
        #print("Recall(+):",tp/(tp+fn))
        rp+=(tp/(tp+fn))
    else:
        #print("Recall(+):INF")
        rp+=0
    if(tn+fp!=0):
        #print("Recall(-):",tn/(tn+fp))
        rm+=(tn/(tn+fp))
    else:
        #print("Recall(-):INF")
        rm+=0
    accuracy[i]=(tp+tn)/(tp+tn+fp+fn)
    s_accur+=accuracy[i]

#print the average accuracy
print("Accuracy is:",s_accur/len(inputs)*100,"%")
print("Precision(+):",pp/len(inputs))
print("Precision(-):",pm/len(inputs))
print("Recall(+):",rp/len(inputs))
print("Recall(-):",rm/len(inputs))
