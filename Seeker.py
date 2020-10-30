import socket

def Main():
    #add creator host IP's here
    host = ['127.0.0.1','127.0.0.1']
    port = [5000,5001]
     
    
    i=-1
    while True: 
        i+=1
        if i==len(host):
            i=0
        while True:
            try:
                print("Asking " + host[i] + ":" + str(port[i]) + " for a job...")
                mySocket = socket.socket()
                mySocket.connect((host[i],port[i]))
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
            print("Job found from creater : " + data)
            status=input("Accept job? Y/N: ")
            if status == "Y":
                data = data.split(",")
                jobType = data[0]
                description = data[1]
                nrOfSeekers = data[2]
                jobInput = data[3]
                if jobType == "revStr":
                    jobInput = jobInput[::-1]
                    mySocket.send(jobInput.encode()) 
                    print("Job Complete")
            else:
                mySocket.send("refuse".encode()) 
        mySocket.close()
 
if __name__ == '__main__':
    Main()