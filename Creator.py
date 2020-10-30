import socket
import sys
import random


def Main():
    jobList = ["reverse", "addition", "subtraction", "multiplication"]
    while True:
        job = jobList[random.randint(0, 3)]
        #job = input("Enter Job Type: ")

        if job == "reverse":
            jobInput = input("String to reverse: ")
            haveJob("revStr", "Reverses a String", 1, jobInput)
        elif job == "addition":
            #a = random.randint(0, 99)
            #b = random.randint(0,99)
            print("Addition")
            a = int(input("Enter first integer value: "))
            b = int(input("Enter second integer value: "))
            print(f"Addition between two values {a} and {b}. ")
            jobInput = "{}+{}".format(a,b)
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

def haveJob(jobType, description, nrOfSeekers, jobInput):
    host = "127.0.0.1"
    port = int(sys.argv[1])
    mySocket = socket.socket()
    mySocket.bind((host, port))

    while True:
        print("Looking for seeker...")
        mySocket.listen(0)
        conn, addr = mySocket.accept()
        print("Connection from seeker: " + str(addr))
        message = jobType + "," + description + "," + str(nrOfSeekers) + "," + jobInput

        conn.send(message.encode())
        data = conn.recv(1024).decode()
        if not data:
            break
        if data == "refuse":
            print("Job refused by seeker")
        else:
            print("Data returned from seeker: " + str(data))
            break

    conn.close()


if __name__ == '__main__':
    Main()
