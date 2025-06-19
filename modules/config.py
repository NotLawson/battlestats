# Configuration loader for the application.
# This reads the configuration file and loads the settings into the application.
import os
import json

class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """
        Load the configuration file.
        :return: The configuration as a dictionary.
        """
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Configuration file {self.config_file} not found.")
        
        with open(self.config_file, 'r') as f:
            return json.load(f)
        
        if not self.check_config():
            raise ValueError("Configuration file is invalid.")
    
    def check_config(self):
        """
        Check if the configuration file is valid.
        :return: True if the configuration file is valid, False otherwise.
        """
        required_keys = ['postgres', 'init_runner_scale', 'secret_key', 'port']
        for key in required_keys:
            if key not in self.config:
                return False
        return True

    def get(self, key, default=None):
        """
        Get a value from the configuration.
        :param key: The key to get the value for.
        :param default: The default value to return if the key is not found.
        :return: The value for the key, or the default value if the key is not found.
        """
        return self.config.get(key, default)