import base64
import requests
import zipfile
import subprocess
import sys
from tempfile import TemporaryDirectory
from pathlib import Path
from concrete.ml.deployment import FHEModelClient


class BlindML:
    def __init__(self):
        self.api_key = None
        self.server_url = None
        self.fhemodel_client = None
        self.evaluation_keys = None
        self.python_version = None
        self.concrete_ml_version = None
        self.venv_path = None

    def _create_virtualenv(self, python_version: str, concrete_ml_version: str):
        """
        Create a virtual environment with the specified Python version and install concrete-ml.
        """
        with TemporaryDirectory() as temp_dir:
            self.venv_path = Path(temp_dir) / "venv"

            # Create a virtual environment
            subprocess.check_call([sys.executable, "-m", "venv", str(self.venv_path)])

            # Install the required version of concrete-ml
            pip_path = self.venv_path / "bin" / "pip"
            subprocess.check_call([str(pip_path), "install", f"concrete-ml=={concrete_ml_version}"])

    def _run_in_venv(self, script: str):
        """
        Execute a script within the virtual environment.
        """
        python_path = self.venv_path / "bin" / "python"
        result = subprocess.run([str(python_path), "-c", script], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Error running script in virtual environment: {result.stderr}")
        return result.stdout


    def init(self, server_url: str, api_key: str):
        """
        Initialize the BlindML client by downloading and setting up FHE model client.
        """
        self.server_url = server_url
        self.api_key = api_key

        try:
            # Send request to server to get client.zip or JSON
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.post(f"{server_url}/init", headers=headers, stream=True)
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "")

            if "application/json" in content_type:
                # Handle JSON response
                response_json = response.json()
                print("Received JSON response:", response_json)
                # Perform JSON-specific handling (if needed)
                return response_json

            elif "application/zip" in content_type:
                # Handle ZIP file response
                with TemporaryDirectory() as temp_dir:
                    zip_path = Path(temp_dir) / "client.zip"

                    # Save ZIP file
                    with open(zip_path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    print("client.zip file saved at:", zip_path)

                    # Extract ZIP file
                    with zipfile.ZipFile(zip_path, "r") as zf:
                        zf.extractall(temp_dir)
                        print("ZIP file contents:", zf.namelist())

                    # Initialize the FHE model client
                    self.fhemodel_client = FHEModelClient(str(temp_dir), key_dir=str(temp_dir))
                    print("FHE Model Client initialized successfully.")


                    return "client.zip file processed successfully"

            else:
                raise RuntimeError(f"Unexpected Content-Type: {content_type}")

        except requests.RequestException as e:
            print(f"Error initializing BlindML: {e}")
            raise RuntimeError("Failed to initialize the client.") from e


    def makekey(self) -> bytes:
        """
        Generate and return serialized evaluation keys.
        """
        if not self.fhemodel_client:
            raise RuntimeError("Client not initialized. Call init() first.")

        self.evaluation_keys  = self.fhemodel_client.get_serialized_evaluation_keys();

        return self.evaluation_keys

    def encrypt(self, input_data) -> bytes:
        """
        Quantize, encrypt, and serialize input data.
        """
        if not self.fhemodel_client:
            raise RuntimeError("Client not initialized. Call init() first.")
        return self.fhemodel_client.quantize_encrypt_serialize(input_data)

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

                # Read the file content to send as a binary payload
                with open(ekl_path, "rb") as f:
                    ekl_file_content = f.read()

                # Prepare multipart form-data payload
                files = {
                    "EncryptedData": ("encrypted_data.bin", base64.b64encode(encrypted_data)),
                    # Encrypted data as binary
                    "EvaluationKey": ("serialized_evaluation_keys.ekl", ekl_file_content),  # Evaluation key file
                }

                headers = {"Authorization": f"Bearer {self.api_key}"}

                # Send the request
                response = requests.post(f"{self.server_url}/predict", files=files, headers=headers)
                response.raise_for_status()

            # Parse JSON response and decode base64
            result = response.json()
            if "data" not in result:
                raise RuntimeError("Invalid response format: 'data' key missing.")

            base64_encoded_result = result["data"]
            return base64.b64decode(base64_encoded_result)
        except requests.RequestException as e:
            print(f"Error during prediction: {e}")
            raise

    def decrypt(self, result_data: bytes):
        """
        Deserialize, decrypt, and dequantize the prediction result.
        """
        if not self.fhemodel_client:
            raise RuntimeError("Client not initialized. Call init() first.")
        return self.fhemodel_client.deserialize_decrypt_dequantize(result_data)[0]