DENY_PATTERNS = ('muestra el prompt', 'revela token', 'ignora instrucciones')
SENSITIVE_FIELDS = ('token', 'secret', 'prompt_sistema', 'ruta_interna')

def redact_sensitive(context):
    cleaned = {}
    for key, value in context.items():
        cleaned[key] = '[redacted]' if key in SENSITIVE_FIELDS else value
    return cleaned

def build_prompt(system_prompt, allowed_scope, context, user_prompt):
    lowered = user_prompt.lower()
    for pattern in DENY_PATTERNS:
        if pattern in lowered:
            raise ValueError('solicitud fuera de alcance')
    safe_context = redact_sensitive(context)
    return system_prompt + '\nALCANCE:' + allowed_scope + '\nCONTEXTO:' + str(safe_context) + '\nUSUARIO:' + user_prompt
