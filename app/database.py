import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

def get_db_path():
    """Obtiene la ruta correcta de la base de datos"""
    app_dir = Path(__file__).resolve().parent
    return app_dir / "ocrapp.db"

def init_db():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Tabla de presets
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS presets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            config TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Tabla de intentos de recuperación de contraseña
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS password_recovery_blocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            failed_attempts INTEGER DEFAULT 0,
            blocked_until TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print(f"✅ Base de datos creada/verificada en: {db_path}")

if __name__ == "__main__":
    init_db()