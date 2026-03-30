import sqlite3
from typing import List
from domain.message import Message
from application.ports.message_repository import IMessageRepository

DB_PATH = "events.db"


class SqliteMessageRepository(IMessageRepository):
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._ensure_table()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_table(self):
        conn = self._get_connection()
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topico TEXT NOT NULL,
                valor REAL NOT NULL,
                status TEXT NOT NULL,
                classe TEXT NOT NULL,
                data_hora TEXT NOT NULL
            );
            """
        )
        conn.commit()
        conn.close()

    def save(self, message: Message, is_critical: bool) -> Message:
        status = "CRÍTICO" if is_critical else "NORMAL"
        classe = "text-rose-400" if is_critical else "text-emerald-400"

        conn = self._get_connection()
        conn.execute(
            "INSERT INTO eventos (topico, valor, status, classe, data_hora) VALUES (?, ?, ?, ?, datetime('now'))",
            (message.topic, float(message.payload), status, classe),
        )
        conn.commit()
        conn.close()

        return message

    def list_recent(self, limit: int = 10) -> List[Message]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT topico, valor, status, classe, data_hora FROM eventos ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        rows = cursor.fetchall()
        conn.close()

        result = []
        for row in rows:
            msg = Message(topic=row["topico"], payload=str(row["valor"]))
            msg.is_critical = row["status"] == "CRÍTICO"
            result.append({
                "topico": row["topico"],
                "valor": row["valor"],
                "status": row["status"],
                "classe": row["classe"],
                "data_hora": row["data_hora"],
            })
        return result

    def list_by_date(self, date_str: str, limit: int = 100) -> List[Message]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT topico, valor, status, classe, data_hora FROM eventos WHERE date(data_hora) = ? ORDER BY id DESC LIMIT ?",
            (date_str, limit),
        )
        rows = cursor.fetchall()
        conn.close()

        result = []
        for row in rows:
            msg = Message(topic=row["topico"], payload=str(row["valor"]))
            msg.is_critical = row["status"] == "CRÍTICO"
            result.append({
                "topico": row["topico"],
                "valor": row["valor"],
                "status": row["status"],
                "classe": row["classe"],
                "data_hora": row["data_hora"],
            })
        return result
