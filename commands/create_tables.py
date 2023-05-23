import sqlite3
from discord.ext import commands

class create_table(commands.Cog):
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
    
    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table_last_online(self, table_name):
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        table_exists = self.cursor.fetchone()

        if table_exists:
            return f"Table '{table_name}' already exists."
        else:
            self.cursor.execute(f"CREATE TABLE {table_name} (user_id INTEGER PRIMARY KEY, user_name TEXT, last_online TEXT)")
            return f"Table '{table_name}' created successfully."

    def create_table_admin(self, table_name):
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        table_exists = self.cursor.fetchone()

        if table_exists:
            return f"Table '{table_name}' already exists."
        else:
            self.cursor.execute(f"CREATE TABLE {table_name} (Admin_name TEXT UNIQUE PRIMARY KEY, Permissions INTEGER, DATA INTEGER, Last_mod TEXT)")
            return f"Table '{table_name}' created successfully."

    def create_table_users(self, table_name):
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        table_exists = self.cursor.fetchone()

        if table_exists:
            return f"Table '{table_name}' already exists."
        else:
            self.cursor.execute(f"CREATE TABLE {table_name} (user_id TEXT UNIQUE PRIMARY KEY, val_pts NUMERIC, bet_pts NUMERIC, rank TEXT, games INTEGER, bets INTEGER, games_win INTEGER, games_tied INTEGER, games_lost INTEGER, bet_win INTEGER, bet_lost INTEGER, LAST_GAME TEXT, LAST_BET TEXT, REG_DATA INTEGER, UP_DATA INTEGER)")
            return f"Table '{table_name}' created successfully."

    def create_table_acc(self, table_name):
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        table_exists = self.cursor.fetchone()

        if table_exists:
            return f"Table '{table_name}' already exists."
        else:
            self.cursor.execute(f"CREATE TABLE {table_name} (ACCOUNT TEXT PRIMARY KEY, PASSWORD TEXT, GAME_ID TEXT, RANK TEXT, OWNER TEXT, DATA INTEGER)")
            return f"Table '{table_name}' created successfully."

    def close(self):
        self.cursor.close()
        self.conn.close()

    def create_table_match_history(self, table_name):
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        table_exists = self.cursor.fetchone()

        if table_exists:
            return f"Table '{table_name}' already exists."
        else:
            self.cursor.execute(f"CREATE TABLE {table_name} (No INTEGER PRIMARY KEY, DATA TEXT,Admin TEXT,System TEXT,Map TEXT,Winner TEXT, Team_a_rr INTEGER, Team_b_rr INTEGER, A1 TEXT,A2 TEXT,A3 TEXT,A4 TEXT,A5 TEXT,B1 TEXT,B2 TEXT,B3 TEXT,B4 TEXT,B5 TEXT)")
            return f"Table '{table_name}' created successfully."

    def close(self):
        self.cursor.close()
        self.conn.close()

def setup(client):
    client.add_cog(create_table(client))
    