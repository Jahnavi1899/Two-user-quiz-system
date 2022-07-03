#socket creation
#connecting with the 2 clients
#take input from user
#read question and answer from the inputted quiz file
#write the question function
#score calculation
#printing of the result
#close the socket

#encode()=convert string to bytes
##required before sending any message in python 3.7.4 as in this the parameters must be in bytes but we want to send strings data.So this conversion is required before sending any message.
#decode("utf-8")=convert bytes to string
##required after receiving any message in python 3.7.4 as in this the parameters sent are in bytes but we want to receive strings data .So this conversion is required before using the received message any where in the program.

import socket
import time

host = 'localhost'
port = int(input("Enter the port number for the server => "))
total_ques = int(input("Enter the number of questions => "))
quiz_file = input("Enter the name of the quiz file => ")
f = open(quiz_file, 'r')
score = [0, 0]  # initialise the score of 2 clients to 0


def Questions(connlist, player, to_challenge, challenger, question, answer):
    global score
    global f
    
    connlist[player].sendall("Q\n".encode())
    time.sleep(0.1)
    connlist[player].sendall((question+"\n").encode())
    time.sleep(0.1)
    ans = connlist[player].recv(1024)
    ans = ans.decode("utf-8")
    if answer == ans+'\n':
        score[player] = score[player]+10
        connlist[player].sendall("Correct Answer\n".encode())
        time.sleep(0.1)
    else:
        if to_challenge == True:
            Questions(connlist, 1-player, False, True, question, answer)
        if challenger == True:
            score[player] = score[player]-10
        connlist[player].sendall("Incorrect Answer\n".encode())
        time.sleep(0.1)

def Score(connlist):
    global score
    for i, conn in enumerate(connlist):
        conn.sendall("S\n".encode())
        time.sleep(0.1)
        conn.sendall(("Player "+str(i+1)+" score is "+str(score[i])+"\n").encode())
        time.sleep(0.1)
        


sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sk.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sk.bind((host,port))#bind takes only one argument
sk.listen(2) # only 2 users are trying to connect with this server at a time

print("Server host and port is ", host, port)
print("Waiting to be connected with the 2 players")
(conn1, address1) = sk.accept()
print("Connected with player 1 with address ", address1)
(conn2, address2) = sk.accept()
print("Connected with player 2 with address ", address2)
connlist = [conn1, conn2]

conn1.sendall("A\n".encode())
time.sleep(0.1)
conn1.sendall("You are player 1 \n".encode())
time.sleep(0.1)
conn2.sendall("A\n".encode())
time.sleep(0.1)
conn2.sendall("You are player 2 \n".encode())

for ques in range(total_ques):
    conn1.sendall("A\n".encode())
    time.sleep(0.1)
    conn1.sendall(("Question number "+str(ques+1)+" is for Player "+str(ques%2+1)+"\n").encode())
    time.sleep(0.1)
    conn2.sendall("A\n".encode())
    time.sleep(0.1)
    conn2.sendall(("Question number "+str(ques+1)+" is for Player "+str(ques%2+1)+"\n").encode())
    #Challenge question
    connlist[1-ques%2].sendall("C\n".encode())
    time.sleep(0.1)
    connlist[1-ques%2].sendall("Do u want to challenge player for the next question\n".encode())
    time.sleep(0.1)
    choice = connlist[1-ques%2].recv(1024)
    choice = choice.decode("utf-8")
    if choice[0] == "Y":
        to_challenge = True
    elif choice[0] == "N":
        to_challenge = False
    else:
        print("Enter valid answer")
    question = f.readline()
    answer = f.readline()
    Questions(connlist, ques%2, to_challenge, False, question, answer)
    Score(connlist)

if score[0] > score[1]:
    print("Player 1 won with ",score)
    conn1.sendall("X\n".encode())
    time.sleep(0.1)
    conn1.sendall("YOU WON!!\n".encode())
    time.sleep(0.1)
    conn2.sendall("X\n".encode())
    time.sleep(0.1)
    conn2.sendall("YOU LOST\n".encode())
    time.sleep(0.1)
elif score[0] < score[1]:
    print("Player 2 won with ",score)
    conn1.sendall("X\n".encode())
    time.sleep(0.1)
    conn1.sendall("YOU LOST\n".encode())
    time.sleep(0.1)
    conn2.sendall("X\n".encode())
    time.sleep(0.1)
    conn2.sendall("YOU WON!!\n".encode())
    time.sleep(0.1)
else:
    print("It's a tie with a score of ",score)
    conn1.sendall("X\n".encode())
    time.sleep(0.1)
    conn1.sendall("IT'S A TIE\n".encode())
    time.sleep(0.1)
    conn2.sendall("X\n".encode())
    time.sleep(0.1)
    conn2.sendall("IT'S A TIE\n".encode())
    time.sleep(0.1)
sk.close()
    
    
   
    

