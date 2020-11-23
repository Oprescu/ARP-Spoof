import socket
import sys
import random
import threading


"""
def Main():
    #jobList = ["reverse", "addition", "subtraction", "multiplication", "RPS"]
    while True:

        #job = jobList[random.randint(0, 4)]
        # job = input("Enter Job Type: ")
        
        if job == "reverse":
            jobInput = input("String to reverse: ")
            haveJob("revStr", "Reverses a String", 1, jobInput)
        elif job == "addition":
            # a = random.randint(0, 99)
            # b = random.randint(0,99)
            print("Addition")
            a = int(input("Enter first integer value: "))
            b = int(input("Enter second integer value: "))
            print(f"Addition between two values {a} and {b}. ")
            jobInput = "{}+{}".format(a, b)
            haveJob("Addition", "Add 2 numbers", 1, jobInput)
        elif job == "subtraction":
            # a = random.randint(0, 99)
            # b = random.randint(0,99)
            print("Subtraction")
            a = int(input("Enter first integer value: "))
            b = int(input("Enter second integer value: "))
            print(f"Subtraction between two values {a} and {b}. ")
            jobInput = "{}-{}".format(a, b)
            haveJob("Subtraction", "Subtract 2 numbers", 1, jobInput)
        elif job == "multiplication":
            # a = random.randint(0, 99)
            # b = random.randint(0,99)
            print("Multiplication")
            a = int(input("Enter first integer value: "))
            b = int(input("Enter second integer value: "))
            print(f"Multiplication between two values {a} and {b}. ")
            jobInput = "{}x{}".format(a, b)
            haveJob("Multiplication", "Multiply 2 numbers", 1, jobInput)
        elif job == "RPS":
            print("Rock Paper Scissors")
            multiJob("RPS", "choose either Rock(1), Paper(2) or Scissors(3)", 2, "")

def multiJob(jobType, description, nrOfSeekers, jobInput):
    host = "127.0.0.1"
    port = int(sys.argv[1])
    client1 = -1
    client2 = 2
    while True:
        mySocket = socket.socket()
        mySocket.bind((host, port))
        print("Looking for seeker...")
        mySocket.listen(0)
        conn, addr = mySocket.accept()
        print("Connection from seeker: " + str(addr))
        message = jobType + "," + description + "," + str(nrOfSeekers) + "," + jobInput

        conn.send(message.encode())
        data = conn.recv(1024).decode()
        if not data:
            conn.close()
            mySocket.close()
            break
        if data == "refuse":
            print("Job refused by seeker")
            conn.close()
            mySocket.close()
        else:
            print("Data returned from seeker: " + str(data))
            client1 = int(data)
            conn.close()
            mySocket.close()
            break

    while True:
        mySocket = socket.socket()
        mySocket.bind((host, port))
        print("Looking for seeker...")
        mySocket.listen(0)
        conn, addr = mySocket.accept()
        print("Connection from seeker: " + str(addr))
        message = jobType + "," + description + "," + str(nrOfSeekers)

        conn.send(message.encode())
        data = conn.recv(1024).decode()
        if not data:
            conn.close()
            mySocket.close()
            break
        if data == "refuse":
            print("Job refused by seeker")
            conn.close()
            mySocket.close()
        else:
            print("Data returned from seeker: " + str(data))
            client2 = int(data)
            conn.close()
            mySocket.close()
            break
    if client1 == client2:
        print("The game is a draw, both clients selected same answer")
    elif client1 == 1:
        if client2 == 2:
            print("Client 2 is the winner (Paper > Rock)")
        else:
            print("Client 1 is the winner (Rock > Scissors)")
    elif client1 == 2:
        if client2 == 1:
            print("Client 1 is the winner (Paper > Rock")
        else:
            print("Client 2 is the winner (Scissors > Paper)")
    elif client1 == 3:
        if client2 == 1:
            print("Client 2 is the winner (Rock > Scissors)")
        else:
            print("Client 1 is the winner (Scissors > Paper)")

"""
#def haveJob(jobType, description, nrOfSeekers, jobInput):

def newClient(csock, address):
    csock.send("Hello Client!!!!".encode())
    data = csock.recv(1024).decode()
    print(f"{address} sent: {data}")
       # msg=input("Send a message to the client")
        #csock.send(msg.encode())

    csock.close()

def Main():
    host = "127.0.0.1"
    #port = int(sys.argv[1])
    jobList = ["checkIfOnline", "detectPortStatus"]
    port= 5000
    while True:
        mySocket = socket.socket()
        mySocket.bind((host, port))

        # while True:
        mySocket.listen(0)
        #conn, addr = mySocket.accept()

        while True:
            print("Looking for seekers...")
            conn, addr = mySocket.accept()
            print("Connection from seeker: " + str(addr))
        #threading.start_new_thread(newClient, (conn,addr))
            cThread = threading.Thread(target=newClient, args=(conn,addr,))
            cThread.start()

        #message = jobType + "," + description + "," + str(nrOfSeekers) + "," + jobInput
        #message = ": hello";
        #conn.send(message.encode())


        #data = conn.recv(1024).decode()
        if not data:
            conn.close()
            mySocket.close()

        if data == "refuse":
            print("Job refused by seeker")
            conn.close()
            mySocket.close()
        else:
            print("Data returned from seeker: " + str(data))
            conn.close()
            mySocket.close()



if __name__ == '__main__':
    Main()