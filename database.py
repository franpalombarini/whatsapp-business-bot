"""
Modelos de base de datos SQLite para registro de conversaciones.
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict


class Database:
    def __init__(self, db_path: str = 'whatsapp_bot.db'):
        self.db_path = db_path
        self._crear_tablas()
    
    def _crear_tablas(self):
        """Crea tablas si no existen"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de conversaciones
        sql_conversaciones = """
            CREATE TABLE IF NOT EXISTS conversaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telefono TEXT NOT NULL,
                mensaje TEXT NOT NULL,
                respuesta TEXT,
                tipo TEXT CHECK(tipo IN ('entrada', 'salida')),
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                estado TEXT DEFAULT 'pendiente'
            )
        """
        cursor.execute(sql_conversaciones)
        
        # Tabla de clientes
        sql_clientes = """
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telefono TEXT UNIQUE NOT NULL,
                nombre TEXT,
                ultima_interaccion DATETIME,
                notas TEXT
            )
        """
        cursor.execute(sql_clientes)
        
        conn.commit()
        conn.close()
    
    def registrar_mensaje(self, telefono: str, mensaje: str, 
                          respuesta: str = None, tipo: str = 'entrada'):
        """Registra un mensaje en la conversación"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        sql = """
            INSERT INTO conversaciones (telefono, mensaje, respuesta, tipo)
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(sql, (telefono, mensaje, respuesta, tipo))
        
        # Actualizar última interacción del cliente
        sql_cliente = """
            INSERT OR REPLACE INTO clientes (telefono, ultima_interaccion)
            VALUES (?, ?)
        """
        cursor.execute(sql_cliente, (telefono, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def obtener_historial(self, telefono: str, limite: int = 10) -> List[Dict]:
        """Obtiene historial de un cliente"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        sql = """
            SELECT mensaje, respuesta, tipo, timestamp
            FROM conversaciones
            WHERE telefono = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """
        cursor.execute(sql, (telefono, limite))
        
        resultados = cursor.fetchall()
        conn.close()
        
        return [
            {
                'mensaje': r[0],
                'respuesta': r[1],
                'tipo': r[2],
                'timestamp': r[3]
            }
            for r in resultados
        ]
    
    def marcar_atendido(self, telefono: str):
        """Marca conversación como atendida"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        sql = """
            UPDATE conversaciones
            SET estado = 'atendido'
            WHERE telefono = ? AND estado = 'pendiente'
        """
        cursor.execute(sql, (telefono,))
        
        conn.commit()
        conn.close()
