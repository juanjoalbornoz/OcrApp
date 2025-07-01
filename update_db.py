#!/usr/bin/env python3

import sqlite3
from pathlib import Path

# Ruta a la base de datos
APP_DIR = Path(__file__).resolve().parent / "app"
DB_PATH = APP_DIR / "ocrapp.db"

def update_database():
    """Actualiza la base de datos agregando la tabla de bloqueos de recuperación de contraseña"""
    
    print(f"Conectando a la base de datos: {DB_PATH}")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Verificar si la tabla ya existe
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='password_recovery_blocks'
        """)
        
        if cursor.fetchone():
            print("La tabla 'password_recovery_blocks' ya existe.")
        else:
            # Crear la tabla para el sistema de bloqueo de recuperación de contraseñas
            cursor.execute("""
                CREATE TABLE password_recovery_blocks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    failed_attempts INTEGER DEFAULT 0,
                    blocked_until DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Crear índice para búsquedas más rápidas por email
            cursor.execute("""
                CREATE INDEX idx_password_recovery_blocks_email 
                ON password_recovery_blocks(email)
            """)
            
            conn.commit()
            print("✅ Tabla 'password_recovery_blocks' creada exitosamente.")
        
        print("✅ Base de datos actualizada correctamente.")
        
    except Exception as e:
        print(f"❌ Error al actualizar la base de datos: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    update_database()
