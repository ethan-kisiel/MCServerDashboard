from utils.termmanager.termmanager import TermManager
from utils.filesmanager.filesmanager import FilesManager
from utils.serverutils import ServerManager

term_manager = TermManager()
server_manager = ServerManager()

# try:
#     if term_manager.start_process("sh bedrock-server/start_server.sh"):
#         print("Something went wrong")
#     else:
#         print("exited with code: 0")

#     term_manager.send("hello")
#     term_manager.send("stop")
# except Exception as e:
#     print(f"Failed {e}")

try:
    server_manager = ServerManager()
    server_manager.install_server()
except:
    print("Failed to download/unzip file")
