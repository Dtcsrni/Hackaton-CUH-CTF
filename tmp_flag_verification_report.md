# Flag Verification Report

| ID | Reto | Flag | Estado | Evidencia |
|---:|---|---|---|---|
| 1 | Calentamiento - Bienvenida | `CUH{cuh_ctf_2026_ok}` | verified_source_script | `refresh_assets/normalizar_formato_flags_y_reset.sh` |
| 2 | Leer también es hacking | `CUH{leer_hasta_el_final_tiene_premio}` | verified_source_script | `refresh_assets/pages/index.html` |
| 3 | Robots curiosos | `CUH{robots_no_guardan_secretos}` | registered_only | `page_overhaul_remote.py` |
| 4 | Base64 no es cifrado | `CUH{base64_es_solo_codificacion}` | registered_only | `audit_description_flag_alignment.py` |
| 5 | César escolar | `CUH{cesar_es_inicio}` | registered_only | `audit_description_flag_alignment.py` |
| 6 | Puertas abiertas | `CUH{escanear_antes_de_interpretar}` | verified_effective_source | `CTF_CUH/01_escaneo_de_puertos_puertas_abiertas/server_31337.py` |
| 7 | Metadatos indiscretos | `CUH{los_metadatos_hablan}` | registered_only | `` |
| 8 | Comandos Linux - búsqueda básica | `CUH{linux_tambien_se_investiga}` | verified_effective_source | `CTF_CUH/02_comandos_linux_busqueda_basica/reto_linux/evidencia/oculto/flag.txt` |
| 9 | Logo en observación | `CUH{el_logo_tambien_documenta}` | registered_only | `` |
| 10 | Portada con pista | `CUH{la_portada_si_tenia_pistas}` | registered_only | `` |
| 11 | Cabeceras del laboratorio | `CUH{las_cabeceras_tambien_informan}` | registered_only | `` |
| 12 | JSON de prueba | `CUH{las_respuestas_json_tambien_guian}` | registered_only | `` |
| 13 | Bitácora del proxy | `CUH{los_logs_tambien_cuentan}` | registered_only | `` |
| 14 | Hash filtrado | `CUH{pin_2603}` | verified_source_script | `refresh_assets/normalizar_formato_flags_y_reset.sh` |
| 15 | ZIP bajo llave | `CUH{zip_con_clave_debil}` | registered_only | `` |
| 16 | Acceso heredado | `CUH{basic_auth_tambien_se_audita}` | registered_only | `` |
| 17 | Registro sin servidor | `CUH{el_servidor_tambien_debe_validar}` | verified_source_script | `.tmp_deploy_forms_remote.sh` |
| 18 | Encuesta confiada | `CUH{nunca_confies_en_campos_ocultos}` | verified_source_script | `.tmp_deploy_forms_remote.sh` |
| 19 | Invitado privilegiado | `CUH{el_payload_no_se_debe_confiar}` | registered_only | `` |
| 20 | Secreto compartido debil | `CUH{hs256_necesita_secretos_reales}` | registered_only | `` |
| 21 | Fuente principal | `CUH{el_codigo_fuente_tambien_orienta}` | verified_source_script | `refresh_assets/validar_fuente_principal.sh` |
| 22 | Consola curiosa | `CUH{la_consola_tambien_revela_pistas}` | registered_only | `user-preview.html` |
| 23 | Cookie de rol | `CUH{las_cookies_tambien_autorizan}` | registered_only | `` |
| 24 | Cookie firmada debil | `CUH{firmar_cookies_importa}` | registered_only | `` |
| 25 | Acceso por defecto | `CUH{la_fuerza_bruta_tambien_es_contexto}` | verified_source_script | `make_bruteforce_assets.py` |
| 29 | Formulario de acceso | `CUH{hydra_tambien_necesita_precision}` | verified_source_script | `make_bruteforce_assets.py` |
| 30 | Consulta concatenada | `CUH{consulta_concatenada_corregida}` | verified_effective_source | `CTF_CUH/03_consulta_concatenada/bundle/challenge.json` |
| 31 | Reportes sin parámetros | `CUH{reportes_filtrados_con_parametros}` | verified_effective_source | `CTF_CUH/04_reportes_sin_parametros/bundle/challenge.json` |
| 32 | Portal PHP heredado | `CUH{portal_php_heredado_endurecido}` | verified_effective_source | `CTF_CUH/05_portal_php_heredado/bundle/challenge.json` |
| 33 | Incidente en formularios | `CUH{incidente_de_formularios_reconstruido}` | verified_effective_source | `CTF_CUH/06_incidente_en_formularios/bundle/challenge.json` |
| 34 | Sesión que confía demasiado | `CUH{rol_de_sesion_validado_en_backend}` | verified_effective_source | `CTF_CUH/07_sesion_que_confia_demasiado/bundle/challenge.json` |
| 35 | Cookie de rol heredada | `CUH{cookie_de_rol_endurecida}` | verified_effective_source | `CTF_CUH/08_cookie_de_rol_heredada/bundle/challenge.json` |
| 36 | JWT sin audiencia | `CUH{jwt_con_validacion_completa}` | verified_effective_source | `CTF_CUH/09_jwt_sin_audiencia/bundle/challenge.json` |
| 37 | Restablecimiento abierto | `CUH{token_de_reset_endurecido}` | verified_effective_source | `CTF_CUH/10_restablecimiento_abierto/bundle/challenge.json` |
| 38 | Subida de archivos ansiosa | `CUH{subida_de_archivos_endurecida}` | verified_effective_source | `CTF_CUH/11_subida_de_archivos_ansiosa/bundle/challenge.json` |
| 39 | Traversal en miniatura | `CUH{rutas_normalizadas_y_resueltas}` | verified_effective_source | `CTF_CUH/12_traversal_en_miniatura/bundle/challenge.json` |
| 40 | Portal defaceado en PHP | `CUH{deface_reconstruido_y_contenido}` | verified_effective_source | `CTF_CUH/13_portal_defaceado_en_php/bundle/challenge.json` |
| 41 | Cabeceras que revelan de más | `CUH{cabeceras_endurecidas}` | verified_effective_source | `CTF_CUH/14_cabeceras_que_revelan_de_mas/bundle/challenge.json` |
| 42 | Prompt de soporte indiscreto | `CUH{prompt_de_soporte_endurecido}` | verified_effective_source | `CTF_CUH/15_prompt_de_soporte_indiscreto/bundle/challenge.json` |
| 43 | Recuperación de contexto | `CUH{contexto_filtrado_y_mitigado}` | verified_effective_source | `CTF_CUH/16_recuperacion_de_contexto/bundle/challenge.json` |
| 44 | Linux expuesto: sudoers heredado | `CUH{sudoers_heredado_corregido}` | verified_effective_source | `CTF_CUH/17_linux_expuesto_sudoers_heredado/bundle/challenge.json` |
| 45 | Linux expuesto: servicio olvidado | `CUH{servicio_olvidado_documentado_y_limitado}` | verified_effective_source | `CTF_CUH/18_linux_expuesto_servicio_olvidado/bundle/challenge.json` |
| 46 | Windows expuesto: share legado | `CUH{share_legado_reducido}` | verified_effective_source | `CTF_CUH/19_windows_expuesto_share_legado/bundle/challenge.json` |
| 47 | Windows expuesto: tareas persistentes | `CUH{persistencia_en_tareas_reconstruida}` | verified_effective_source | `CTF_CUH/20_windows_expuesto_tareas_persistentes/bundle/challenge.json` |
| 48 | Binario de despacho | `CUH{clave_de_despacho_recuperada}` | verified_effective_source | `CTF_CUH/21_binario_de_despacho/bundle/challenge.json` |
| 49 | Licencia bajo revisión | `CUH{licencia_reconstruida_sin_parche}` | verified_effective_source | `CTF_CUH/22_licencia_bajo_revision/bundle/challenge.json` |
| 50 | Perfil disperso | `CUH{perfil_disperso_correlacionado}` | verified_effective_source | `CTF_CUH/23_perfil_disperso/bundle/challenge.json` |
| 51 | Agenda filtrada | `CUH{agenda_filtrada_reconstruida}` | verified_effective_source | `CTF_CUH/24_agenda_filtrada/bundle/challenge.json` |
| 52 | Foto del laboratorio | `CUH{foto_del_laboratorio_interpretada}` | verified_effective_source | `CTF_CUH/25_foto_del_laboratorio/bundle/challenge.json` |
| 53 | Proveedor fantasma | `CUH{proveedor_fantasma_correlacionado}` | verified_effective_source | `CTF_CUH/26_proveedor_fantasma/bundle/challenge.json` |
| 54 | Huella de publicación | `CUH{huella_de_publicacion_reconstruida}` | verified_effective_source | `CTF_CUH/27_huella_de_publicacion/bundle/challenge.json` |
| 55 | XOR de respaldo | `CUH{xor_reutilizado_identificado}` | verified_effective_source | `CTF_CUH/28_xor_de_respaldo/bundle/challenge.json` |
| 56 | Firma reciclada | `CUH{firma_con_nonce_repetido_detectada}` | verified_effective_source | `CTF_CUH/29_firma_reciclada/bundle/challenge.json` |
| 57 | RSA sin OAEP | `CUH{rsa_con_oaep_y_sha256}` | verified_effective_source | `CTF_CUH/30_rsa_sin_oaep/bundle/challenge.json` |
| 58 | Derivación lenta | `CUH{kdf_endurecida_con_pbkdf2}` | verified_effective_source | `CTF_CUH/31_derivacion_lenta/bundle/challenge.json` |
| 59 | Bloques repetidos | `CUH{bloques_repetidos_interpretados}` | verified_effective_source | `CTF_CUH/32_bloques_repetidos/bundle/challenge.json` |
| 60 | CBC sin integridad | `CUH{cbc_sin_integridad_identificada}` | verified_effective_source | `CTF_CUH/33_cbc_sin_integridad/bundle/challenge.json` |
| 61 | IV reciclado en reportes | `CUH{iv_reciclado_detectado_en_reportes}` | verified_effective_source | `CTF_CUH/34_iv_reciclado_en_reportes/bundle/challenge.json` |
| 62 | HMAC truncado en gateway | `CUH{gateway_hmac_verificado_completo}` | verified_effective_source | `CTF_CUH/35_hmac_truncado_en_gateway/bundle/challenge.json` |
| 63 | Semilla predecible | `CUH{entropia_fuerte_para_llaves}` | verified_effective_source | `CTF_CUH/36_semilla_predecible/bundle/challenge.json` |
| 64 | Certificados a ciegas | `CUH{tls_validado_con_ca_y_hostname}` | verified_effective_source | `CTF_CUH/37_certificados_a_ciegas/bundle/challenge.json` |
| 65 | Cronología cruzada | `CUH{cronologia_cruzada_reconstruida}` | verified_effective_source | `CTF_CUH/38_cronologia_cruzada/bundle/challenge.json` |
| 66 | Repositorio fantasma | `CUH{repositorio_fantasma_atribuido}` | verified_effective_source | `CTF_CUH/39_repositorio_fantasma/bundle/challenge.json` |
| 67 | Credencial en ponencia | `CUH{credencial_en_ponencia_correlacionada}` | verified_effective_source | `CTF_CUH/40_credencial_en_ponencia/bundle/challenge.json` |
| 68 | Red de proveedores | `CUH{red_de_proveedores_mapeada}` | verified_effective_source | `CTF_CUH/41_red_de_proveedores/bundle/challenge.json` |
| 69 | Trazas de convocatoria | `CUH{convocatoria_atribuida_y_validada}` | verified_effective_source | `CTF_CUH/42_trazas_de_convocatoria/bundle/challenge.json` |
| 70 | Traza en PCAP | `CUH{tshark_reconstruye_la_pista}` | verified_effective_source | `CTF_CUH/43_traza_en_pcap/bundle/challenge.json` |
| 71 | Firmware en capas | `CUH{binwalk_descubre_el_resto_olvidado}` | verified_effective_source | `CTF_CUH/44_firmware_en_capas/bundle/challenge.json` |
| 72 | Metadatos en cascada | `CUH{exiftool_enlaza_la_historia}` | verified_effective_source | `CTF_CUH/45_metadatos_en_cascada/bundle/challenge.json` |
| 73 | Carving de evidencias | `CUH{foremost_recupera_la_pieza_util}` | verified_effective_source | `CTF_CUH/46_carving_de_evidencias/bundle/challenge.json` |
| 74 | Diccionario de laboratorio | `CUH{john_prioriza_el_contexto}` | verified_effective_source | `CTF_CUH/47_diccionario_de_laboratorio/bundle/challenge.json` |
| 75 | Portal sin redirección segura | `CUH{https_obligatorio_desde_el_borde}` | verified_effective_source | `CTF_CUH/48_portal_sin_redireccion_segura/bundle/challenge.json` |
| 76 | HSTS pendiente | `CUH{hsts_define_la_politica_de_transporte}` | verified_effective_source | `CTF_CUH/49_hsts_pendiente/bundle/challenge.json` |
| 77 | Cookie de sesión sin Secure | `CUH{cookies_de_sesion_solo_por_https}` | verified_effective_source | `CTF_CUH/50_cookie_de_sesion_sin_secure/bundle/challenge.json` |
| 78 | Contenido mixto heredado | `CUH{todos_los_recursos_van_por_https}` | verified_effective_source | `CTF_CUH/51_contenido_mixto_heredado/bundle/challenge.json` |
| 79 | Credenciales expuestas en tránsito | `CUH{credenciales_expuestas_por_http_reconstruidas}` | verified_effective_source | `CTF_CUH/52_credenciales_expuestas_en_transito/bundle/challenge.json` |
| 80 | Rompe el sistema | `CUH{rompe_el_sistema_reportado_con_responsabilidad}` | registered_only | `` |
