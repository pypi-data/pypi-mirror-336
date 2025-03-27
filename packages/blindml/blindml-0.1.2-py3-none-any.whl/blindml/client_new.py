import os
import base64
import requests
import zipfile
import subprocess
import shutil
import sys
from tempfile import TemporaryDirectory
from pathlib import Path


class BlindML:
    def __init__(self):
        self.api_key = None
        self.server_url = None
        self.fhemodel_client = None
        self.evaluation_keys = None
        self.python_version = None
        self.concrete_ml_version = None
        self.venv_path = None

    def _get_base_dir(self) -> Path:
        """
        Determine the base directory for creating virtual environments.
        """
        if os.name == "nt":  # Windows
            base_dir = Path(os.getenv("LOCALAPPDATA", "C:\\app"))
        elif os.name == "posix":  # Linux/Mac
            base_dir = Path(os.getenv("HOME", "/tmp")) / "app"
        else:
            raise RuntimeError(f"Unsupported OS: {os.name}")

        base_dir.mkdir(parents=True, exist_ok=True)
        return base_dir

    def _install_python_version(self, python_version: str) -> str:
        """
        Install the specified Python version using pyenv.
        """
        if shutil.which("pyenv") is None:
            raise RuntimeError("pyenv is not installed. Please install pyenv first.")

        try:
            print(f"Installing Python {python_version} using pyenv...")
            subprocess.run(["pyenv", "install", "-s", python_version], check=True)
            subprocess.run(["pyenv", "rehash"], check=True)

            python_executable = shutil.which(f"python{python_version}")
            if not python_executable:
                subprocess.run(["pyenv", "global", python_version], check=True)
                python_executable = shutil.which("python")

            if not python_executable:
                raise RuntimeError(f"Failed to find Python {python_version} after installation.")
            print(f"Python {python_version} installed successfully.")
            return python_executable
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to install Python {python_version} using pyenv: {e}")

    def _create_virtualenv(self, python_version: str, library_name: str, library_version: str) -> str:
        """
        Create a virtual environment for the specified Python version and library.
        """
        base_dir = self._get_base_dir()
        venv_dir = base_dir / "venvs" / f"venv_py{python_version}_{library_name}{library_version}"

        # Use pyenv-installed Python if needed
        python_executable = shutil.which(f"python{python_version}")
        if not python_executable:
            print(f"Python {python_version} not found. Attempting to install...")
            self._install_python_version(python_version)
            # Explicitly get the pyenv path for the installed version
            python_executable = f"{os.getenv('HOME')}/.pyenv/versions/{python_version}/bin/python3.8"

        try:
            # Ensure the Python executable is available
            if not Path(python_executable).exists():
                raise RuntimeError(f"Python executable {python_executable} not found after installation.")

            print(f"Creating virtual environment at {venv_dir}...")
            subprocess.run([python_executable, "-m", "venv", str(venv_dir)], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to create virtual environment: {e}")

        self.venv_path = venv_dir
        venv_python = venv_dir / "bin" / "python" if os.name != "nt" else venv_dir / "Scripts" / "python.exe"

        try:
            subprocess.run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"], check=True)
            subprocess.run([str(venv_python), "-m", "pip", "install", f"{library_name}=={library_version}"], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to install {library_name}=={library_version}: {e}")

        print(f"Virtual environment created at {venv_dir}.")
        return str(venv_python)

    def init(self, server_url: str, api_key: str):
        """
        Initialize the BlindML client by setting up the environment and client.
        """
        self.server_url = server_url
        self.api_key = api_key

        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.post(f"{server_url}/init", headers=headers, stream=True)
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "")

            self.python_version = response.headers.get("X-Python-Version", "3.8")
            self.library_name = response.headers.get("X-Library-Name", "concrete-ml")
            self.library_version = response.headers.get("X-Library-Version", "1.4.0")

            if self.library_name == "concrete-ml":
                self._create_virtualenv(self.python_version, self.library_name, self.library_version)

                if "application/json" in content_type:
                    return response.json()
                elif "application/zip" in content_type:
                    with TemporaryDirectory() as temp_dir:
                        zip_path = Path(temp_dir) / "client.zip"
                        with open(zip_path, "wb") as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        with zipfile.ZipFile(zip_path, "r") as zf:
                            zf.extractall(temp_dir)
                    print("Client setup complete.")
                    return "client.zip file processed successfully"
                else:
                    raise RuntimeError(f"Unexpected Content-Type: {content_type}")

        except requests.RequestException as e:
            raise RuntimeError("Failed to initialize the client.") from e

    def makekey(self) -> bytes:
        """
        Generate and return serialized evaluation keys.
        """
        script = """
        evaluation_keys = fhemodel_client.get_serialized_evaluation_keys()
        print(evaluation_keys)
        """
        return self._run_in_venv(script)

    def encrypt(self, input_data) -> bytes:
        """
        Quantize, encrypt, and serialize input data.
        """
        script = f"""
        encrypted_data = fhemodel_client.quantize_encrypt_serialize({input_data})
        print(encrypted_data)
        """
        return self._run_in_venv(script)

    def predict(self, encrypted_data: bytes) -> bytes:
        """
        Send encrypted data and evaluation key file to the server for prediction and retrieve results.
        """
        if not self.server_url or not self.api_key:
            raise RuntimeError("Client not initialized. Call init() first.")
        if not self.evaluation_keys:
            self.makekey()

        try:
            # Save the evaluation keys to a temporary .ekl file
            with TemporaryDirectory() as temp_dir:
                ekl_path = Path(temp_dir) / "serialized_evaluation_keys.ekl"
                with open(ekl_path, "wb") as f:
                    f.write(self.evaluation_keys)

                files = {
                    "EncryptedData": ("encrypted_data.bin", base64.b64encode(encrypted_data)),
                    "EvaluationKey": ("serialized_evaluation_keys.ekl", ekl_path.read_bytes()),
                }

                headers = {"Authorization": f"Bearer {self.api_key}"}
                response = requests.post(f"{self.server_url}/predict", files=files, headers=headers)
                response.raise_for_status()

            result = response.json()
            base64_encoded_result = result.get("data")
            if not base64_encoded_result:
                raise RuntimeError("Invalid response format: 'data' key missing.")

            return base64.b64decode(base64_encoded_result)
        except requests.RequestException as e:
            raise RuntimeError("Error during prediction.") from e

    def decrypt(self, result_data: bytes):
        """
        Deserialize, decrypt, and dequantize the prediction result.
        """
        script = f"""
        result = fhemodel_client.deserialize_decrypt_dequantize({result_data})[0]
        print(result)
        """
        return self._run_in_venv(script)
