from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent / 'CTF_CUH'
TARGETS = ['01_escaneo_de_puertos_puertas_abiertas', '02_comandos_linux_busqueda_basica', '03_consulta_concatenada', '04_reportes_sin_parametros', '05_portal_php_heredado', '06_incidente_en_formularios', '07_sesion_que_confia_demasiado', '08_cookie_de_rol_heredada', '09_jwt_sin_audiencia', '10_restablecimiento_abierto', '11_subida_de_archivos_ansiosa', '12_traversal_en_miniatura', '13_portal_defaceado_en_php', '14_cabeceras_que_revelan_de_mas', '15_prompt_de_soporte_indiscreto', '16_recuperacion_de_contexto', '17_linux_expuesto_sudoers_heredado', '18_linux_expuesto_servicio_olvidado', '19_windows_expuesto_share_legado', '20_windows_expuesto_tareas_persistentes', '21_binario_de_despacho', '22_licencia_bajo_revision', '23_perfil_disperso', '24_agenda_filtrada', '25_foto_del_laboratorio', '26_proveedor_fantasma', '27_huella_de_publicacion', '28_xor_de_respaldo', '29_firma_reciclada', '30_rsa_sin_oaep', '31_derivacion_lenta', '32_bloques_repetidos', '33_cbc_sin_integridad', '34_iv_reciclado_en_reportes', '35_hmac_truncado_en_gateway', '36_semilla_predecible', '37_certificados_a_ciegas', '38_cronologia_cruzada', '39_repositorio_fantasma', '40_credencial_en_ponencia', '41_red_de_proveedores', '42_trazas_de_convocatoria', '43_traza_en_pcap', '44_firmware_en_capas', '45_metadatos_en_cascada', '46_carving_de_evidencias', '47_diccionario_de_laboratorio', '48_portal_sin_redireccion_segura', '49_hsts_pendiente', '50_cookie_de_sesion_sin_secure', '51_contenido_mixto_heredado', '52_credenciales_expuestas_en_transito']

failed = []
for target in TARGETS:
    proc = subprocess.run([sys.executable, 'verify_organizer.py'], cwd=ROOT / target, text=True, capture_output=True)
    print(f'=== {target} ===')
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    if proc.returncode != 0:
        failed.append(target)
if failed:
    print('FALLARON:', ', '.join(failed))
    raise SystemExit(1)
print('ALL_LOCAL_CHALLENGES_OK')
