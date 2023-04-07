import numpy as np
import main


#Πίνακας που μας δίνει το αποτέλεσμα του xor μεταξύ όλων τον bits ενος αριθμού δηλαδη ο αριθμος 5 βρίσκεται στην θέση 6 του πίνακα αρα x1^x2^x3^x4=0
arr = [0,1,1,0,1,0,0,1,1,0,0,1,0,1,1,0]
print(arr)
#Πινακας γραμμικών προσσεγγίσεων
pinakas = np.matrix(np.zeros((16, 16), dtype = np.int))

#Πινακας διαφορών
pinakas2 = np.matrix(np.zeros((16, 16), dtype = np.int))

num=0
sum=0
for i in range(16):
    for j in range(16):
        sum=0
        for k in range(16):
            for l in range(16):
                num = arr[(i&l)]^arr[(j&main.S_Box[l])]
                if(num==1):
                    sum-=1
                else:
                    sum+=1
            pinakas[i,j]=sum/2
            sum=0
print(pinakas)
print()
print()
print()
lista = []
lista2 = []
for i in range(16):  
    for k in range(16):
        for l in range(16):
            lista.append(main.S_Box[l]^main.S_Box[l^i])
        
        num2=0
        for m in lista:
            if k==m:
                num2+=1
        pinakas2[i,k] = num2
        lista.clear()
print(pinakas2)
