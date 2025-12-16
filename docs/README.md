# Comparador Balance vs DDP

Aplicación web en Flask que cruza el Balance de Sumas y Saldos de los proveedores (exportado de tu ERP) con el archivo DDP manual para detectar diferencias de importe proveedor por proveedor.

## Características principales

- Subida de dos archivos `.xls`/`.xlsx` (Balance y DDP).
- Normalización automática de IDs con la regla `40000XXXX`.
- Agrupación de importes duplicados en DDP.
- Tablas diferenciadas: diferencias detectadas, solo en Balance, solo en DDP.
- Totales globales y formateo monetario español.
- Página de documentación accesible desde la UI (`/documentacion`).

## Requisitos

- Docker + Docker Compose plugin (`docker compose`).
- Python 3.10 (dentro del contenedor) y dependencias listadas en `src/requirements.txt`.

## Puesta en marcha rápida

```bash
# Construir y levantar solo el servicio Flask
cd /ruta/al/proyecto/docker
sudo docker compose up -d --build xls-compare

# Ver logs
sudo docker compose logs -f xls-compare
```

Accede en el navegador a `http://<host>:8083`.

## Estructura resumida

- `src/` – Código Python y recursos de ejecución.
  - `app/` – Blueprint, rutas, servicios, plantillas y estáticos.
  - `wsgi.py` – Punto de entrada para Flask/WSGI.
  - `requirements.txt` – Dependencias del servicio.
- `infra/` – Artefactos de despliegue (por ejemplo, `Dockerfile`).
- `docs/` – Documentación y `CHANGELOG.md`.
- `assets/` – Recursos originales (logos, ficheros de ejemplo, etc.).
- `scripts/` – Herramientas auxiliares (Makefile con atajos para Docker).

## Sincronización de assets

- La imagen de Docker copia automáticamente los archivos de `assets/logo/` hacia `src/app/static/logo/` durante el build, por lo que siempre estarán disponibles en producción.
- En desarrollo local puedes ejecutar `make sync-assets` para refrescar la carpeta estática tras cambiar un logo u otro recurso.

## Versionado

- Se sigue SemVer (Mayor.Menor.Patch).
- Versión actual: `1.2.4`.
- Cada cambio que afecte a los usuarios implica actualizar `docs/VERSION` antes de commitear.
- El valor se refleja automáticamente tanto en la UI como en la documentación (`/documentacion`).

## Documentación y mantenimiento

Consulta la documentación completa en la propia aplicación (botón “Ver documentación completa”). Incluye flujo de datos, normalización, límites y comandos útiles.
