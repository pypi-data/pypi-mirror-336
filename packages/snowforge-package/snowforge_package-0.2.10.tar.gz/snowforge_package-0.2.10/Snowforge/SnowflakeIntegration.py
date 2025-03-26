import snowflake.connector as sf
from .Logging import Debug  # Import from same package
from .Config import Config  # Import from same package

class SnowflakeIntegration:
    """Handles establishing and managing connections to Snowflake."""

    DEFAULTS = {
        "snowflake_username": "snowflake username",
        "snowflake_account": "snowflake account"
    }
    
    _connection = None  # Instance variable

    @staticmethod
    def connect(user_name: str = DEFAULTS["snowflake_username"], account: str = DEFAULTS["snowflake_account"], profile: str = "default", verbose: bool = False) -> sf.connection:
        """Establishes a connection to Snowflake.

        Uses either a credentials file or manual login via username and account.

        Args:
            user_name (str, optional): The Snowflake username. Defaults to 'DEFAULTS["snowflake_username"]'.
            account (str, optional): The Snowflake account ID. Defaults to 'DEFAULTS["snowflake_account"]'.
            profile (str, optional): The Snowflake profile to use, must be defined in the 'snowforge_config.toml'. Defaults to 'default'.
            verbose (bool, optional): set True to enable DEBUG output. Defaults to False.

        Returns:
            sf.connection: A Snowflake account connection object.

        Raises:
            sf.errors.Error: If connection fails.
        """

        Debug.log(f"Connecting to Snowflake with profile: '{profile}'", 'DEBUG', verbose)

        if SnowflakeIntegration._connection:
            return SnowflakeIntegration._connection

        try:
            sf_creds = Config.get_snowflake_credentials(profile=profile)
            user_name = sf_creds["USERNAME"] if "USERNAME" in sf_creds else user_name
            account = sf_creds["ACCOUNT"] if "ACCOUNT" in sf_creds else account
            role = sf_creds["ROLE"] if "ROLE" in sf_creds else None
            key_file_path = sf_creds["KEY_FILE_PATH"] if "KEY_FILE_PATH" in sf_creds else None
            key_file_password = sf_creds["KEY_FILE_PASSWORD"] if "KEY_FILE_PASSWORD" in sf_creds else None
            database = sf_creds["DATABASE"] if "SNOWFLAKE_DATABASE" in sf_creds else None
            schema = sf_creds["SCHEMA"] if "SNOWFLAKE_SCHEMA" in sf_creds else None
            warehouse = sf_creds["SNOWFLAKE_WAREHOUSE"] if "SNOWFLAKE_WAREHOUSE" in sf_creds else None
            
            Debug.log(f"\nSnowflake credentials found in config.toml by user: \nUSERNAME: {user_name}\nACCOUNT: {account}\n", 'DEBUG', verbose)

        except TypeError as e:
            Debug.log(f"No profile named '{profile}' in config file.", 'ERROR')
            raise sf.errors.ConfigSourceError
        except KeyError as e:
            Debug.log(f"Missing key in configuration: {e}", 'ERROR')
            raise sf.errors.ConfigSourceError
        
        
        try:
            
            if key_file_path is not None and key_file_password is not None:
                SnowflakeIntegration._connection = sf.connect(
                    user=user_name,
                    account=account,
                    private_key_file=key_file_path,
                    private_key_file_pwd=key_file_password
                )

            if SnowflakeIntegration._connection == None:
                Debug.log(f"\nCould not connect to Snowflake, did you create a .toml file?\nRemember you can always connect using account + username.", 'ERROR')
                raise Exception
            
            return SnowflakeIntegration._connection

           
        except Exception as e:
            Debug.log(f"\nCould not connect to Snowflake, did you create a .toml file?\nRemember you can always connect using account + username.\nError message: {e}", 'ERROR')
            raise sf.errors.ConfigSourceError