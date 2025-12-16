# ──────────────── CONFIGURACIÓN ────────────────
SERVICE = xls-compare

# ──────────────── COMANDOS PRINCIPALES ────────────────

# Levantar el contenedor (sin rebuild)
up:
	sudo docker compose up -d $(SERVICE)

# Parar el contenedor
down:
	sudo docker compose down $(SERVICE)

# Reconstruir y levantar (equivalente a --build)
rebuild:
	sudo docker compose up -d --build $(SERVICE)

# Ver logs en tiempo real
logs:
	sudo docker compose logs -f $(SERVICE)

# Eliminar imágenes, contenedores y volúmenes huérfanos
clean:
	sudo docker system prune -af
	sudo docker volume prune -f

# Mostrar estado actual de los contenedores
status:
	sudo docker ps

# Sincronizar assets (logo) hacia la carpeta estática de Flask
sync-assets:
	mkdir -p src/app/static/logo
	cp -r assets/logo/. src/app/static/logo/
