"""
Configuración del bot de WhatsApp Business.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API de WhatsApp Business
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN', '')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'mi_token_secreto')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID', '')

# API URL
API_URL = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

# Base de datos
DATABASE_PATH = os.getenv('DATABASE_PATH', 'whatsapp_bot.db')

# Mensajes predefinidos
MENSAJES = {
    'bienvenida': """¡Hola! Soy el asistente virtual de [Nombre Empresa].
    
Elegí una opción:
1️⃣ Información de productos
2️⃣ Horarios de atención
3️⃣ Hablar con un humano
4️⃣ Dejar mensaje""",
    
    'opciones': ['1', '2', '3', '4'],
    
    'default': "No entendí tu mensaje. Escribí *hola* para ver las opciones.",
    
    'humano': "Te comunico con un asesor. Aguardá un momento...",
    
    'fuera_horario': "Estamos fuera de horario. Te respondemos mañana a primera hora."
}
