# Solución al Error de Conexión SQL Server

## Error Actual
```
Named Pipes Provider: Could not open a connection to SQL Server [2]
```

Este error indica que SQL Server está intentando usar **Named Pipes** en lugar de **TCP/IP**.

## Soluciones Paso a Paso

### 1. Verificar que SQL Server esté ejecutándose

1. Abre **SQL Server Configuration Manager**
2. Ve a **SQL Server Services**
3. Verifica que **SQL Server (SQLEXPRESS01)** esté en estado **Running**
4. Si no está corriendo, haz clic derecho > **Start**

### 2. Habilitar TCP/IP (MUY IMPORTANTE)

1. En **SQL Server Configuration Manager**, ve a:
   - **SQL Server Network Configuration** > **Protocols for SQLEXPRESS01**
2. Haz clic derecho en **TCP/IP** y selecciona **Enable**
3. Haz clic derecho en **TCP/IP** > **Properties**
4. Ve a la pestaña **IP Addresses**
5. Desplázate hasta **IPAll**
6. Anota el número en **TCP Dynamic Ports** (ej: 49152) o **TCP Port** (si está configurado)
7. Si está vacío, puedes configurar un puerto fijo (ej: 1433)
8. Haz clic en **OK**
9. **REINICIA el servicio SQL Server (SQLEXPRESS01)**

### 3. Verificar el puerto de la instancia

Si tu instancia usa un puerto dinámico (no 1433), necesitas:

1. En **SQL Server Configuration Manager**, ve a **TCP/IP Properties** > **IP Addresses** > **IPAll**
2. Anota el **TCP Dynamic Ports** (ej: 49152)
3. Actualiza `settings.py` con ese puerto:

```python
'PORT': '49152',  # El puerto que encontraste
```

### 4. Configuración Alternativa - Si el puerto dinámico no funciona

Si tu instancia usa un puerto dinámico y no puedes conectarte, puedes:

**Opción A: Configurar un puerto fijo**
1. En **TCP/IP Properties** > **IPAll**
2. Deja **TCP Dynamic Ports** vacío
3. Configura **TCP Port** con un número (ej: 1433 o 1434)
4. Reinicia SQL Server
5. Actualiza `settings.py`:

```python
'PORT': '1433',  # El puerto que configuraste
```

**Opción B: Usar el formato de servidor completo**

Si nada funciona, intenta esta configuración:

```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'DB_TiendaOnline',
        'HOST': 'localhost\\SQLEXPRESS01',  # Formato con instancia
        'PORT': '',  # Vacío
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'trusted_connection': 'yes',
        },
    }
}
```

### 5. Verificar que Named Pipes esté deshabilitado (opcional)

Si quieres forzar solo TCP/IP:

1. En **SQL Server Network Configuration** > **Protocols for SQLEXPRESS01**
2. Haz clic derecho en **Named Pipes** > **Disable**
3. Reinicia SQL Server

### 6. Verificar la conexión desde SQL Server Management Studio

Antes de probar con Django, verifica que puedes conectarte desde SSMS:

1. Abre **SQL Server Management Studio (SSMS)**
2. En **Server name**, usa: `localhost\SQLEXPRESS01` o `localhost,49152` (con el puerto)
3. Si puedes conectarte desde SSMS, entonces el problema es la configuración de Django
4. Si NO puedes conectarte desde SSMS, el problema es la configuración de SQL Server

### 7. Verificar el nombre exacto de la instancia

El nombre de la instancia debe ser EXACTO. Para verificar:

1. Abre **SQL Server Configuration Manager**
2. Ve a **SQL Server Services**
3. Busca el servicio que dice algo como: **SQL Server (SQLEXPRESS01)**
4. El nombre entre paréntesis es el nombre de la instancia
5. Asegúrate de que en `settings.py` uses exactamente ese nombre (sin paréntesis)

## Configuración Final Recomendada

Una vez que hayas verificado el puerto, usa esta configuración:

```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'DB_TiendaOnline',
        'HOST': 'localhost',
        'PORT': '1433',  # O el puerto que encontraste
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'trusted_connection': 'yes',
            'instance': 'SQLEXPRESS01',
        },
    }
}
```

## Probar la Conexión

Ejecuta:
```bash
python verificar_conexion.py
```

Si aún no funciona, ejecuta:
```bash
python manage.py runserver
```

Y comparte el error completo para ayudarte mejor.


