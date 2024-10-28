import socket
import audio_manager

def command_listener():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 65432))
        s.listen()
        print("Birb Bot listening for commands...")

        while True:
            conn, addr = s.accept()
            with conn:
                command = conn.recv(1024).decode()
                print("Received command:", command)

                # Process command
                if command.startswith("!simon"):
                    _, sound = command.split()
                    audio_manager.play_audio_file(sound, 2)
                elif command == "!reward":
                    # Trigger treat dispenser here
                    print("Dispensing treat...")

# Start the command listener in a separate thread or as part of the main bot loop
command_listener()
