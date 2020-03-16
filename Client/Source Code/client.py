#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


LOGIN_STATE = 1
CHAT_ROOM_SELECT_STATE = 2
CHAT_ROOM_STATE = 3

##Make global some gui value to pass into Client
msg_list = None


class ChatClient:
    def __init__(self):
         #----Now comes the sockets part----
        self.HOST = "127.0.0.1"
        self.PORT = 33000

        self.BUFSIZ = 1024
        self.ADDR = (self.HOST, self.PORT)


        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)

        self.PageState =  CHAT_ROOM_STATE
        self.StateNum = 0
        self.connected = True
        
    def receive(self):
        """Handles receiving of messages."""
        while self.connected:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                if(self.PageState == CHAT_ROOM_STATE):
                    global msg_list 
                    msg_list.insert(tkinter.END, msg)
                elif(self.PageState == CHAT_ROOM_SELECT_STATE):
                    pass
                elif(self.PageState == LOGIN_STATE):
                    if(self.StepNum==0):
                        Self.StepNum +=1
                    elif(self.StepNum==1):
                        Self.StepNum +=1
                    elif(self.StepNum==2):
                        Self.StepNum +=1
                    elif(self.StepNum==3):
                        Self.StepNum +=1    
                        

                #msg_list.insert(tkinter.END, msg)
            except OSError:  # Possibly client has left the chat.
                break

    def send_message_into_ChatRoom(self,my_msg, is_cancel= False):  # event is passed by binders.
        """Handles sending of messages."""
        if(is_cancel):
            self.client_socket.send(bytes("{quit}", "utf8"))
            global app
            global receive_thread

            self.connected = False
            app.destroy()            
            self.client_socket.close()
            receive_thread.join(1)
            
        else:
            msg = my_msg.get()
            print(msg)
            my_msg.set("")  # Clears input field.
            self.client_socket.send(bytes(msg, "utf8"))
        


    def on_closing(self,event=None):
        """This function is to be called when the window is closed."""
        self.send_message_into_ChatRoom(None,is_cancel=True)
    

class ClientApp(tkinter.Tk):
    def __init__(self, inputChatClient , *args,**kwargs):
        self.CurrentChatClient = inputChatClient

        tkinter.Tk.__init__(self,*args,**kwargs)
        self.title("Chat Application")
        container = tkinter.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        
        self.frames = {}
        for F in (LoginPage, ChatRoomSelectPage, ChatRoomPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

        self.protocol("WM_DELETE_WINDOW", self.CurrentChatClient.on_closing)
    
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class LoginPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller

        #username label and text entry box
        usernameLabel = tkinter.Label(self, text="User Name").grid(row=0, column=0)
        username = tkinter.StringVar()
        usernameEntry = tkinter.Entry(self, textvariable=username).grid(row=0, column=1)  

        #password label and password entry box
        passwordLabel = tkinter.Label(self,text="Password").grid(row=1, column=0)  
        password = tkinter.StringVar()
        passwordEntry = tkinter.Entry(self, textvariable=password, show='*').grid(row=1, column=1)  


        #login button
        loginButton = tkinter.Button(self, text="Login", command=lambda a = username: [controller.show_frame("ChatRoomSelectPage"),ClientObject.send_message_into_ChatRoom(a)]).grid(row=4, column=0)  

        

class ChatRoomSelectPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller

        #username label and text entry box
        ChatRoomName = tkinter.Label(self, text="Chat Room Name").grid(row=0, column=0)
        ChatRoomName = tkinter.StringVar()
        ChatRoomNameEntry = tkinter.Entry(self, textvariable=ChatRoomName).grid(row=0, column=1)  

        #Enter button
        EnterButton = tkinter.Button(self, text="Enter", command=lambda a = ChatRoomName: [controller.show_frame("ChatRoomPage"),ClientObject.send_message_into_ChatRoom(a)]).grid(row=4, column=0)


class ChatRoomPage(tkinter.Frame):
    def __init__(self, parent, controller):
        global msg_list
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        
        my_msg = tkinter.StringVar()  # For the messages to be sent.
        my_msg.set("Type your messages here.")
        
        scrollbar = tkinter.Scrollbar(self)  # To navigate through past messages.
        # Following will contain the messages.
        msg_list = tkinter.Listbox(self, height=15, width=50, yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        msg_list.pack()

        entry_field = tkinter.Entry(self, textvariable=my_msg)
        entry_field.bind("<Return>",lambda event, temp = my_msg : ClientObject.send_message_into_ChatRoom(temp))
        entry_field.pack()
        send_button = tkinter.Button(self, text="Send", command= lambda :ClientObject.send_message_into_ChatRoom(my_msg))
        send_button.pack()
        
        

if __name__ == "__main__":
    
    ClientObject = ChatClient()
    app = ClientApp(ClientObject)
    
    receive_thread = Thread(target=ClientObject.receive)
    receive_thread.start()
    
    app.mainloop()

    
    

    
