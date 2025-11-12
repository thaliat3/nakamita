# Control de Asistencia (Django)

Aplicación web para el registro de asistencia de empleados con soporte para exportación a Excel, validación por dispositivo (FingerprintJS ID), y autenticación de personal administrativo para descarga de reportes.

## Características
- Registro de eventos de asistencia por empleado: Entrada, Salida, Inicio/Fin de Almuerzo, Comisión y Otros.
- Validaciones de negocio:
  - Eventos únicos por día para tipos: "Entrada", "Inicio Almuerzo", "Fin Almuerzo", "Salida".
  - Bloqueo por dispositivo: un mismo dispositivo (fingerprint) no puede registrar para dos empleados distintos el mismo día.
- Exportación a Excel:
  - Registro detallado de asistencia (`/login/descargar/asistencia`).
  - Resumen diario por empleado con cálculo de tiempos de almuerzo, comisión, permisos y horas trabajadas (`/login/descargar/resumen/`).
- Panel de login para personal (usa autenticación de Django) y acceso a página de descargas.
- Población rápida de datos de ejemplo mediante `cargar_empleados.py`.
- Generación de QR para acceso rápido a una URL con `generar_qr.py`.
- Preparado para despliegue (Railway/WSGI) y archivos estáticos servidos con WhiteNoise.

## Tecnologías
- Django 5.x
- Base de datos: SQLite (local) o PostgreSQL (producción)
- `openpyxl` para generación de Excel
- `dj-database-url` para configurar la base de datos vía `DATABASE_URL`
- `whitenoise` para estáticos en producción
- `python-dotenv` para variables de entorno
- `gunicorn` para WSGI en producción
- Opcional: FingerprintJS en el frontend (el ID se envía desde el formulario)

## Estructura (resumen)
- `app/models.py`: Modelos `Empleado`, `TipoAsistencia`, `RegistroAsistencia`.
- `app/views.py`: Registro de asistencia y exportaciones a Excel.
- `app/urls.py`: Rutas de app (formulario, descargas, resumen).
- `control_asistencia/settings.py`: Configuración, base de datos, estáticos, zona horaria `America/Lima`.
- `control_asistencia/urls.py`: Admin, login y enrutado principal.
- `cargar_empleados.py`: Script para poblar empleados y tipos de asistencia.
- `generar_qr.py`: Script para generar `qr_asistencia.png` a partir de una URL.
- `Procfile`: Comando para migraciones y ejecución WSGI.

## Modelado de datos
- `Empleado`: nombres, apellidos, DNI único, tipo de contrato.
- `TipoAsistencia`: catálogo de tipos (p. ej. Entrada, Salida, Inicio/Fin Almuerzo, Comisión, Otros).
- `RegistroAsistencia`: empleado, tipo, fecha, hora, descripción opcional, `fingerprint` opcional.

## Variables de entorno
Copia `example.env` a `.env` y ajusta:

- `DB_LIVE`: True/False. Si es False y no hay `DATABASE_URL`, se usa SQLite local.
- `DATABASE_URL`: URL completa PostgreSQL (tiene prioridad si está definida). Ejemplo: `postgresql://usuario:pass@host:5432/db`.
- Si no defines `DATABASE_URL` y `DB_LIVE=True`, se usan variables `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` (con SSL requerido).

Zona horaria por defecto: `America/Lima`. Hosts permitidos y CSRF incluyen `localhost` y Railway.

## Requisitos
- Python 3.13 (o versión compatible del entorno virtual incluido)
- Pip/venv
- Opcional: PostgreSQL si deseas producción local

## Instalación y ejecución local
1) Clonar el repositorio y crear entorno virtual (opcional si ya usas el `venv/` del proyecto):
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
```

2) Instalar dependencias:
```bash
pip install -r requirements.txt
```

3) Configurar variables de entorno:
- Copiar `example.env` a `.env` y ajustar según tu entorno. Para desarrollo rápido deja `DB_LIVE=False` y `DATABASE_URL` vacío (usa SQLite).

4) Aplicar migraciones:
```bash
python manage.py migrate
```

5) Crear superusuario (para acceder a descargas y admin si lo deseas):
```bash
python manage.py createsuperuser
```

6) Cargar datos de ejemplo (empleados y tipos):
```bash
python cargar_empleados.py
```

7) Ejecutar el servidor de desarrollo:
```bash
python manage.py runserver
```

- Formulario de asistencia: `http://127.0.0.1:8000/`
- Login: `http://127.0.0.1:8000/login/` (usa el superusuario creado)
- Página de descargas (tras login): `http://127.0.0.1:8000/login/descarga/`

