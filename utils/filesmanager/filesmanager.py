import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import zipfile


class FilesManager:
    def __init__(self):
        return

    def transfer_contents(self, src: str, dst: str):
        """
        will go through every item in the src directory and recursivly copy all of its contents to the
        dst directory
        """

        try:
            src_contents = os.listdir(src)
            for item in src_contents:
                if "." in item:
                    shutil.copy(f"{src}/{item}", dst)
                else:
                    try:
                        shutil.copytree(
                            f"{src}/{item}", f"{dst}/{item}", dirs_exist_ok=True
                        )
                    except NotADirectoryError:
                        shutil.copy(f"{src}/{item}", dst)
            return 0

        except Exception as e:
            print(e)
            return 1

    def clean_dir(self, src: str):
        """
        Removes all contents from dir directory
        """
        try:
            dir_contents = os.listdir(src)
            for item in dir_contents:
                if "." in item:
                    os.remove(f"{src}/{item}")
                else:
                    os.system(f"rm -rf {src}/{item}")
            return 0

        except Exception as e:
            print(e)
            return 1

    def download_zip(
        self, url: str, css_selector: str, save_location: str, file_name: str
    ):
        """
        Use selenium to get the element from the given url with selector and save the
        file to save_location with file_name
        """
        driver = webdriver.Chrome()

        driver.get(url)

        try:
            element = driver.find_element(By.CSS_SELECTOR, css_selector)

            # print(element.get_attribute("href"))

            file_url = element.get_attribute("href")

            req = requests.get(file_url, timeout=None, allow_redirects=True)

            with open(f"{save_location}/{file_name}.zip", "wb") as server_files:
                server_files.write(req.content)

            driver.quit()

            return 0

        except:
            print("Element not found.")
            driver.quit()

            return 1

        # Close the browser when done

    def unzip_file(self, file_dir: str, zip_file: str, extract_dir: str):
        """
        Unzips file at location: zip_file to directory: extract_dir
        """
        try:
            with zipfile.ZipFile(f"{file_dir}/{zip_file}.zip", "r") as zip_file:
                zip_file.extractall(extract_dir)

            return 0

        except:
            return 1
