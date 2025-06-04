import MetaTrader5 as mt5
import sys
import os

# Dynamically add the root project directory to sys.path
def add_project_root_to_sys_path():
    current_path = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.abspath(os.path.join(current_path, ".."))
    if root_path not in sys.path:
        sys.path.append(root_path)

add_project_root_to_sys_path()

class MT5Connector:
    def __init__(self, login, password, server):
        self.login = login
        self.password = password
        self.server = server

    def initialize(self):
        if not mt5.initialize():
            raise Exception(f"❌ Initialization failed: {mt5.last_error()}")

        authorized = mt5.login(self.login, password=self.password, server=self.server)
        if not authorized:
            raise Exception(f"❌ Login failed: {mt5.last_error()}")

        print(f"✅ Successfully connected to MetaTrader 5 Server: {self.server}")

    def shutdown(self):
        mt5.shutdown()
        print("🔕 MT5 connection closed.")

    def check_connection(self):
        if not mt5.initialize():
            return False
        authorized = mt5.login(self.login, password=self.password, server=self.server)
        return authorized

    def get_account_info(self):
        account_info = mt5.account_info()
        if account_info is None:
            raise Exception(f"❌ Failed to get account info: {mt5.last_error()}")
        return account_info._asdict()

# Example Usage
def test_connection():
    from config.mt5_config import MT5_LOGIN, MT5_PASSWORD, MT5_SERVER

    connector = MT5Connector(
        login=MT5_LOGIN,
        password=MT5_PASSWORD,
        server=MT5_SERVER
    )

    try:
        connector.initialize()
        info = connector.get_account_info()
        print("📊 Account Info:", info)
    finally:
        connector.shutdown()

if __name__ == "__main__":
    test_connection()