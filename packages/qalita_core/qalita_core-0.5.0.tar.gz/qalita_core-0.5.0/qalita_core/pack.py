"""
# QALITA (c) COPYRIGHT 2025 - ALL RIGHTS RESERVED -
"""

import os
import json
import base64
import logging
from qalita_core.data_source_opener import DataSourceOpener


class Pack:
    """
    Represents a pack in the system, handling configurations and data loading.
    """

    # Default configuration paths
    default_configs = {
        "pack_conf": "pack_conf.json",
        "source_conf": "source_conf.json",
        "target_conf": "target_conf.json",
        "agent_file": "~/.qalita/.agent",
    }

    def __init__(self, configs=None):
        self.logger = logging.getLogger(self.__class__.__name__)

        if configs is None:
            configs = {}

        # Update default paths with any provided configurations
        self.config_paths = {**self.default_configs, **configs}
        self.pack_config = ConfigLoader.load_config(self.config_paths["pack_conf"])
        self.source_config = ConfigLoader.load_config(self.config_paths["source_conf"])
        self.target_config = ConfigLoader.load_config(self.config_paths["target_conf"])
        self.agent_config = self.load_agent_config(self.config_paths["agent_file"])
        self.metrics = PlatformAsset("metrics")
        self.recommendations = PlatformAsset("recommendations")
        self.schemas = PlatformAsset("schemas")

        # Validate configurations
        if not self.source_config:
            self.logger.error("Source configuration is empty.")
        elif "type" not in self.source_config:
            self.logger.error("Source configuration is missing the 'type' key.")

    def load_agent_config(self, agent_file_path):
        try:
            abs_agent_file_path = os.path.expanduser(
                agent_file_path
            )  # Resolve any user-relative paths
            with open(abs_agent_file_path, "r") as agent_file:
                encoded_content = agent_file.read()
                decoded_content = base64.b64decode(encoded_content).decode("utf-8")
                return json.loads(decoded_content)
        except Exception as e:
            self.logger.error(f"Error loading agent configuration: {e}")
            return {}

    def load_data(self, trigger):
        opener = DataSourceOpener()
        if trigger == "source":
            self.df_source = opener.load_data(self.source_config, self.pack_config)
            return self.df_source
        elif trigger == "target":
            self.df_target = opener.load_data(self.target_config, self.pack_config)
            return self.df_target


class ConfigLoader:
    """Utility class for loading configuration files."""

    @staticmethod
    def load_config(file_name):
        # logger = logging.getLogger("ConfigLoader")
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError as e:
            # logger.warning(f"Configuration file not found: {file_name}")
            return {}


class PlatformAsset:
    """
    A platform asset is a json formated data that can be pushed to the platform
    """

    def __init__(self, type):
        self.type = type
        self.data = []

    def save(self):
        # Writing data to metrics.json
        with open(self.type + ".json", "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)
