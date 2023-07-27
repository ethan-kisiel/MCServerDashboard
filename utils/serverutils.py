from utils.filesmanager.filesmanager import FilesManager
from utils.termmanager.termmanager import TermManager

# Replace 'your_url_here' with the URL of the webpage you want to scrape
url = "https://www.minecraft.net/en-us/download/server/bedrock"

# Replace 'your_data_platform_value_here' with the value of the data-platform attribute you want to target
data_platform_value = "serverBedrockLinux"
selector = f'a[data-platform="{data_platform_value}"]'
# Set up the Selenium WebDriver (assuming you have it installed and the proper driver for your browser)


class ServerManager:
    def __init__(self):
        self.term_manager = TermManager()
        self.files_manager = FilesManager()
        pass

    def start_server(self):
        try:
            if self.term_manager.is_term_active:
                self.term_manager.send("sh bedrock-server/start_server.sh")
            else:
                self.term_manager.start_process("sh bedrock-server/start_server.sh")
            return 0
        except:
            return 1

    def stop_server(self):
        try:
            self.term_manager.send("stop")
            self.term_manager.stop_process()
            return 0
        except:
            return 1

    def restart_server(self):
        self.term_manager.send("stop")
        self.term_manager.stop_process()
        self.term_manager.start_process("sh bedrock-server/start_server.sh")

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

    def update_settings(self, settings: list):
        """
        overwrites settings file with the
        """

        with open("bedrock-server/server.properties", "w") as properties:
            properties.writelines(settings)

    def update_server(self):
        self.stop_server()
        self.install_server()
        self.start_server()
