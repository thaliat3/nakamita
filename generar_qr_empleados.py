#!/usr/bin/env python
"""
Script para generar códigos QR para todos los empleados.
Ejecutar: python generar_qr_empleados.py
"""

import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'control_asistencia.settings')
django.setup()

from app.models import Empleado
from app.qr_service import QRService

def generar_qr_todos():
    """Genera códigos QR para todos los empleados."""
    print("🔄 Generando códigos QR para todos los empleados...")
    
    empleados = Empleado.objects.all()
    print(f"📊 Total de empleados: {empleados.count()}")
    
    archivos_generados = []
    
    for empleado in empleados:
        try:
            print(f"👤 Procesando: {empleado.nombre_completo}")
            
            # Generar código QR si no existe
            codigo_qr = empleado.generar_codigo_qr()
            print(f"   📱 Código QR: {codigo_qr}")
            
            # Generar archivo QR
            archivo = QRService.generar_qr_empleado(empleado)
            print(f"   💾 Archivo: {archivo}")
            
            archivos_generados.append({
                'empleado': empleado,
                'codigo_qr': codigo_qr,
                'archivo': archivo
            })
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n✅ Proceso completado!")
    print(f"📁 Archivos generados: {len(archivos_generados)}")
    
    # Mostrar resumen
    print("\n📋 Resumen de códigos QR generados:")
    for item in archivos_generados:
        print(f"   • {item['empleado'].nombre_completo}: {item['codigo_qr']}")
    
    return archivos_generados

if __name__ == "__main__":
    try:
        archivos = generar_qr_todos()
        print(f"\n🎉 ¡Códigos QR generados exitosamente para {len(archivos)} empleados!")
    except Exception as e:
        print(f"\n❌ Error durante la generación: {e}")
        sys.exit(1)
