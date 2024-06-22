""" (Suggest open this file in the VScode and Sublime to get a good reading experience)

# How to run this system???
(This system could both run on the macOS and Lunix on the school machine)
Prepare:
A folder having myserver.py, myclient.py and ex2utils.py was opened in the terminal.
Firstly, run the Command: "python3 myserver.py localhost 8090" to start the server.
Secondly, run the Command: "python3 myclient.py localhost 8090" to start the client, which could be used in several terminals representing different clients not just one.
There would be some hints on the server when a new client terminal was connected or disconnected (counting also worked if the client terminal was deliberately closed not through the command number).
(The server would also provide the hint if one name was "successfully" registered and exited for the client but the terminal should be disconnected through the command number in this case).

Steps:
In one client terminal, register the name like "Robert", the client terminal will ask you to input the operation number.
In another client terminal, register the name like "Ned", the client terminal will ask you to input the operation number.
And choose the operation number 1, 2, 3 or 4:

For the 1: (show all screen names connected to the server)
If Robert terminal input 1, the connected names would be shown (including Robert itself).
Note: If Ned has NOT input 1 before "Robert + 1 operation", the name list would not show Ned, since the server had not received the operation command and saved the name information "Ned" yet.
Note: If Ned has also input 1 before "Robert + 1 operation", the name list would both show the Robert and Ned as the connected clients.

For the 2: (send the message to EVERYONE)
If Robert terminal input 2, the system will provide hint and ask you to input the public content like
"Ned, be my hand of the king and help me"   and click "Enter(return)" on the keyboard.
Now, both Robert and Ned terminals would receive and see this message with the time.
(But Ned must finish a whole action: input the name and input any reasonable operation number to finish registration on the server).
The Ned could also do the same thing.

For the 3: (send the PRIVATE message)
To see what will happen for the operation 3, firstly, a new client should be created with new name like "Daenerys" with any operation number (except 4) (suggest just 1).
Then, if Robert terminal input 2, and put the information   "I am a king"
These three people would all receive and see this message with the time in their own terminal.
If Robert terminal input 3, the system will provide hint and ask you to input the PRIVATE content like
"Ned, the House Targaryen was dangerous"
Then, according to the hint and input the name for this private message like "Ned"
And only the Ned terminal would receive this message: "Ned, the House Targaryen was dangerous", Robert and Daenerys would not receive it.

For the 4: (exit)
For these three client terminals now, any one could input the operation number 4 to disconnect the server, relational message would also be shown in the server terminal.
If you kept one client, exiting the other two clients, and do the operation number 1, you would only see the name of this kept client, since names of the other two clients were deleted.
If you closed all three clients, the server will show the number of correct active clients: 0


# How to test the stability and functionality of this system???
## Stability:
### server:
To test the single point of failure, when two terminals were opened and running: one for server and one for client, the user could type any message in the server terminal 
and then click the "Enter(Return)" or other string keys on the keyboard without any effect (except control+C). And the client could also run and used as usual with the operation 1, 2, 3 or 4, 
since there was no pipeline to input words in the server terminal.
### client:
In the client terminal, the user would be asked to input data step by step: name, operation number, message (if possible) and the name to private chat (if possible).
For the "name", "message" and "the name to private chat", ALL strings and numbers were accepted, since they would not affect the principle of server interpretation.
For the operation number, the simple check would be set in the client terminal and control the input, which would be sent to the server, in [1, 4]
and return the hint in the client terminal if receiving a wrong number or strings.
Besides, the message, which would be sent to the server, was created in the client, using the special symbols "$_$_$_!@#" to concatenate them.
This symbol could be more difficult and complex using Hash function adding the number and the string,
and the server would interpret the command using this special symbol. The only way to destory this system was using BF to get this secret key and input it in client terminals.
However, if the destructive message with this symbol was sent to the server like name or message having "$_$_$_!@#", there would be a "try-except" in the server to catch errors of the interpretation and close the connection to this client terminal immediately.
(same principles were on the communication content and the name for the private chat, the name information in the server would also be deleted if the user firstly registered the name before sending "$_$_$_!@#")

## Functionality:
1. For the name already exists:
Two clients were created with the same name like "Robert", no matter which terminal input the operation number firstly, that terminal would be registered as the unique "Robert".
Another one would get the hint after input the operation number and may try other names OR WAITING until the former "Robert" exited (disconnected) to the server, since the name in the dictionary would be deleted when disconnection.
(The server will show the number of client numbers correctly AND it will also provide the hint WHEN the name was registered successfully.)
(BUT it will happen that: the number of clients is 2, but there was only one registered user in the server, which was accepted, since they were separate systems.)

2. For the incorrect operation number:
One client was registered with any name and input the any number or string except 1, 2, 3 or 4, the hint would be returned and user need to try again.

3. For the unreasonable target name in private chat:
One client was registered with any name and input 3 with any content, then input a NEW name, which had not been registered, and it will return the hint that "Sorry, this username has not been registered, please check and try again" in the client terminal.

4. For the disconnect:
One client was registered with "Robert" and input 1 to finish the register.
One client was registered with "Ned" and input 1 to finsh the register and checked the list (now there should be two items: Robert and Ned).
If a new client was created still using name "Robert" with operation number 4, the hint will return "This name is ALREADY registered".
AGAIN: in the "Ned" terminal, input the operation number 1, the Robert client was STILL there making no difference and the "Robert" terminal could work as usual.
Therefore, when a user input an existed name and the disconnection request, the hint would be provided as usual and it would NOT affect the current system(client).

"""

import sys
from ex2utils import Client
import os

class IRCClient(Client):
    def onMessage(self, socket, message):
        message = message.encode()
        if message == str("#_DISCONNECT_COMMAND_#").encode():
            print("Disconnect this client......")
            os._exit(0)
            return False

        elif message == str("#_ALREADY_EXIST_COMMAND_#").encode():
            self.name = input("This name is ALREADY registered, please try another one: \n")
            return True
        
        elif message == str("#_Malicious_ATTACK_DETECTED_#").encode():
            print("Malicious attack detected...Closing the client...")
            os._exit(0)
            return False
        
        else:
            print(message)  # message on the client
            return True
        
        
    def onStart(self): 
        print("# The client has been activated #")
        self.name = input("Please register (input) your name here: \n")
        
        
    def listen(self):
        while True:
            print("Operation number hint:")
            print("1 Show all screen names connected to the server now.")
            print("2 Input the public message.")
            print("3 Input the private message.")
            print("4 Disconnect this client.")
            operation = input("Please input your operation number: \n")
            
            if (operation == str(1)) or (operation == str(4)):
                message = self.name + "$_$_$_!@#" + operation + "$_$_$_!@#" + "default" + "$_$_$_!@#" + "default"
                client.send(message.encode())
            
            elif (operation == str(2)):
                content = input("Please type the message sent to everyone: \n")
                message = self.name + "$_$_$_!@#" + operation + "$_$_$_!@#" + content + "$_$_$_!@#" + "default"
                client.send(message.encode())
                
            elif (operation == str(3)):
                content = input("Please type the PRIVATE message: \n")
                private = input("Please type her/his name to send this private message: \n")
                message = self.name + "$_$_$_!@#" + operation + "$_$_$_!@#" + content + "$_$_$_!@#" + private
                client.send(message.encode())
                
            else:
                print("Note: Your operation number was not correct, please check and try again ")
          
                
ip = sys.argv[1]
port = int(sys.argv[2])
client = IRCClient()
client.start(ip, port)
client.listen()
