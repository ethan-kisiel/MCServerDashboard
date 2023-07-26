from utils.termmanager.termmanager import TermManager

term_manager = TermManager()


try:
    if term_manager.start_process("sh bedrock-server/start_server.sh"):
        print("Something went wrong")
    else:
        print("exited with code: 0")

    term_manager.send("hello")
    term_manager.send("stop")
except Exception as e:
    print(f"Failed {e}")
