# Configuración de Conexión a SQL Server

## Problema de Conexión

Si recibes el error:
```
pyodbc.OperationalError: TCP Provider: No connection could be made because the target machine actively refused it
```

Esto significa que Django no puede conectarse a SQL Server. Sigue estos pasos:

## Soluciones

### 1. Verificar que SQL Server esté ejecutándose

- Abre **SQL Server Configuration Manager**
- Verifica que **SQL Server (SQLEXPRESS)** o tu instancia esté **Running**
- Si no está corriendo, inícialo

### 2. Verificar la configuración en `settings.py`

La configuración actual es:
```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'DB_TiendaOnline',
        'HOST': 'localhost',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'trusted_connection': 'yes',
            'instance': 'SQLEXPRESS',  # Cambia esto si tu instancia tiene otro nombre
        },
    }
}
```

### 3. Verificar el nombre de la instancia

Si tu instancia de SQL Server tiene un nombre diferente a `SQLEXPRESS`:

1. Abre **SQL Server Management Studio (SSMS)**
2. Conéctate al servidor y verifica el nombre de la instancia
3. Actualiza `'instance': 'TU_INSTANCIA'` en `settings.py`

### 4. Si no usas una instancia nombrada

Si usas la instancia por defecto (MSSQLSERVER), elimina la línea `'instance'`:

```python
'OPTIONS': {
    'driver': 'ODBC Driver 17 for SQL Server',
    'trusted_connection': 'yes',
    # Elimina 'instance': 'SQLEXPRESS',
},
```

### 5. Verificar que el puerto TCP/IP esté habilitado

1. Abre **SQL Server Configuration Manager**
2. Ve a **SQL Server Network Configuration** > **Protocols for SQLEXPRESS**
3. Asegúrate de que **TCP/IP** esté **Enabled**
4. Reinicia el servicio SQL Server

### 6. Verificar el puerto

El puerto por defecto es 1433, pero si tu instancia usa otro puerto:

1. En **SQL Server Configuration Manager**, ve a **TCP/IP Properties**
2. Ve a la pestaña **IP Addresses**
3. Busca **IPAll** y verifica el **TCP Dynamic Ports** o **TCP Port**
4. Actualiza `'PORT': '1433'` en `settings.py` si es necesario

### 7. Si usas autenticación SQL Server (no Windows)

Si no usas autenticación Windows, actualiza la configuración:

```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'DB_TiendaOnline',
        'HOST': 'localhost',
        'PORT': '1433',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            # Elimina 'trusted_connection': 'yes',
        },
    }
}
```

## Verificar la Conexión

Para verificar que la base de datos existe y está accesible:

1. Abre **SQL Server Management Studio**
2. Conéctate al servidor
3. Verifica que la base de datos `DB_TiendaOnline` existe
4. Verifica que el schema `SC_TiendaOline` existe
5. Verifica que todas las tablas están creadas según el script SQL proporcionado

## Verificar la Conexión con el Script

He creado un script de verificación que puedes ejecutar:

```bash
python verificar_conexion.py
```

Este script:
- Intenta conectarse a SQL Server
- Verifica que la base de datos existe
- Verifica que el schema existe
- Lista todas las tablas encontradas

## Nota Importante

El proyecto está configurado con `managed = False` en todos los modelos, lo que significa que Django NO creará las tablas automáticamente. Debes ejecutar el script SQL proporcionado para crear la base de datos y las tablas antes de usar el proyecto.

## Solución Rápida

Si necesitas que el servidor inicie sin verificar la conexión (solo para desarrollo), puedes comentar temporalmente la verificación de migraciones, pero esto NO es recomendado para producción.

