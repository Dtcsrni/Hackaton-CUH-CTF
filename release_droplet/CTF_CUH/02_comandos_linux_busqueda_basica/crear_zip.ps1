# Script para generar el archivo distribuible del reto Linux.
# El ZIP final conserva la carpeta raiz reto_linux para que el alumno la vea al descomprimir.

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceDir = Join-Path $scriptDir 'reto_linux'
$zipPath = Join-Path $scriptDir 'reto_archivos_linux.zip'

if (-not (Test-Path -LiteralPath $sourceDir)) {
    throw "No se encontro la carpeta fuente: $sourceDir"
}

if (Test-Path -LiteralPath $zipPath) {
    Remove-Item -LiteralPath $zipPath -Force
}

Compress-Archive -Path $sourceDir -DestinationPath $zipPath -CompressionLevel Optimal
Write-Host "ZIP generado correctamente en: $zipPath"
