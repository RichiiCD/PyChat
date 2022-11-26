import tkinter as tk
from .config import read_configuration_file


class Interface:
    ''' Interface parent class for the login and chat inherit '''

    def __init__(self, root):
        self.root = root
        self.config = self.set_configuration()
    
    # Display the Tk windows
    def display(self, title):
        self.root.title(title)
        self.root.resizable(False, False) 
        self.root.mainloop()
    
    # Read and set the configuration from JSON file
    def set_configuration(self):
        json_config = read_configuration_file()
        return json_config['interface']

    # Close the current Tk windows
    def close_tab(self):
        self.root.destroy()

    # Center the Tk window to screen
    def center_windows(self, width_divisor, height_divisor):
        windowWidth = self.root.winfo_reqwidth()
        windowHeight = self.root.winfo_reqheight()        

        positionRight = int(self.root.winfo_screenwidth()/width_divisor - windowWidth/2)
        positionDown = int(self.root.winfo_screenheight()/height_divisor - windowHeight/2)
        
        self.root.geometry("+{}+{}".format(positionRight, positionDown))


class ChatInterface(Interface):
    ''' Client chat application interface '''

    def __init__(self, root, room, on_close, send_message):
        super().__init__(root)
        self.center_windows(3, 4)

        # Create the textarea for display the received messages
        self.text = tk.Text(self.root)

        # Create the input for send messages 
        self.input = tk.Entry(self.root)
        
        self.root.protocol("WM_DELETE_WINDOW", on_close)
        self.root.bind('<Return>', send_message)
        self.send_message = send_message
        self.room = room
    
    # Display chat elements in the Tk windows
    def display(self):
        self.text.grid(row=1, column=0, columnspan=2)
        self.input.grid(row=2, column=0)

        tk.Scrollbar(self.text).place(relheight=1, relx=0.974)
        tk.Button(self.root, text="Send", font=self.config['font'], bg=self.config['bg_button'], command=self.send_message).grid(row=2, column=1)

        self.text.config(bg=self.config['bg_color'], fg=self.config['text_color'], font=self.config['font'], width=60)
        self.input.config(bg=self.config['bg_color'], fg=self.config['text_color'], font=self.config['font'], width=55)

        return super().display(f'Room {self.room}')
    
    # Display a recieved new messages
    def new_message(self, message):
        self.text.insert(tk.END, f"{message['username']} > {message['message']} \n")
        self.text.see(tk.END)

    # Get the input message value
    def get_input_value(self):
        value = self.input.get()
        self.input.delete(0, 'end')
        return value


class LoginInterface(Interface):
    ''' Client login chat application interface '''

    def __init__(self, root, start_chat):
        super().__init__(root)
        self.center_windows(2, 2)

        # Create the input for username
        self.username_input = tk.Entry(self.root)

        # Create the input for room
        self.room_input = tk.Entry(self.root)

        self.root.bind('<Return>', start_chat)
        self.start_chat = start_chat

    # Display login elements in the Tk windows
    def display(self):
        tk.Label(self.root, text="Username").grid(row=0, column=0)
        self.username_input.grid(row=0, column=1)  

        tk.Label(self.root, text="Room").grid(row=1, column=0)  
        self.room_input.grid(row=1, column=1)  

        tk.Button(self.root, text="Login", command=self.start_chat).grid(row=4, column=0)  

        return super().display('Home')

    # Get the login form values
    def get_input_value(self):
        username = self.username_input.get()
        room = self.room_input.get()
        self.username_input.delete(0, 'end')
        self.room_input.delete(0, 'end')
        return {'username': username, 'room': room}

