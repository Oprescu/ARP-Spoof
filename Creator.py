import socket
import sys

def Main():
    while True:
        job = input("Enter Job Type: ")
        if job == "reverse":
            jobInput = input("String to reverse: ")
            haveJob("revStr", "Reverses a String", 1, jobInput)
    

def haveJob(jobType, description, nrOfSeekers, jobInput):
    host = "127.0.0.1"
    port = int(sys.argv[1])
    mySocket = socket.socket()
    mySocket.bind((host,port))
     
    
    
    while True:
        print ("Looking for seeker...")
        mySocket.listen(0)
        conn, addr = mySocket.accept()
        print ("Connection from seeker: " + str(addr))
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