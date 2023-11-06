from threading import current_thread
from utils.filesmanager.filesmanager import FilesManager
from utils.termmanager.termmanager import TermManager
import time

# Replace 'your_url_here' with the URL of the webpage you want to scrape
url = "https://www.minecraft.net/en-us/download/server/bedrock"

# Replace 'your_data_platform_value_here' with the value of the data-platform attribute you want to target
data_platform_value = "serverBedrockLinux"
selector = f'a[data-platform="{data_platform_value}"]'
# Set up the Selenium WebDriver (assuming you have it installed and the proper driver for your browser)

MESSAGE_PREFIX = "title @a actionbar"


class ServerManager:
    def __init__(self):
        self.term_manager = TermManager()
        self.files_manager = FilesManager()
        self.is_server_running: bool = False
        self.is_server_busy: bool = False
        self.server_properties = {}
        self.get_properties()

    def __countdown(self, count: int, message: str):
        self.term_manager.send(f"{MESSAGE_PREFIX} {message} in {count}")
        time.sleep(1)

        if count <= 0:
            return

        return self.__countdown(count - 1, message)

    def start_server(self):
        try:
            if self.term_manager.is_term_active:
                self.term_manager.send("sh start_server.sh")
            else:
                self.term_manager.start_process("sh start_server.sh")

            self.is_server_running = True
            return 0
        except:
            self.start_server()
            return 1

    def stop_server(self):
        try:
            self.is_server_running = False
            self.__countdown(10, "Stopping server...")
            self.term_manager.send("stop")
            self.term_manager.stop_process()

            return 0
        except:
            return 1

    def restart_server(self):
        self.is_server_busy = True
        self.__countdown(10, "Restarting server...")
        self.term_manager.send("stop")
        self.term_manager.stop_process()
        self.term_manager.start_process("sh start_server.sh")
        self.is_server_busy = False

    def install_server(self):
        """
        Download server files to temp directory and move the server files into the main directory
        """
        # download and unzip the server files
        temp_dir = "temp"
        zip_file = "temp-server"
        self.files_manager.download_zip(url, selector, temp_dir, zip_file)
        self.files_manager.unzip_file(temp_dir, zip_file, f"{temp_dir}/temp-server")
        # move the files into the main directory
        transfer_res = self.files_manager.transfer_contents(
            f"{temp_dir}/temp-server", "bedrock-server"
        )
        # clean up the temp folder
        clean_res = self.files_manager.clean_dir(temp_dir)

        print(f"clean res = {clean_res}, transfer res = {transfer_res}")

    def apply_persistence(self):
        persistent_dir = "persistent"
        self.files_manager.transfer_contents(f"{persistent_dir}", "bedrock-server")

    def update_settings(self, settings: list):
        """
        overwrites settings file with the
        """

        with open("bedrock-server/server.properties", "w") as properties:
            properties.writelines(settings)

    def update_server(self):
        self.is_server_busy = True
        self.__countdown(10, "Updating server...")
        self.stop_server()
        self.install_server()
        self.apply_persistence()
        self.start_server()
        self.is_server_busy = False

    def get_properties(self):
        """
        Retrieve and return properties if available
        """
        server_properties = {}
        try:
            with open("bedrock-server/server.properties", "r") as server_props:
                for line in server_props.readlines():
                    if "=" in line:
                        clean_line = line.strip().strip("\n").split("=")
                        server_properties[clean_line[0]] = clean_line[1]

            self.server_properties = server_properties
            return 0

        except Exception as e:
            print(e)
            return 1

    def apply_properties(self):
        """
        Apply properties to server.properties
        """
        try:
            with open("bedrock-server/server.properties", "w") as server_properties:
                for key in self.server_properties.keys():
                    server_properties.write(f"{key}={self.server_properties[key]}\n")
            return 0

        except Exception as e:
            print(e)
            return 1

    def set_level(self, level_name: str):
        """
        Sets the world_name property locally, then applies changes
        """
        self.__countdown(5, "Server is changing levels...")
        self.stop_server()
        self.server_properties["level-name"] = level_name
        self.apply_properties()
        self.start_server()

    def get_levels(self):
        return self.files_manager.get_folders("bedrock-server/worlds")

    def get_current_level(self):
        return self.server_properties["level-name"]

    def upload_level(self, file, filename: str):
        try:
            # with open(f"temp/{filename}", "wb") as zip_upload:
            #     zip_upload.write(file.read())

            file_name = filename.split(".zip")[0]

            self.files_manager.unzip_file("temp", file_name, f"temp/{file_name}")

            self.files_manager.transfer_folder(
                f"temp/{file_name}", f"bedrock-server/worlds/{file_name}"
            )

            self.files_manager.clean_dir("temp")

            return 0
        except:
            return 1
