arr1=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
a=int(len(arr1)/7)
#print(arr1)
arr=[]
#print(a)
for i in range(0,7):
    for j in range(0,a):
        arr.append(arr1[i+j*7])
        print(arr)



#print(arr)