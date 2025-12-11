"""
Comando para verificar las tablas de Django.
Ejecuta: python manage.py verificar_tablas_django
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Verifica que las tablas del sistema de Django existan'

    def handle(self, *args, **options):
        self.stdout.write('Verificando tablas del sistema de Django...\n')
        
        with connection.cursor() as cursor:
            # Verificar django_session
            cursor.execute("""
                SELECT 
                    t.name AS tabla,
                    s.name AS schema_name,
                    CASE WHEN t.name IS NOT NULL THEN 'EXISTE' ELSE 'NO EXISTE' END AS estado
                FROM sys.tables t
                INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
                WHERE t.name = 'django_session'
            """)
            resultados = cursor.fetchall()
            
            if resultados:
                for row in resultados:
                    self.stdout.write(f'[OK] Tabla: {row[0]}, Schema: {row[1]}, Estado: {row[2]}')
            else:
                self.stdout.write(self.style.ERROR('[ERROR] Tabla django_session NO encontrada'))
            
            # Verificar django_migrations
            cursor.execute("""
                SELECT 
                    t.name AS tabla,
                    s.name AS schema_name,
                    CASE WHEN t.name IS NOT NULL THEN 'EXISTE' ELSE 'NO EXISTE' END AS estado
                FROM sys.tables t
                INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
                WHERE t.name = 'django_migrations'
            """)
            resultados = cursor.fetchall()
            
            if resultados:
                for row in resultados:
                    self.stdout.write(f'[OK] Tabla: {row[0]}, Schema: {row[1]}, Estado: {row[2]}')
            else:
                self.stdout.write(self.style.ERROR('[ERROR] Tabla django_migrations NO encontrada'))
            
            # Verificar django_content_type
            cursor.execute("""
                SELECT 
                    t.name AS tabla,
                    s.name AS schema_name,
                    CASE WHEN t.name IS NOT NULL THEN 'EXISTE' ELSE 'NO EXISTE' END AS estado
                FROM sys.tables t
                INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
                WHERE t.name = 'django_content_type'
            """)
            resultados = cursor.fetchall()
            
            if resultados:
                for row in resultados:
                    self.stdout.write(f'[OK] Tabla: {row[0]}, Schema: {row[1]}, Estado: {row[2]}')
            else:
                self.stdout.write(self.style.ERROR('[ERROR] Tabla django_content_type NO encontrada'))
            
            # Verificar todas las tablas que empiezan con django_
            self.stdout.write('\nTodas las tablas django_* encontradas:')
            cursor.execute("""
                SELECT 
                    s.name AS schema_name,
                    t.name AS tabla
                FROM sys.tables t
                INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
                WHERE t.name LIKE 'django_%'
                ORDER BY s.name, t.name
            """)
            todas = cursor.fetchall()
            if todas:
                for row in todas:
                    self.stdout.write(f'  - {row[1]} (schema: {row[0]})')
            else:
                self.stdout.write(self.style.WARNING('  No se encontraron tablas django_*'))

