-- Script para crear las tablas de Django necesarias en SQL Server
-- Ejecuta este script en SQL Server Management Studio
-- IMPORTANTE: Django busca estas tablas en el schema 'dbo' por defecto, no en 'SC_TiendaOline'

USE DB_TiendaOnline
GO

-- Crear tabla django_session para manejar sesiones (en schema dbo)
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'django_session' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
    CREATE TABLE dbo.django_session (
        session_key NVARCHAR(40) NOT NULL PRIMARY KEY,
        session_data NVARCHAR(MAX) NOT NULL,
        expire_date DATETIME2 NOT NULL
    )
    
    CREATE INDEX django_session_expire_date ON dbo.django_session(expire_date)
    
    PRINT 'Tabla django_session creada exitosamente en schema dbo'
END
ELSE
BEGIN
    PRINT 'La tabla django_session ya existe en schema dbo'
END
GO

-- Crear tabla django_migrations para rastrear migraciones (en schema dbo)
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'django_migrations' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
    CREATE TABLE dbo.django_migrations (
        id INT IDENTITY(1,1) PRIMARY KEY,
        app NVARCHAR(255) NOT NULL,
        name NVARCHAR(255) NOT NULL,
        applied DATETIME2 NOT NULL DEFAULT GETDATE()
    )
    
    CREATE INDEX django_migrations_app ON dbo.django_migrations(app)
    
    PRINT 'Tabla django_migrations creada exitosamente en schema dbo'
END
ELSE
BEGIN
    PRINT 'La tabla django_migrations ya existe en schema dbo'
END
GO

-- Crear tabla django_content_type (necesaria para el sistema de contenido de Django) (en schema dbo)
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'django_content_type' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
    CREATE TABLE dbo.django_content_type (
        id INT IDENTITY(1,1) PRIMARY KEY,
        app_label NVARCHAR(100) NOT NULL,
        model NVARCHAR(100) NOT NULL
    )
    
    CREATE UNIQUE INDEX django_content_type_app_label_model ON dbo.django_content_type(app_label, model)
    
    PRINT 'Tabla django_content_type creada exitosamente en schema dbo'
END
ELSE
BEGIN
    PRINT 'La tabla django_content_type ya existe en schema dbo'
END
GO

PRINT 'Todas las tablas de Django han sido creadas o ya existen en schema dbo'
GO

