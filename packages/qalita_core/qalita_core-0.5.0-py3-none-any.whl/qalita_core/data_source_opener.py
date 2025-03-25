"""
# QALITA (c) COPYRIGHT 2025 - ALL RIGHTS RESERVED -
"""

import os
import glob
from venv import logger
import pandas as pd
from sqlalchemy import create_engine


class DataSourceOpener:
    """
    The DataSourceOpener class contains methods to load data from files and databases.
    """

    DEFAULT_PORTS = {
        "5432": "postgresql",
        "3306": "mysql",
        "1433": "mssql+pymssql",
    }

    def load_data(self, source_config, pack_config):
        source_type = source_config.get("type")
        if source_type == "file":
            path = source_config.get("config", {}).get("path")
            return self.load_data_from_file(path, pack_config)
        if source_type == "database":
            engine = self.create_db_connection(source_config["config"])
            return self.load_data_from_db(engine)
        raise ValueError(
            "Unsupported source type. Only 'file' and 'database' are supported."
        )

    @staticmethod
    def load_data_from_db(engine):
        with engine.connect() as connection:
            connection.execute("SELECT 1")
            if not (tables := engine.table_names()):
                raise ValueError("No tables found in the database.")
            dataframes = {table: pd.read_sql_table(table, engine) for table in tables}
            return dataframes

    @classmethod
    def create_db_connection(cls, config):
        if (
            db_type := config.get("type")
            or cls.DEFAULT_PORTS.get(config["port"], "unknown")
        ) == "unknown":
            raise ValueError(f"Unsupported or unknown database port: {config['port']}")

        engine = create_engine(
            f"{db_type}://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
        )
        return engine

    def load_data_from_file(self, path, pack_config):
        if os.path.isfile(path):
            return self.load_data_file(path, pack_config)
        if os.path.isdir(path):
            data_files = glob.glob(os.path.join(path, "*.csv")) + glob.glob(
                os.path.join(path, "*.xlsx")
            )
            if not data_files:
                raise FileNotFoundError(
                    "No CSV or XLSX files found in the provided path."
                )
            return self.load_data_file(data_files[0], pack_config)
        raise FileNotFoundError(
            f"The path {path} is neither a file nor a directory, or it can't be reached."
        )

    @staticmethod
    def load_data_file(file_path, pack_config):
        logger.info("Loading file data from: %s", file_path)
        if (
            skiprows := pack_config.get("job", {}).get("source", {}).get("skiprows", 0)
        ) is not None:
            if file_path.endswith(".csv"):
                return pd.read_csv(
                    file_path,
                    low_memory=False,
                    memory_map=True,
                    skiprows=int(skiprows),
                    on_bad_lines="warn",
                    encoding="utf-8",
                )
            if file_path.endswith(".xlsx"):
                return pd.read_excel(
                    file_path,
                    engine="openpyxl",
                    skiprows=int(skiprows),
                )

        raise ValueError(
            f"Unsupported file extension or missing 'skiprows' for file: {file_path}"
        )