## Uso
- Desde la página principal se registra un evento seleccionando `Empleado` y `Tipo de evento`. El sistema registra la fecha/hora del servidor (
`TIME_ZONE=America/Lima`).
- Si el formulario envía `fingerprint` (ID del dispositivo), se valida que un dispositivo no registre para dos empleados diferentes el mismo día.
- Para descargar reportes, inicia sesión y visita la página de descargas:
  - `Descargar asistencia`: `/login/descargar/asistencia`
  - `Descargar resumen`: `/login/descargar/resumen/`

### Reporte: Asistencia (detalle)
Incluye: Empleado, Tipo, Fecha, Hora, Descripción, ID Dispositivo.

### Reporte: Resumen diario
Calcula tiempos por día y empleado:
- **Tiempo de Almuerzo**: diferencia entre "Inicio almuerzo" y "Fin almuerzo".
- **Horas por Comisión**: "Salida por comisión" a "Entrada por comisión".
- **Horas por Permiso (Otros)**: "Salida por otros" a "Entrada por otros".
- **Horas Trabajadas Totales**: `Entrada` → `Salida` menos almuerzo y permisos.

## Generación de QR (opcional)
Edita la variable `url` en `generar_qr.py` y ejecuta:
```bash
python generar_qr.py
```
Genera `qr_asistencia.png` apuntando a la URL elegida.

## Despliegue
El proyecto está preparado para plataformas como Railway.

- Archivos estáticos: WhiteNoise (configurado en `MIDDLEWARE` y `STATICFILES_STORAGE`).
- Procfile:
```bash
web: python manage.py migrate && gunicorn control_asistencia.wsgi
```
- Base de datos: define `DATABASE_URL` (recomendado) o variables `DB_*` con `DB_LIVE=True`.
- Ajusta `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS` en `settings.py` con tu dominio.

### Pasos típicos (Railway)
1) Configura variables en el panel: `.env` equivalente (DATABASE_URL, etc.).
2) Habilita `python-3.x` y ejecuta el comando del Procfile.
3) Asegura que `STATIC_ROOT` exista (se genera en deploy); WhiteNoise servirá estáticos.

## Solución de problemas
- Error de base de datos en producción: verifica `DATABASE_URL` válido o `DB_*` con `DB_LIVE=True`. En Railway/Supabase, exige SSL; `settings.py` ya establece `sslmode=require`.
- No aparece el botón de descarga: las rutas de descarga requieren usuario autenticado y con `is_staff=True`. Ajusta en el admin de Django.
- Tiempos en la hora incorrecta: revisa `TIME_ZONE` y `USE_TZ=True`. En desarrollo, la hora se toma por `timezone.localtime()`.
- Fingerprint no se valida: asegúrate de enviar el ID del dispositivo desde el formulario (p. ej. mediante FingerprintJS) al campo `fingerprint`.

## Licencia
MIT (o la que definas). Ajusta este apartado según tus necesidades.

## Preparar y subir a repositorio
1) Asegúrate de NO commitear secretos:
   - `.env`, `db.sqlite3`, `venv/` y `staticfiles/` están en `.gitignore`.
2) Inicializa el repo y primer commit:
```bash
git init
git add .
git commit -m "Inicializa proyecto de control de asistencia"
```
3) Configura remoto y sube (GitHub como ejemplo):
```bash
git branch -M main
git remote add origin https://github.com/tu-usuario/control-asistencia.git
git push -u origin main
```
4) Configura variables en el repositorio/CI:
   - Añade `SECRET_KEY`, `DEBUG`, `DATABASE_URL` (o `DB_*`) como secretos del entorno.