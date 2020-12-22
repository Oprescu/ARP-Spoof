from scapy.all import *
import socket




def Main():
    # add creator host IP's here
    host = ['127.0.0.1', '127.0.0.1']
    port = [5000, 5001]

    i = -1
    while True:
        i += 1
        if i == len(host):
            i = 0
        while True:
            try:
                # print("Asking " + host[i] + ":" + str(port[i]) + " for a job...")
                print("looking for " + host[i] + ":" + str(port[i]))
                mySocket = socket.socket()
                mySocket.connect((host[i], port[i]))
                break
            except:
                break
        data = ""
        mySocket.settimeout(1)
        try:
            data = mySocket.recv(1024).decode()
        except:
            pass
        if data == "":
            pass
        else:
            data = str(data)
            # print("Job found from creater : " + data)
            print("Message recieved from creator\n" + data)
            status = input("Accept job? Y/N: ").upper()

            mySocket.send(status.encode())
            if (status == "Y"):
                mySocket.settimeout(45)
                print("Waiting for creator to respond")

                # try:
                jobRECEIVE = mySocket.recv(1024).decode()
                jobSPLIT = jobRECEIVE.split("$")
                print(jobSPLIT[0])
                #print(jobSPLIT[1])
                #print(jobSPLIT[2])
                jobHandler(jobSPLIT[0], jobSPLIT[1], jobSPLIT[2], mySocket)
                # except:
                #   print("Uh oh. The creator was too slow!")
            # data=mySocket.recv(1024).decode()
            # print(f"message is {data}")
        mySocket.close()


if __name__ == '__main__':
    Main()
