import im  
import time
server= im.IMServerProxy("https://web.cs.manchester.ac.uk/a65914zc/comp28112_ex1/IMserver.php")

server_tag = 1  # lock
Robert_time = 0  
Ned_time = 0     


def Robert():
    global server_tag, Robert_time, Ned_time
    if (server_tag == 1):  
        print("Ned just said: " + str(server["Ned" + str(Ned_time)]) )
        # Ned()
        Robert_time += 1  
        # Ned()
        server["Robert" + str(Robert_time)] = input("Hello, Robert! Please input your message here: ")
        # Ned()
        print("Sending to the server... (sleep 3s)")
        # Ned()
        time.sleep(3)
        # Ned()
        server_tag = 0  
        print("Now, tag is set to 0! It's Ned's turn! ")
        Ned()  # GIVE UP RESOURCE
    else:
        print("Sorry, Ned is typing something, please wait! ")  # NOT ALLOWED


def Ned():
    global server_tag, Robert_time, Ned_time
    if (server_tag == 0):
        print("Robert just said: " + str(server["Robert" + str(Robert_time)]) )
        
        Ned_time += 1  
        server["Ned" + str(Ned_time)] = input("Hello, Ned! Please input yout message here: ")
  
        print("Sending to the server... (sleep 3s)")
        time.sleep(3)
        
        server_tag = 1  
        print("Now, tag is set to 1! It's Robert's turn! ")    
        Robert()  # GIVE UP RESOURCE
    else:
        print("Sorry, Robert is typing something, please wait! ")  # NOT ALLOWED
        

Robert()
