import socket
import sys
import random


def Main():
    jobList = ["reverse", "addition", "subtraction", "multiplication", "RPS"]
    while True:
        job = jobList[random.randint(0, 4)]
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


def haveJob(jobType, description, nrOfSeekers, jobInput):
    host = "127.0.0.1"
    port = int(sys.argv[1])
    
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
            conn.close()
            mySocket.close()
            break


if __name__ == '__main__':
    Main()
