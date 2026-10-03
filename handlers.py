"""
Manejo de mensajes entrantes y lógica de respuestas.
"""

from typing import Dict, Optional
from .database import Database
from .config import MENSAJES, API_URL
import requests
import logging

logger = logging.getLogger(__name__)


class MessageHandler:
    def __init__(self, db: Database):
        self.db = db
    
    def procesar_mensaje(self, telefono: str, mensaje: str) -> str:
        """
        Procesa mensaje entrante y devuelve respuesta.
        
        Args:
            telefono: Número del cliente
            mensaje: Texto del mensaje
            
        Returns:
            Texto de respuesta
        """
        mensaje_lower = mensaje.lower().strip()
        
        # Guardar mensaje en BD
        self.db.registrar_mensaje(telefono, mensaje, tipo='entrada')
        
        # Respuestas por palabra clave
        respuesta = None
        
        if any(palabra in mensaje_lower for palabra in ['hola', 'buenas', 'hi']):
            respuesta = MENSAJES['bienvenida']
        
        elif mensaje_lower in ['1', 'productos', 'info']:
            respuesta = "📦 *Catálogo de productos*

Escribinos a [email] o visitanos en [dirección] para ver nuestro catálogo completo."
        
        elif mensaje_lower in ['2', 'horarios', 'horario']:
            respuesta = "🕐 *Horarios de atención*

Lunes a Viernes: 9:00 - 18:00
Sábados: 9:00 - 13:00

Fuera de horario responderemos tu mensaje al día siguiente."
        
        elif mensaje_lower in ['3', 'humano', 'asesor', 'persona']:
            respuesta = MENSAJES['humano']
            # Acá va lógica para notificar a humano
        
        elif mensaje_lower in ['4', 'mensaje', 'dejar']:
            respuesta = "📝 *Dejanos tu mensaje*

Escribí tu consulta y te respondemos a la brevedad."
        
        else:
            respuesta = MENSAJES['default']
        
        # Guardar respuesta
        self.db.registrar_mensaje(telefono, respuesta, tipo='salida')
        
        return respuesta
    
    def enviar_respuesta(self, telefono: str, mensaje: str) -> bool:
        """
        Envía mensaje via API de WhatsApp Business.
        
        Args:
            telefono: Número destino (con código país, sin +)
            mensaje: Texto a enviar
            
        Returns:
            True si se envió correctamente
        """
        headers = {
            'Authorization': f'Bearer {WHATSAPP_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'messaging_product': 'whatsapp',
            'to': telefono,
            'type': 'text',
            'text': {'body': mensaje}
        }
        
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            logger.info(f"Mensaje enviado a {telefono}")
            return True
        except Exception as e:
            logger.error(f"Error enviando mensaje: {e}")
            return False
    
    def validar_webhook(self, token: str, challenge: str) -> Optional[str]:
        """
        Valida webhook de WhatsApp.
        
        Returns:
            challenge si el token es válido, None si no
        """
        if token == VERIFY_TOKEN:
            return challenge
        return None
