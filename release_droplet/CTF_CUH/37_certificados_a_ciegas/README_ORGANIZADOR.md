# Certificados a ciegas

## Propósito didáctico
Practicar validación correcta de TLS del lado cliente con CA interna y verificación de hostname.

## Dinámica de resolución
El alumno endurece el contexto SSL y valida que desaparezca la confianza ciega.

## Material del alumno
- Bundle final: `certificados_a_ciegas_bundle.zip`
- Página de apoyo: `/certificados-a-ciegas`

## Validación del organizador
1. Ejecuta `python verify_organizer.py` dentro de esta carpeta.
2. Confirma que el validador devuelve `CUH{tls_validado_con_ca_y_hostname}`.
3. Sube el ZIP a CTFd como archivo descargable del reto.
4. Verifica que la página de apoyo publique el contexto correcto.

## Nota pedagógica
Reto de parche centrado en cadena de confianza y autenticidad del endpoint.
