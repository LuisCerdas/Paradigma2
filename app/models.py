from django.db import models
from django.core.validators import MinValueValidator

# Modelo Usuario - coincide con T_Usuario
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True, db_column='id_usuario')
    nombre_usuario = models.CharField(max_length=100, db_column='nombre_usuario')
    apellido_usuario = models.CharField(max_length=100, db_column='apellido_usuario')
    email_usuario = models.CharField(max_length=150, unique=True, db_column='email_usuario')
    contraseña_usuario = models.CharField(max_length=255, db_column='contraseña_usuario')
    telefono_usuario = models.CharField(max_length=20, null=True, blank=True, db_column='telefono_usuario')
    fecha_registro_usuario = models.DateTimeField(auto_now_add=True, db_column='fecha_registro_usuario')
    rol_usuario = models.CharField(max_length=50, default='cliente', db_column='rol_usuario')
    activo_usuario = models.BooleanField(default=True, db_column='activo_usuario')

    class Meta:
        managed = False
        db_table = 'SC_TiendaOline.T_Usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombre_usuario} {self.apellido_usuario}"

# Modelo Direccion - coincide con T__Direccion
class Direccion(models.Model):
    id_direccion = models.AutoField(primary_key=True, db_column='id_direccion')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    provincia_direccion = models.CharField(max_length=100, null=True, blank=True, db_column='provincia_direccion')
    canton_direccion = models.CharField(max_length=100, null=True, blank=True, db_column='canton_direccion')
    distrito_direccion = models.CharField(max_length=100, null=True, blank=True, db_column='distrito_direccion')
    direccion_detallada_direccion = models.CharField(max_length=255, null=True, blank=True, db_column='direccion_detallada_direccion')
    predeterminada_direccion = models.BooleanField(default=False, db_column='predeterminada_direccion')

    class Meta:
        managed = False
        db_table = 'SC_TiendaOline.T__Direccion'
        verbose_name = 'Dirección'
        verbose_name_plural = 'Direcciones'

    def __str__(self):
        return f"{self.direccion_detallada_direccion} - {self.provincia_direccion}"

# Modelo Producto - coincide con T_Producto
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True, db_column='id_producto')
    nombre_producto = models.CharField(max_length=150, db_column='nombre_producto')
    descripcion_producto = models.TextField(null=True, blank=True, db_column='descripcion_producto')
    categoria_producto = models.CharField(max_length=100, null=True, blank=True, db_column='categoria_producto')
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2, db_column='precio_producto')
    stock_producto = models.IntegerField(default=0, db_column='stock_producto')
    imagen_producto = models.CharField(max_length=255, null=True, blank=True, db_column='imagen_producto')
    codigo_producto = models.CharField(max_length=50, unique=True, null=True, blank=True, db_column='codigo_producto')
    activo_producto = models.BooleanField(default=True, db_column='activo_producto')
    fecha_creacion_producto = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion_producto')
    fecha_actualizacion_producto = models.DateTimeField(auto_now=True, db_column='fecha_actualizacion_producto')

    class Meta:
        managed = False
        db_table = 'SC_TiendaOline.T_Producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre_producto

# Modelo Carrito - coincide con T_Carrito
class Carrito(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('convertido', 'Convertido'),
        ('cancelado', 'Cancelado'),
    ]

    id_carrito = models.AutoField(primary_key=True, db_column='id_carrito')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto')
    cantidad_carrito = models.IntegerField(validators=[MinValueValidator(1)], db_column='cantidad_carrito')
    precio_unitario_carrito = models.DecimalField(max_digits=10, decimal_places=2, db_column='precio_unitario_carrito')
    subtotal_carrito = models.DecimalField(max_digits=10, decimal_places=2, db_column='subtotal_carrito', editable=False)
    estado_carrito = models.CharField(max_length=50, default='activo', choices=ESTADO_CHOICES, db_column='estado_carrito')
    fecha_creacion_carrito = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion_carrito')
    fecha_actualizacion_carrito = models.DateTimeField(auto_now=True, db_column='fecha_actualizacion_carrito')

    class Meta:
        managed = False
        db_table = 'SC_TiendaOline.T_Carrito'
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'

    def __str__(self):
        return f"Carrito {self.id_carrito} - {self.id_usuario}"

# Modelo Pedido - coincide con T_Pedido (fusiona Pedido + DetallePedido + Pago)
class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
    ]

    METODO_PAGO_CHOICES = [
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
        ('efectivo', 'Efectivo'),
    ]

    id_pedido = models.AutoField(primary_key=True, db_column='id_pedido')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    id_direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, db_column='id_direccion')
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto')
    cantidad_pedido = models.IntegerField(validators=[MinValueValidator(1)], db_column='cantidad_pedido')
    precio_unitario_pedido = models.DecimalField(max_digits=10, decimal_places=2, db_column='precio_unitario_pedido')
    subtotal_pedido = models.DecimalField(max_digits=10, decimal_places=2, db_column='subtotal_pedido', editable=False)
    descuento_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=0, db_column='descuento_pedido')
    monto_total_pedido = models.DecimalField(max_digits=10, decimal_places=2, db_column='monto_total_pedido')
    metodo_pago_pedido = models.CharField(max_length=50, choices=METODO_PAGO_CHOICES, db_column='metodo_pago_pedido')
    referencia_transaccion_pedido = models.CharField(max_length=100, null=True, blank=True, db_column='referencia_transaccion_pedido')
    fecha_pedido_pedido = models.DateTimeField(auto_now_add=True, db_column='fecha_pedido_pedido')
    estado_pedido = models.CharField(max_length=50, default='pendiente', choices=ESTADO_CHOICES, db_column='estado_pedido')

    class Meta:
        managed = False
        db_table = 'SC_TiendaOline.T_Pedido'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f"Pedido {self.id_pedido} - {self.id_usuario}"
