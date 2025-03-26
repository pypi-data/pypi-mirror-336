import sqlite3

from xdg_base_dirs import xdg_config_home

DB_PATH = f"{xdg_config_home()}/pymodoro.db"
print(DB_PATH)


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute(
                """CREATE TABLE IF NOT EXISTS settings (
                    focus_duration INTEGER DEFAULT 25,
                    break_duration INTEGER DEFAULT 5,
                    total_time_focused_minutes INTEGER DEFAULT 0
                )"""
            )
            self.conn.execute("INSERT OR IGNORE INTO settings VALUES (25, 5, 0)")
            self.conn.commit()

    def get_db_values(self) -> tuple[int, int, int]:
        cursor = self.conn.execute("SELECT * FROM settings")
        result = cursor.fetchone()
        print(int(result[0]), int(result[1]), int(result[2]))
        return (int(result[0]), int(result[1]), int(result[2])) if result else None

    def update_setting(self, key: str, value: int):
        with self.conn:
            self.conn.execute(f"UPDATE settings SET {key} = {value}")

    def close(self):
        self.conn.close()
