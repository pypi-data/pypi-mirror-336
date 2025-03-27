import os
import sys
import platform
import subprocess
import shutil
import requests
import zipfile
import tempfile

class TerraformInstaller:
    TERRAFORM_VERSION = "1.7.5"
    BASE_URL = f"https://releases.hashicorp.com/terraform/{TERRAFORM_VERSION}"

    @classmethod
    def get_download_url(cls):
        """Generate download URL based on system"""
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        # Normalize architecture
        if machine in ['x86_64', 'amd64']:
            arch = 'amd64'
        elif machine in ['arm64', 'aarch64']:
            arch = 'arm64'
        else:
            arch = machine
        
        # URL mapping
        url_map = {
            ('darwin', 'amd64'): f"{cls.BASE_URL}/terraform_{cls.TERRAFORM_VERSION}_darwin_amd64.zip",
            ('darwin', 'arm64'): f"{cls.BASE_URL}/terraform_{cls.TERRAFORM_VERSION}_darwin_arm64.zip",
            ('linux', 'amd64'): f"{cls.BASE_URL}/terraform_{cls.TERRAFORM_VERSION}_linux_amd64.zip",
            ('linux', 'arm64'): f"{cls.BASE_URL}/terraform_{cls.TERRAFORM_VERSION}_linux_arm64.zip",
            ('windows', 'amd64'): f"{cls.BASE_URL}/terraform_{cls.TERRAFORM_VERSION}_windows_amd64.zip",
        }
        
        key = (system, arch)
        if key not in url_map:
            raise ValueError(f"No Terraform download available for {system} {arch}")
        
        return url_map[key]

    @classmethod
    def install_via_brew(cls):
        """Install Terraform using Homebrew on macOS"""
        try:
            subprocess.run(["brew", "install", "terraform"], check=True)
            print("Terraform installed successfully via Homebrew!")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Homebrew installation failed.")
            return False

    @classmethod
    def install_via_apt(cls):
        """Install Terraform using APT on Linux"""
        try:
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "terraform"], check=True)
            print("Terraform installed successfully via APT!")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("APT installation failed.")
            return False

    @classmethod
    def manual_download_install(cls):
        """Manually download and install Terraform"""
        try:
            # Get download URL
            url = cls.get_download_url()
            
            # Create temporary directory
            with tempfile.TemporaryDirectory() as tmpdir:
                # Download Terraform
                zip_path = os.path.join(tmpdir, "terraform.zip")
                print(f"Downloading Terraform from {url}...")
                
                # Download file
                response = requests.get(url, stream=True)
                with open(zip_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Extract to a suitable location
                system = platform.system().lower()
                if system == 'darwin':
                    extract_path = "/usr/local/bin"
                    os.makedirs(extract_path, exist_ok=True)
                elif system == 'linux':
                    extract_path = "/usr/local/bin"
                    os.makedirs(extract_path, exist_ok=True)
                else:
                    # Windows or other systems
                    extract_path = os.path.join(os.path.expanduser("~"), "terraform")
                    os.makedirs(extract_path, exist_ok=True)
                
                # Extract zip
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                
                # Make executable (for Unix-like systems)
                if system in ['darwin', 'linux']:
                    terraform_path = os.path.join(extract_path, "terraform")
                    subprocess.run(["chmod", "+x", terraform_path], check=True)
                
                print(f"Terraform manually installed to {extract_path}")
                return True
        except Exception as e:
            print(f"Manual installation failed: {e}")
            return False

    @classmethod
    def verify_installation(cls):
        """Verify Terraform installation"""
        try:
            result = subprocess.run(
                ["terraform", "version"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            print("Terraform installation verified:")
            print(result.stdout)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Terraform is not accessible in PATH")
            return False

    @classmethod
    def install(cls):
        """Main installation method"""
        system = platform.system().lower()
        
        # Installation methods by system
        install_methods = {
            'darwin': [cls.install_via_brew, cls.manual_download_install],
            'linux': [cls.install_via_apt, cls.manual_download_install],
            'windows': [cls.manual_download_install]
        }
        
        # Try methods for current system
        methods = install_methods.get(system, [cls.manual_download_install])
        
        for method in methods:
            if method():
                if cls.verify_installation():
                    return True
        
        print(f"Failed to install Terraform on {system}")
        return False

def main():
    """Main entry point for pip-terraform"""
    print("Installing Terraform...")
    success = TerraformInstaller.install()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()