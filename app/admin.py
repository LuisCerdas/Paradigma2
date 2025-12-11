from django.contrib import admin
from .models import Usuario, Direccion, Producto, Carrito, Pedido

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nombre_usuario', 'apellido_usuario', 'email_usuario', 'rol_usuario', 'activo_usuario', 'fecha_registro_usuario')
    list_filter = ('rol_usuario', 'activo_usuario', 'fecha_registro_usuario')
    search_fields = ('nombre_usuario', 'apellido_usuario', 'email_usuario')
    readonly_fields = ('id_usuario', 'fecha_registro_usuario')

@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('id_direccion', 'id_usuario', 'provincia_direccion', 'canton_direccion', 'predeterminada_direccion')
    list_filter = ('provincia_direccion', 'predeterminada_direccion')
    search_fields = ('id_usuario__nombre_usuario', 'id_usuario__apellido_usuario', 'direccion_detallada_direccion')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'nombre_producto', 'categoria_producto', 'precio_producto', 'stock_producto', 'activo_producto', 'fecha_creacion_producto')
    list_filter = ('categoria_producto', 'activo_producto', 'fecha_creacion_producto')
    search_fields = ('nombre_producto', 'codigo_producto', 'descripcion_producto')
    readonly_fields = ('id_producto', 'fecha_creacion_producto', 'fecha_actualizacion_producto')

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('id_carrito', 'id_usuario', 'id_producto', 'cantidad_carrito', 'precio_unitario_carrito', 'subtotal_carrito', 'estado_carrito', 'fecha_creacion_carrito')
    list_filter = ('estado_carrito', 'fecha_creacion_carrito')
    search_fields = ('id_usuario__nombre_usuario', 'id_producto__nombre_producto')
    readonly_fields = ('id_carrito', 'subtotal_carrito', 'fecha_creacion_carrito', 'fecha_actualizacion_carrito')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id_pedido', 'id_usuario', 'id_producto', 'cantidad_pedido', 'monto_total_pedido', 'metodo_pago_pedido', 'estado_pedido', 'fecha_pedido_pedido')
    list_filter = ('estado_pedido', 'metodo_pago_pedido', 'fecha_pedido_pedido')
    search_fields = ('id_usuario__nombre_usuario', 'id_producto__nombre_producto', 'referencia_transaccion_pedido')
    readonly_fields = ('id_pedido', 'subtotal_pedido', 'fecha_pedido_pedido')
