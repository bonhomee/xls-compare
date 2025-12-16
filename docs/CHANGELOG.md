# Changelog

Se sigue el formato [SemVer](https://semver.org/lang/es/) y este documento registra cambios visibles para el usuario.

## [1.2.4] - 2025-10-26
- Documentación actualizada: refleja que solo se listan proveedores presentes en ambos archivos y con diferencia != 0.
- Se eliminan referencias a secciones "Solo en Balance / Solo en DDP" en la doc.

## [1.2.3] - 2025-10-26
- Ajuste estético: footer de ancho completo con fondo gris claro y bordes redondeados, siempre al pie de página.

## [1.2.2] - 2025-10-26
- Footer fijado al fondo mediante layout flex (se muestra al final aunque haya poco contenido).

## [1.2.1] - 2025-10-26
- El pie de página se muestra siempre, sin depender de la comparación.
- Limpieza de la plantilla (el resumen general sigue oculto, sólo se renderizan diferencias cuando hay archivos cargados).

## [1.2.0] - 2025-10-26
- Sólo se muestran proveedores presentes en ambos archivos y con diferencia distinta de 0.
- Se eliminan las secciones "Solo en Balance" y "Solo en DDP" de la vista.

## [1.1.0] - 2025-10-26
- La diferencia ahora se calcula como `DDP + Balance` (útil cuando el Balance exporta saldos en negativo).
- Observaciones ajustadas según el nuevo cálculo.

## [1.0.0] - 2025-10-26
- Versión inicial con nueva estructura del proyecto (src/, docs/, infra/, scripts/, assets/).
- Funcionalidad base: comparación Balance vs DDP, normalización de IDs, vista web y documentación interna.
