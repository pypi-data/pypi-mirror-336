import os
import subprocess
from grid.utils.azcopy_downloader import AzCopyDownloader
import shutil

class GRIDAssetDownloader:
    @staticmethod
    def download_sample_notebooks():
        samples_dir = os.path.join(os.path.expanduser("~"), ".grid", "samples")
        
        # Check if the directory already exists
        if not os.path.exists(samples_dir):
            # Create the directory
            os.makedirs(samples_dir)
            
            # Clone the repository into the samples directory
            repo_url = "https://github.com/scaledfoundations/grid-playground"
            subprocess.run(["git", "clone", "--depth", "1", "--branch", "new", repo_url, samples_dir], check=True)
            shutil.rmtree(os.path.join(samples_dir, ".git"))
        else:
            print(f"Samples currently at {samples_dir}")

    @staticmethod
    def download_model_weights(sas_token:str = ''):
        downloader = AzCopyDownloader()
        weights_dir = os.path.join(os.path.expanduser("~"), ".grid", "models")
        
        # Check if the directory already exists
        if not os.path.exists(weights_dir):
            # Create the directory
            os.makedirs(weights_dir)

        # Download the model weights
        downloader.download_asset("https://gridenterpriseresources.blob.core.windows.net/aimodelweights/weights", sas_token, weights_dir)
            

# Example usage
if __name__ == "__main__":
    GRIDAssetDownloader.download_sample_notebooks()