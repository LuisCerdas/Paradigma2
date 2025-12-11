"""
Comando de Django para crear las tablas del sistema de Django automáticamente.
Ejecuta: python manage.py crear_tablas_django
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Crea las tablas del sistema de Django (django_session, django_migrations, django_content_type)'

    def handle(self, *args, **options):
        self.stdout.write('Creando tablas del sistema de Django...')
        
        with connection.cursor() as cursor:
            # Crear tabla django_session
            try:
                cursor.execute("""
                    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'django_session' AND schema_id = SCHEMA_ID('dbo'))
                    BEGIN
                        CREATE TABLE dbo.django_session (
                            session_key NVARCHAR(40) NOT NULL PRIMARY KEY,
                            session_data NVARCHAR(MAX) NOT NULL,
                            expire_date DATETIME2 NOT NULL
                        )
                        
                        CREATE INDEX django_session_expire_date ON dbo.django_session(expire_date)
                        
                        SELECT 'Tabla django_session creada exitosamente'
                    END
                    ELSE
                    BEGIN
                        SELECT 'La tabla django_session ya existe'
                    END
                """)
                result = cursor.fetchone()
                self.stdout.write(self.style.SUCCESS(f'[OK] {result[0]}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'[ERROR] Error al crear django_session: {str(e)}'))
            
            # Crear tabla django_migrations
            try:
                cursor.execute("""
                    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'django_migrations' AND schema_id = SCHEMA_ID('dbo'))
                    BEGIN
                        CREATE TABLE dbo.django_migrations (
                            id INT IDENTITY(1,1) PRIMARY KEY,
                            app NVARCHAR(255) NOT NULL,
                            name NVARCHAR(255) NOT NULL,
                            applied DATETIME2 NOT NULL DEFAULT GETDATE()
                        )
                        
                        CREATE INDEX django_migrations_app ON dbo.django_migrations(app)
                        
                        SELECT 'Tabla django_migrations creada exitosamente'
                    END
                    ELSE
                    BEGIN
                        SELECT 'La tabla django_migrations ya existe'
                    END
                """)
                result = cursor.fetchone()
                self.stdout.write(self.style.SUCCESS(f'[OK] {result[0]}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'[ERROR] Error al crear django_migrations: {str(e)}'))
            
            # Crear tabla django_content_type
            try:
                cursor.execute("""
                    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'django_content_type' AND schema_id = SCHEMA_ID('dbo'))
                    BEGIN
                        CREATE TABLE dbo.django_content_type (
                            id INT IDENTITY(1,1) PRIMARY KEY,
                            app_label NVARCHAR(100) NOT NULL,
                            model NVARCHAR(100) NOT NULL
                        )
                        
                        CREATE UNIQUE INDEX django_content_type_app_label_model ON dbo.django_content_type(app_label, model)
                        
                        SELECT 'Tabla django_content_type creada exitosamente'
                    END
                    ELSE
                    BEGIN
                        SELECT 'La tabla django_content_type ya existe'
                    END
                """)
                result = cursor.fetchone()
                self.stdout.write(self.style.SUCCESS(f'[OK] {result[0]}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'[ERROR] Error al crear django_content_type: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS('\n[OK] Proceso completado. Las tablas de Django estan listas.'))

