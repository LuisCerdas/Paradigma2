"""
Script para verificar la conexión a SQL Server
Ejecuta: python verificar_conexion.py
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ec.settings')
django.setup()

from django.db import connection
from django.core.management.color import no_style

def verificar_conexion():
    """Verifica la conexión a la base de datos"""
    try:
        print("Intentando conectar a SQL Server...")
        print(f"Base de datos: {connection.settings_dict['NAME']}")
        print(f"Host: {connection.settings_dict['HOST']}")
        print(f"Puerto: {connection.settings_dict['PORT']}")
        print(f"Instancia: {connection.settings_dict['OPTIONS'].get('instance', 'Default')}")
        print()
        
        # Intentar conectar
        with connection.cursor() as cursor:
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()
            print("[OK] Conexion exitosa!")
            print(f"Version de SQL Server: {version[0][:50]}...")
            print()
            
            # Verificar que la base de datos existe
            cursor.execute("SELECT name FROM sys.databases WHERE name = 'DB_TiendaOnline'")
            db_exists = cursor.fetchone()
            if db_exists:
                print("[OK] Base de datos 'DB_TiendaOnline' encontrada")
            else:
                print("[ERROR] Base de datos 'DB_TiendaOnline' NO encontrada")
                print("  Debes ejecutar el script SQL para crear la base de datos")
            print()
            
            # Verificar schema
            cursor.execute("""
                SELECT name FROM sys.schemas 
                WHERE name = 'SC_TiendaOline'
            """)
            schema_exists = cursor.fetchone()
            if schema_exists:
                print("[OK] Schema 'SC_TiendaOline' encontrado")
            else:
                print("[ERROR] Schema 'SC_TiendaOline' NO encontrado")
            print()
            
            # Verificar tablas
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = 'SC_TiendaOline'
                ORDER BY TABLE_NAME
            """)
            tablas = cursor.fetchall()
            if tablas:
                print(f"[OK] Tablas encontradas ({len(tablas)}):")
                for tabla in tablas:
                    print(f"  - {tabla[0]}")
            else:
                print("[ERROR] No se encontraron tablas en el schema 'SC_TiendaOline'")
                print("  Debes ejecutar el script SQL para crear las tablas")
            
    except Exception as e:
        print("[ERROR] Error de conexion:")
        print(f"  {str(e)}")
        print()
        print("Posibles soluciones:")
        print("1. Verifica que SQL Server este ejecutandose")
        print("2. Verifica el nombre de la instancia en settings.py")
        print("3. Verifica que el puerto TCP/IP este habilitado")
        print("4. Revisa CONEXION_SQL_SERVER.md para mas detalles")
        return False
    
    return True

if __name__ == '__main__':
    verificar_conexion()

