#!/usr/bin/env python3
"""
Bot principal de WhatsApp Business.
"""

import logging
from flask import Flask, request, jsonify

from .config import VERIFY_TOKEN
from .handlers import MessageHandler
from .database import Database

# Configuración
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializar
app = Flask(__name__)
db = Database()
handler = MessageHandler(db)


@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verificación de webhook para Meta"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        logger.info("Webhook verificado")
        return challenge, 200
    
    return "Forbidden", 403


@app.route('/webhook', methods=['POST'])
def receive_message():
    """Recibe mensajes de WhatsApp"""
    data = request.get_json()
    
    try:
        # Extraer mensaje del payload complejo de WhatsApp
        entry = data['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        
        if 'messages' not in value:
            return jsonify({'status': 'no_message'}), 200
        
        message = value['messages'][0]
        telefono = message['from']
        texto = message['text']['body']
        
        logger.info(f"Mensaje de {telefono}: {texto[:50]}...")
        
        # Procesar y responder
        respuesta = handler.procesar_mensaje(telefono, texto)
        handler.enviar_respuesta(telefono, respuesta)
        
        return jsonify({'status': 'ok'}), 200
        
    except Exception as e:
        logger.error(f"Error procesando mensaje: {e}")
        return jsonify({'status': 'error', 'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de salud"""
    return jsonify({
        'status': 'running',
        'service': 'whatsapp-business-bot'
    })


if __name__ == '__main__':
    logger.info("Iniciando bot de WhatsApp...")
    app.run(host='0.0.0.0', port=5000, debug=False)
