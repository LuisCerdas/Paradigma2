from .models import Carrito, Usuario

def cart_context(request):
    """
    Context processor para agregar información del carrito a todos los templates
    """
    cart_count = 0
    cart_total = 0
    
    # Si hay un usuario autenticado (usando sesión)
    if hasattr(request, 'session') and 'usuario_id' in request.session:
        usuario_id = request.session.get('usuario_id')
        try:
            usuario = Usuario.objects.get(id_usuario=usuario_id)
            carritos = Carrito.objects.filter(
                id_usuario=usuario,
                estado_carrito='activo'
            )
            cart_count = carritos.count()
            cart_total = sum(float(carrito.subtotal_carrito) for carrito in carritos)
        except Usuario.DoesNotExist:
            pass
    
    return {
        'cart_count': cart_count,
        'cart_total': cart_total,
    }


