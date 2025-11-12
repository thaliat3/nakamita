# cargar_empleados.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'control_asistencia.settings')
django.setup()

from app.models import Empleado, TipoAsistencia

# Crear empleados (ordenados alfabéticamente por apellidos y luego nombres)
empleados_data = [
    {"nombres": "Ademir", "apellidos": "Arredondo", "dni": 10000001, "contrato": "Planilla"},
    {"nombres": "Alexis", "apellidos": "Vasquez Conchatupac", "dni": 10000002, "contrato": "Planilla"},
    {"nombres": "Carlos Fernando", "apellidos": "Lozano Roman", "dni": 10000003, "contrato": "Planilla"},
    {"nombres": "Carlos Gabriel", "apellidos": "More Miranda", "dni": 10000004, "contrato": "Planilla"},
    {"nombres": "Cecy Kattia", "apellidos": "Salcedo Arauda", "dni": 10000005, "contrato": "Planilla"},
    {"nombres": "Claudia", "apellidos": "Aguilar", "dni": 10000006, "contrato": "Planilla"},
    {"nombres": "David Eduardo", "apellidos": "Pauta Juarez", "dni": 10000007, "contrato": "Planilla"},
    {"nombres": "Edwin", "apellidos": "Chaparro Ampa", "dni": 10000008, "contrato": "Planilla"},
    {"nombres": "Edson Pavel", "apellidos": "Ipenza", "dni": 10000009, "contrato": "Planilla"},
    {"nombres": "Iris", "apellidos": "Oblitas La Rosa", "dni": 10000010, "contrato": "Planilla"},
    {"nombres": "Jean Leonardo", "apellidos": "Estrada Roque", "dni": 10000011, "contrato": "Planilla"},
    {"nombres": "Joel Edwin", "apellidos": "Llanos Mejico", "dni": 10000012, "contrato": "Planilla"},
    {"nombres": "Jordi Cesar Hernando", "apellidos": "Quezada Rosales", "dni": 10000013, "contrato": "Planilla"},
    {"nombres": "Jose Alberto", "apellidos": "Davila Paredes", "dni": 10000014, "contrato": "Planilla"},
    {"nombres": "Jose Angel", "apellidos": "Borda Hernandez", "dni": 10000015, "contrato": "Planilla"},
    {"nombres": "Jose Lino", "apellidos": "Solano Caqui", "dni": 10000016, "contrato": "Planilla"},
    {"nombres": "Jose Luis", "apellidos": "Gonzalez Romero", "dni": 10000017, "contrato": "Planilla"},
    {"nombres": "Julio Daniel", "apellidos": "Peñaherrera Orrillo", "dni": 10000018, "contrato": "Planilla"},
    {"nombres": "Marco Antonio Jose", "apellidos": "Garcia Galvan", "dni": 10000019, "contrato": "Planilla"},
    {"nombres": "Pedro Luis", "apellidos": "Hernandez Reyes", "dni": 10000020, "contrato": "Planilla"},
    {"nombres": "Romulo", "apellidos": "Prieto", "dni": 10000021, "contrato": "Planilla"},
    {"nombres": "Ruben Dario", "apellidos": "Canicani Cahuana", "dni": 10000022, "contrato": "Planilla"},
    {"nombres": "Thalia", "apellidos": "Giral Onton", "dni": 10000023, "contrato": "Planilla"},
    {"nombres": "Valery", "apellidos": "Celestino Begar", "dni": 10000024, "contrato": "Planilla"},
    {"nombres": "Willy Jhon", "apellidos": "Paco Deza", "dni": 10000025, "contrato": "Planilla"},
    {"nombres": "Wilmer", "apellidos": "Quispe Huaringa", "dni": 10000026, "contrato": "Planilla"},
    {"nombres": "Yuli", "apellidos": "Tarazona", "dni": 10000027, "contrato": "Planilla"},
    {"nombres": "Zhihua Santiago", "apellidos": "Yong Sanchez", "dni": 10000028, "contrato": "Planilla"},
    {"nombres": "Jaime Franksue", "apellidos": "Sullon Li", "dni": 10000029, "contrato": "Planilla"},
    {"nombres": "Jonathan Oswaldo", "apellidos": "Azaña Ramos", "dni": 10000030, "contrato": "Planilla"}
]

empleados_data_sorted = sorted(
    empleados_data,
    key=lambda e: (e["apellidos"].lower(), e["nombres"].lower())
)

# Inserción/actualización masiva por clave única DNI
# - Si ya existe el DNI, actualiza nombres, apellidos y contrato
# - Si no existe, crea el registro
Empleado.objects.bulk_create(
    [Empleado(**e) for e in empleados_data_sorted],
    update_conflicts=True,
    update_fields=["nombres", "apellidos", "contrato"],
    unique_fields=["dni"],
)

# Crear tipos de asistencia si no existen
tipos = [
    'Entrada', 'Salida', 'Inicio Almuerzo', 'Fin Almuerzo',
    'Entrada por comisión', 'Salida por comisión',
    'Entrada por otros', 'Salida por otros'
]
for nombre in tipos:
    TipoAsistencia.objects.get_or_create(nombre_asistencia=nombre)

print("Datos insertados correctamente.")
