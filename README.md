# WhatsApp Business Bot

Bot automatizado para atención al cliente de PyMEs via WhatsApp Business API.

## Características

- Respuestas automáticas por palabra clave
- Menú interactivo de opciones
- Registro de conversaciones en SQLite
- Integración con API de WhatsApp Business
- Panel web simple para administración

## Estructura

```
whatsapp-business-bot/
├── README.md
├── requirements.txt
├── config.py           # Configuración y variables
├── bot.py              # Lógica principal del bot
├── handlers.py         # Manejo de mensajes
├── database.py         # Modelos SQLite
└── webapp/
    ├── app.py          # Flask admin panel
    └── templates/      # HTML admin
```

## Configuración

```python
# config.py
WHATSAPP_TOKEN = "tu-token-de-whatsapp-business"
VERIFY_TOKEN = "tu-token-de-verificacion"
PHONE_NUMBER_ID = "tu-phone-number-id"
```

## Uso

```bash
pip install -r requirements.txt
python bot.py
```

## Flujo de mensajes

1. Cliente envía mensaje
2. Webhook recibe y valida
3. Handler procesa texto/comandos
4. Respuesta automática o escalada a humano

## Próximos pasos

- [ ] Integración con calendario (turnos)
- [ ] Respuestas con IA (Ollama local)
- [ ] Estadísticas de atención

---

**Desarrollado por:** Franco Palombarini  
**Contacto:** fran.palombarini.dev@gmail.com  
**LinkedIn:** linkedin.com/in/franpalombarini-dev
