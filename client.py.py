#Creating the socket
#Write print function
#We do "%2" because if the no is even we will get 0 and if the no is odd we will get 1.So the answer will be either 1 or 0.
#Which helps us to use the clients with the help of their index in the connlist.
#In ask_question we are just asking user the question ,taking its input ,sending and printing wheather the entered answer is correct or not.
import socket


def challenge(sk):
    c = sk.recv(1024)
    c = c.decode("utf-8")
    print(c)
    a = input("Enter Y or N : ")
    while a not in ["Y","N"]:
        print ("Enter valid input")
        a=input("Enter Y or N : ")
    a=a.encode()
    sk.sendall(a)
    
def ask_question(sk):
    q=sk.recv(1024)
    q=q.decode("utf-8")
    print( "Question : ",q)
    a= input("Answer :")
    while a not in ["A","B","C","D"]:
        print("Enter valid answer")
        input("Answer :")
    a=a.encode()
    sk.sendall(a)
    result=sk.recv(1024)
    result=result.decode("utf-8")
    print(result)
    
    
def printing_func(sk):
    p=sk.recv(1024)
    p=p.decode("utf-8")
    print(p)
    
host='localhost'
port=int(input("Enter the port number of the server => "))
sk=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sk.connect((host,port))
while True:
    choice=sk.recv(1024)
    choice=choice.decode("utf-8")
    
    if choice[0]=="Q":
        ask_question(sk)
    elif choice[0]=="S":
        printing_func(sk)
    elif choice[0]=="C":
        challenge(sk)
    elif choice[0]=="X":
        printing_func(sk)
        break
    elif choice[0]=="A":
        printing_func(sk)
    else:
        print ("Invalid choice : ",choice)
        
        

