# Solución: Error de Tabla django_session

## Problema

Al intentar iniciar sesión, aparece el error:
```
Invalid object name 'django_session'
```

## Causa

Django necesita crear sus propias tablas para funcionalidades del sistema (sesiones, migraciones, etc.), pero como todos los modelos de la aplicación tienen `managed = False`, Django no puede crear estas tablas automáticamente.

## Solución

He creado un script SQL (`crear_tablas_django.sql`) que crea las tablas necesarias de Django.

### Pasos para Solucionar:

1. **Abre SQL Server Management Studio (SSMS)**

2. **Conéctate a tu servidor SQL Server**

3. **Ejecuta el script `crear_tablas_django.sql`**

   - Abre el archivo `crear_tablas_django.sql` en SSMS
   - Asegúrate de estar conectado a la base de datos `DB_TiendaOnline`
   - Ejecuta el script completo (F5)

4. **Verifica que las tablas se crearon**

   Puedes verificar ejecutando:
   ```sql
   SELECT name FROM sys.tables WHERE name LIKE 'django_%'
   ```

   Deberías ver:
   - `django_session`
   - `django_migrations`
   - `django_content_type`

5. **Reinicia el servidor de Django**

   ```bash
   python manage.py runserver
   ```

## Tablas que se Crean

El script crea las siguientes tablas en el schema `dbo`:

1. **django_session**: Almacena las sesiones de los usuarios
2. **django_migrations**: Rastrea las migraciones aplicadas
3. **django_content_type**: Sistema de tipos de contenido de Django

## Nota Importante

Estas tablas se crean en el schema `dbo` (por defecto), no en `SC_TiendaOline`, porque Django busca estas tablas en el schema por defecto de la base de datos.

Las tablas de tu aplicación (Usuario, Producto, Carrito, etc.) permanecen en el schema `SC_TiendaOline` como está definido en los modelos.

## Verificación

Después de ejecutar el script, intenta iniciar sesión nuevamente. El error debería desaparecer.


