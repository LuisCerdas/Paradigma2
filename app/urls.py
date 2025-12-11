from django.urls import path
from . import views

urlpatterns = [
    # Vistas principales
    path("", views.home, name='home'),
    
    # Autenticación
    path("registro/", views.registro, name='registro'),
    path("login/", views.login, name='login'),
    path("logout/", views.logout, name='logout'),
    path("perfil/", views.perfil, name='perfil'),
    path("perfil/direccion/agregar/", views.agregar_direccion, name='agregar_direccion'),
    
    # Carrito
    path("carrito/", views.ver_carrito, name='ver_carrito'),
    path("carrito/agregar/<int:producto_id>/", views.agregar_al_carrito, name='agregar_al_carrito'),
    path("carrito/actualizar/<int:carrito_id>/", views.actualizar_carrito, name='actualizar_carrito'),
    path("carrito/eliminar/<int:carrito_id>/", views.eliminar_del_carrito, name='eliminar_del_carrito'),
    
    # Checkout y Pedidos
    path("checkout/", views.checkout, name='checkout'),
    path("mis-pedidos/", views.mis_pedidos, name='mis_pedidos'),
    
    # CRUD Productos (Admin)
    path("admin/productos/", views.listar_productos, name='listar_productos'),
    path("admin/productos/crear/", views.crear_producto, name='crear_producto'),
    path("admin/productos/editar/<int:producto_id>/", views.editar_producto, name='editar_producto'),
    path("admin/productos/eliminar/<int:producto_id>/", views.eliminar_producto, name='eliminar_producto'),
]
