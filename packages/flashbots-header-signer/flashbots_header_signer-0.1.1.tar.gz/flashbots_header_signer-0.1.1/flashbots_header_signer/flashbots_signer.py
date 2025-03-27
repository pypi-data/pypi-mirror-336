import os
import json
import importlib.metadata
import aiohttp
import logging
from web3 import Web3
from eth_account import Account, messages
from typing import Dict, Optional, Union

class FlashbotsHeaderSigner:
    def __init__(self, private_key: Optional[str] = None, log_level: str = "WARNING") -> None:
        """
        Initializes the FlashbotsHeaderSigner with the provided private key or from the environment variable.
        Also initializes the logger with the specified log level.

        Parameters:
        - private_key (str): The private key to use for signing. If not provided, 
                              it will attempt to get it from the environment variable 'FLASHBOT_PRIVATE_KEY'.
        - log_level (str): The logging level for the logger. Default is "WARNING". 
                           Other options: "DEBUG", "INFO", "ERROR", "CRITICAL".
        """
        # Initialize the logger with the specified log level
        self._initialize_logger(log_level)

        if private_key is None:
            raise ValueError("Error: The variable 'FLASHBOT_PRIVATE_KEY' is not set!")

        if not isinstance(private_key, str):
            raise TypeError("url must be a string")
        
        if private_key.startswith("0x"):
            private_key = private_key[2:]

        if len(private_key) != 64:
            raise ValueError(f"Error: The private key must be 64 characters long! Len of private_key {len(private_key)}")

        if private_key:
            self._private_key = private_key
        
        self._account = Account.from_key(self._private_key)
        self._w3 = Web3()

        # Check Web3 version
        try:
            self._web3_version = importlib.metadata.version("web3")
        except importlib.metadata.PackageNotFoundError:
            raise RuntimeError("Web3 is not installed! Please install it via 'pip install web3'")

        self.logger.info(f"Using Web3 version: {self._web3_version}")

    def _initialize_logger(self, log_level: str) -> None:
        """
        Initializes the logger with the given log level.

        Parameters:
        - log_level (str): The logging level to set. E.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.
        """
        # Set up the logger
        if log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError(f"Invalid log level: {log_level}. Valid options are: DEBUG, INFO, WARNING, ERROR, CRITICAL")
            
        self.logger = logging.getLogger(__name__)

        if not self.logger.hasHandlers():
            level_map = {
                "DEBUG": logging.DEBUG,
                "INFO": logging.INFO,
                "WARNING": logging.WARNING,
                "ERROR": logging.ERROR,
                "CRITICAL": logging.CRITICAL,
            }

            # Default to WARNING if an invalid level is passed
            self.logger.setLevel(level_map.get(log_level.upper(), logging.WARNING))

            # Set up console handler and formatter
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.logger.level)  # Use the level set above
            formatter = logging.Formatter("%(asctime)s [%(levelname)s] Line: %(lineno)d - %(message)s")
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        else:
            self.logger.debug("Logger already initialized, skipping re-initialization.")

    def _sign_flashbots(self, tx_body: str, version: str) -> str:
        """
        Signs a transaction based on Web3 version and returns the signature.
        
        Parameters:
        - tx_body (str): The transaction body to be signed.
        - version (str): The Web3 version (e.g., '6' or '7').

        Returns:
        - str: The signed transaction in the format 'address:signature'.
        """
        try:
            if version == '6':
                keccak_res = self._w3.keccak(text=tx_body)
                keccak_res_hex = keccak_res.hex()
            elif version == '7':
                keccak_res_hex = "0x" + self._w3.keccak(text=tx_body).hex()
            else:
                raise ValueError(f"Unsupported Web3 version: {version}")

            self.logger.debug(f"keccak_res: {keccak_res_hex}")

            message = messages.encode_defunct(text=keccak_res_hex)
            self.logger.debug(f"SignableMessage: {message}")

            if version == '6':
                signature = f'{self._account.address}:{self._w3.eth.account.sign_message(message, self._private_key).signature.hex()}'
            elif version == '7':
                signature = f'{self._account.address}:0x{self._w3.eth.account.sign_message(message, self._private_key).signature.hex()}'
            
            self.logger.debug(f"Signature: {signature}")
            return signature
        except ValueError as e:
            self.logger.error(f"Error signing transaction: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during signing: {e}")
            raise

    def generate_flashbots_header(self, tx_body: str) -> Dict[str, str]:
        """
        Generates the complete header for Flashbots requests, including the signature.

        Parameters:
        - tx_body (str): The transaction body to be signed.

        Returns:
        - dict: The complete headers to send in your Flashbots HTTP request.
        """
        if tx_body is None:
            raise ValueError("tx_body cannot be None")

        if not isinstance(tx_body, str):
            raise TypeError(f"tx_body must be a string. tx_body is {type(tx_body)}")
         
        # Check for empty or invalid tx_body
        if not tx_body.strip():  # Check if the string is empty or contains only spaces
            raise ValueError("tx_body cannot be empty or just whitespace.")

        try:
            major_version = int(self._web3_version.split('.')[0])
        except ValueError:
            raise ValueError(f"Invalid Web3 version: {self._web3_version}")

        if major_version == 6:
            signature = self._sign_flashbots(tx_body, version='6')
        elif major_version == 7:
            signature = self._sign_flashbots(tx_body, version='7')
        else:
            raise RuntimeError(f"Unsupported Web3 version: {self._web3_version}")

        headers = {
            "Content-Type": "application/json",
            "X-Flashbots-Signature": signature,
        }

        return headers
    
    async def send_request(self, url: str, headers_json: Union[dict, str], tx_body: str):
        """
        Sends an asynchronous HTTP POST request to the given URL with the specified headers and body.

        Parameters:
        - url (str): The URL to send the POST request to.
        - headers_json (Optional[dict, str]): The headers for the request.
        - tx_body (str): The transaction body to be sent in the POST request.
        
        Returns:
        - dict: The response from the Flashbots API.
        """
        try:
            if not isinstance(tx_body, str):
                raise TypeError(f"tx_body must be a string. tx_body is {type(tx_body)}")

            tx_body = json.loads(tx_body)

            if not isinstance(url, str):
                raise TypeError("url must be a string")

            if headers_json is None:
                    raise TypeError("headers_json must not be None")

            if not isinstance(headers_json, (dict, str)):
                raise TypeError("headers_json must be a dictionary or a string")
            
            # If headers_json is a string, convert it to a dictionary
            if isinstance(headers_json, str):
                try:
                    headers_json = json.loads(headers_json)
                except json.JSONDecodeError:
                    raise TypeError("headers_json must be a valid JSON string")
            
            if isinstance(headers_json, dict):
                if not all(isinstance(k, str) and isinstance(v, str) for k, v in headers_json.items()):
                    raise TypeError("All keys and values in headers_json must be strings")
            else:
                raise TypeError("headers_json must be a dictionary")

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers_json, json=tx_body) as response:
                        response_data = await response.json()

                        if response.status == 200:
                            self.logger.info("Flashbots request sent successfully")
                        else:
                            self.logger.warning(f"Failed. Status code: {response.status}")
                        
                        self.logger.debug(f"Response: {response_data}")
                        return response_data
            except aiohttp.ClientError as e:
                self.logger.error(f"HTTP error occurred: {e}")
                raise
            except Exception as e:
                self.logger.error(f"Unexpected error occurred: {e}")
                raise
        
        except aiohttp.ClientError as e:
            self.logger.error(f"HTTP error occurred: {e}")
            raise
        except TypeError as e:
            self.logger.error(f"Type error occurred: {e}")
            raise
        except ValueError as e:
            self.logger.error(f"Value error occurred: {e}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error occurred: {e}")
            raise
        except RuntimeError as e:
            self.logger.error(f"Runtime error occurred: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error occurred: {e}")
            raise
        