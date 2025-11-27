from django.db import models

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=150)
    descripcion_producto = models.TextField(null=True)
    categoria_producto = models.CharField(max_length=100, null=True)
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2)
    stock_producto = models.IntegerField(null=True)
    imagen_producto = models.CharField(max_length=255, null=True)
    codigo_producto = models.CharField(max_length=50, null=True)
    activo_producto = models.BooleanField(null=True)

    class Meta:
        managed = False
        db_table = 'SC_TiendaOline.T_Producto'