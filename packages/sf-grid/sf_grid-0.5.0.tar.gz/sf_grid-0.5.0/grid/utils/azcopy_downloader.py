import subprocess
import shlex
import os

class AzCopyDownloader:
    def __init__(self, azcopy_path='~/.grid/utils/azcopy'):
        self.azcopy_path = azcopy_path
        self.azcopy_url = "https://aka.ms/downloadazcopy-v10-linux"  # Example URL for AzCopy download

    def ensure_azcopy_exists(self):
        """
        Ensures that AzCopy is downloaded and available at the specified path.
        """
        azcopy_full_path = os.path.expanduser(self.azcopy_path)
        if not os.path.exists(azcopy_full_path):
            print("AzCopy not found. Downloading...")
            # Make the folder if it does not exist
            os.makedirs(os.path.dirname(azcopy_full_path), exist_ok=True)
            try:
                # Download AzCopy
                subprocess.run(shlex.split("wget -q https://aka.ms/downloadazcopy-v10-linux"), check=True)
                # Expand Archive
                subprocess.run(shlex.split(f"tar --strip-components=1 -xvf downloadazcopy-v10-linux -C {os.path.dirname(azcopy_full_path)}"), check=True)
                # Change permissions of AzCopy
                subprocess.run(shlex.split(f"chmod 777 {azcopy_full_path}"), check=True)
                print("AzCopy downloaded and ready to use.")
                os.remove("downloadazcopy-v10-linux")

            except subprocess.CalledProcessError as e:
                print(f"Failed to download AzCopy: {e}")
            except Exception as e:
                print(f"Failed to download AzCopy: {e}")

    def download_asset(self, container_url: str, sas_token: str, destination_path: str, force_redownload: bool = False) -> bool:
        """
        Downloads a file from a specified Azure container using azcopy and a SAS token.

        :param container_url: The URL of the Azure container.
        :param sas_token: The SAS token for authentication.
        :param destination_path: The local path where the file should be downloaded.
        :param force_redownload: If True, force download and overwrite existing files.
        :return: True if download is successful, False otherwise.
        """

        if os.path.exists(destination_path) and not force_redownload:
            if os.path.isfile(destination_path):
                print("File already exists at destination. Skipping download.")
                return True
            elif os.path.isdir(destination_path) and not os.listdir(destination_path):
                print("Downloading...")
            else:
                return True
        self.ensure_azcopy_exists()

        try:
            # Construct the azcopy command
            command = f"{os.path.expanduser(self.azcopy_path)} copy '{container_url}?{sas_token}' '{destination_path}' --recursive"

            # Execute the command using subprocess.run
            result = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Check if the command was successful
            if result.returncode == 0:
                return True
            else:
                print(result.stdout)
                return False

        except Exception as e:
            print(f"An error occurred: {e}")
            return False
