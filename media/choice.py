import random
import string
import pickle
import sys
def randomword(length):
   letters = string.ascii_uppercase
   return ''.join(random.choice(letters) for i in range(length))

def fill_choice():
    data={}
    while len(data)<=99:
        data[random.randint(1,5000)]=randomword(4)
    file = open("new_int.p" , "wb")
    pickle.dump(data , file)
    file.close()
    #print(length(data))
fill_choice()
file2 = open(sys.argv[1] , "rb")
now = pickle.load(file2)
#rint(now)
lis=list(now.keys())
#print(lis)



def search(element,list1):
    for i in list1:
        if element==i:
            re = True
            break
        else :
            re = False
    return re
m=False

def reqFunc(li,x):
    for i in li:
        if search(int(x)-i,lis):
            global m 
            m= True
            return i
        else:
               # global m
            m = False

def ask_choice() :
#print(y)
    def disFunc(element,li):
        if len(li)>0:
            for i in li:
                if element+i<int(x):
                    return [element , i]
        else:
            return -1
        ele=li[0]
        del li[0]
        disFunc(ele,li)

    x=input("Enter a number between 5000 and 7000 : ")
    try:
        if 5000<=int(x)<=7000 :
            y=reqFunc(lis,x)
            #print(m)
            if m == True:
                print(now[y] , y)
                print(now[int(x)-y] ,int(x)-y)
            else:
                elemen=lis[0]
                del lis[0]
                if disFunc(elemen,lis)!= -1 :
                    print(now[disFunc(elemen , lis)[0]] , disFunc(elemen , lis)[0], now[disFunc(elemen , lis)[1]] , disFunc(elemen , lis)[1])
                #print(now[disFunc(elemen , lis)[1]] , disFunc(elemen , lis)[1])
                else:
                    print("Not Possible")
        else :
            raise ValueError
    except ValueError :
        print('Error : Please enter a value between 5000 and 7000')

ask_choice()
    
















