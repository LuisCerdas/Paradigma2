from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, F, Q
from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password
from .models import Producto, Usuario, Direccion, Carrito, Pedido

def home(request):
    """Vista principal - muestra todos los productos activos"""
    productos = Producto.objects.filter(activo_producto=True)
    
    # Filtro por categoría si se proporciona
    categoria = request.GET.get('categoria')
    if categoria:
        productos = productos.filter(categoria_producto=categoria)
    
    # Búsqueda si se proporciona
    busqueda = request.GET.get('busqueda')
    if busqueda:
        productos = productos.filter(
            Q(nombre_producto__icontains=busqueda) |
            Q(descripcion_producto__icontains=busqueda)
        )
    
    categorias = Producto.objects.values_list('categoria_producto', flat=True).distinct().exclude(categoria_producto__isnull=True)
    
    return render(request, 'app/index.html', {
        'productos': productos,
        'categorias': categorias,
    })

def agregar_al_carrito(request, producto_id):
    """Agrega un producto al carrito"""
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id_producto=producto_id, activo_producto=True)
        cantidad = int(request.POST.get('cantidad', 1))
        
        if cantidad <= 0:
            messages.error(request, 'La cantidad debe ser mayor a 0')
            return redirect('home')
        
        if cantidad > producto.stock_producto:
            messages.error(request, 'No hay suficiente stock disponible')
            return redirect('home')
        
        # Obtener o crear usuario (simplificado - en producción usar autenticación real)
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            # Crear usuario temporal o redirigir a login
            messages.error(request, 'Debes iniciar sesión para agregar productos al carrito')
            return redirect('home')
        
        try:
            usuario = Usuario.objects.get(id_usuario=usuario_id)
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')
            return redirect('home')
        
        # Verificar si ya existe el producto en el carrito activo
        carrito_existente = Carrito.objects.filter(
            id_usuario=usuario,
            id_producto=producto,
            estado_carrito='activo'
        ).first()
        
        if carrito_existente:
            nueva_cantidad = carrito_existente.cantidad_carrito + cantidad
            if nueva_cantidad > producto.stock_producto:
                messages.error(request, 'No hay suficiente stock disponible')
                return redirect('home')
            
            # Usar update() para evitar que Django intente modificar subtotal_carrito (columna calculada)
            Carrito.objects.filter(id_carrito=carrito_existente.id_carrito).update(
                cantidad_carrito=nueva_cantidad
            )
            messages.success(request, f'Cantidad actualizada en el carrito')
        else:
            # SQL Server calculará automáticamente el subtotal_carrito (columna calculada)
            # Usar raw SQL para evitar que Django intente incluir el campo calculado
            from django.db import connection
            with connection.cursor() as cursor:
                # Usar %s como placeholder (Django lo convertirá a ? para SQL Server)
                cursor.execute("""
                    INSERT INTO [SC_TiendaOline].[T_Carrito] 
                    (id_usuario, id_producto, cantidad_carrito, precio_unitario_carrito, estado_carrito)
                    VALUES (%s, %s, %s, %s, %s)
                """, [
                    usuario.id_usuario,
                    producto.id_producto,
                    cantidad,
                    producto.precio_producto,
                    'activo'
                ])
            messages.success(request, f'{producto.nombre_producto} agregado al carrito')
        
        return redirect('ver_carrito')
    
    return redirect('home')

def ver_carrito(request):
    """Muestra el contenido del carrito"""
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.info(request, 'Debes iniciar sesión para ver tu carrito')
        return redirect('home')
    
    try:
        usuario = Usuario.objects.get(id_usuario=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        return redirect('home')
    
    carritos = Carrito.objects.filter(id_usuario=usuario, estado_carrito='activo')
    total = sum(float(carrito.subtotal_carrito) for carrito in carritos)
    
    return render(request, 'app/carrito.html', {
        'carritos': carritos,
        'total': total,
    })

def actualizar_carrito(request, carrito_id):
    """Actualiza la cantidad de un item en el carrito"""
    if request.method == 'POST':
        carrito = get_object_or_404(Carrito, id_carrito=carrito_id, estado_carrito='activo')
        nueva_cantidad = int(request.POST.get('cantidad', 1))
        
        if nueva_cantidad <= 0:
            carrito.delete()
            messages.success(request, 'Producto eliminado del carrito')
        else:
            if nueva_cantidad > carrito.id_producto.stock_producto:
                messages.error(request, 'No hay suficiente stock disponible')
                return redirect('ver_carrito')
            
            # Usar update() para evitar que Django intente modificar subtotal_carrito (columna calculada)
            Carrito.objects.filter(id_carrito=carrito.id_carrito).update(
                cantidad_carrito=nueva_cantidad
            )
            messages.success(request, 'Carrito actualizado')
        
        return redirect('ver_carrito')
    
    return redirect('ver_carrito')

def eliminar_del_carrito(request, carrito_id):
    """Elimina un item del carrito"""
    carrito = get_object_or_404(Carrito, id_carrito=carrito_id, estado_carrito='activo')
    carrito.delete()
    messages.success(request, 'Producto eliminado del carrito')
    return redirect('ver_carrito')

def checkout(request):
    """Proceso de checkout"""
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.info(request, 'Debes iniciar sesión para realizar un pedido')
        return redirect('home')
    
    try:
        usuario = Usuario.objects.get(id_usuario=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        return redirect('home')
    
    carritos = Carrito.objects.filter(id_usuario=usuario, estado_carrito='activo')
    
    if not carritos.exists():
        messages.info(request, 'Tu carrito está vacío')
        return redirect('ver_carrito')
    
    direcciones = Direccion.objects.filter(id_usuario=usuario)
    
    if request.method == 'POST':
        direccion_id = request.POST.get('direccion_id')
        metodo_pago = request.POST.get('metodo_pago')
        referencia_transaccion = request.POST.get('referencia_transaccion', '')
        
        if not direccion_id or not metodo_pago:
            messages.error(request, 'Por favor completa todos los campos requeridos')
            return render(request, 'app/checkout.html', {
                'carritos': carritos,
                'direcciones': direcciones,
                'total': sum(float(carrito.subtotal_carrito) for carrito in carritos),
            })
        
        try:
            direccion = Direccion.objects.get(id_direccion=direccion_id, id_usuario=usuario)
        except Direccion.DoesNotExist:
            messages.error(request, 'Dirección no encontrada')
            return render(request, 'app/checkout.html', {
                'carritos': carritos,
                'direcciones': direcciones,
                'total': sum(float(carrito.subtotal_carrito) for carrito in carritos),
            })
        
        # Crear pedidos para cada item del carrito
        with transaction.atomic():
            for carrito in carritos:
                # Verificar stock
                if carrito.cantidad_carrito > carrito.id_producto.stock_producto:
                    messages.error(request, f'No hay suficiente stock para {carrito.id_producto.nombre_producto}')
                    return redirect('ver_carrito')
                
                # Calcular totales
                subtotal = float(carrito.subtotal_carrito)
                descuento = 0  # Puede ser calculado según reglas de negocio
                monto_total = subtotal - descuento
                
                # Crear pedido usando SQL directo para evitar incluir subtotal_pedido (columna calculada)
                from django.db import connection
                from django.utils import timezone
                with connection.cursor() as cursor:
                    # Usar timezone.now() para la fecha (Django lo convertirá al formato correcto)
                    cursor.execute("""
                        INSERT INTO [SC_TiendaOline].[T_Pedido] 
                        (id_usuario, id_direccion, id_producto, cantidad_pedido, precio_unitario_pedido, 
                         descuento_pedido, monto_total_pedido, metodo_pago_pedido, referencia_transaccion_pedido, 
                         fecha_pedido_pedido, estado_pedido)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, [
                        usuario.id_usuario,
                        direccion.id_direccion,
                        carrito.id_producto.id_producto,
                        carrito.cantidad_carrito,
                        carrito.precio_unitario_carrito,
                        descuento,
                        monto_total,
                        metodo_pago,
                        referencia_transaccion if referencia_transaccion else None,
                        timezone.now(),
                        'pendiente'
                    ])
                
                # Actualizar stock
                carrito.id_producto.stock_producto -= carrito.cantidad_carrito
                carrito.id_producto.save()
                
                # Marcar carrito como convertido (usar update() para evitar modificar subtotal_carrito)
                Carrito.objects.filter(id_carrito=carrito.id_carrito).update(
                    estado_carrito='convertido'
                )
            
            messages.success(request, 'Pedido realizado exitosamente')
            return redirect('mis_pedidos')
    
    total = sum(float(carrito.subtotal_carrito) for carrito in carritos)
    
    return render(request, 'app/checkout.html', {
        'carritos': carritos,
        'direcciones': direcciones,
        'total': total,
    })

def mis_pedidos(request):
    """Muestra los pedidos del usuario"""
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.info(request, 'Debes iniciar sesión para ver tus pedidos')
        return redirect('home')
    
    try:
        usuario = Usuario.objects.get(id_usuario=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        return redirect('home')
    
    pedidos = Pedido.objects.filter(id_usuario=usuario).order_by('-fecha_pedido_pedido')
    
    return render(request, 'app/mis_pedidos.html', {
        'pedidos': pedidos,
    })

# Vistas CRUD para Productos (Admin)
def listar_productos(request):
    """Lista todos los productos (admin)"""
    productos = Producto.objects.all()
    return render(request, 'app/admin/productos_list.html', {'productos': productos})

def crear_producto(request):
    """Crea un nuevo producto (admin)"""
    if request.method == 'POST':
        try:
            Producto.objects.create(
                nombre_producto=request.POST.get('nombre_producto'),
                descripcion_producto=request.POST.get('descripcion_producto', ''),
                categoria_producto=request.POST.get('categoria_producto', ''),
                precio_producto=request.POST.get('precio_producto'),
                stock_producto=request.POST.get('stock_producto', 0),
                imagen_producto=request.POST.get('imagen_producto', ''),
                codigo_producto=request.POST.get('codigo_producto', ''),
                activo_producto=request.POST.get('activo_producto', 'on') == 'on'
            )
            messages.success(request, 'Producto creado exitosamente')
            return redirect('listar_productos')
        except Exception as e:
            messages.error(request, f'Error al crear producto: {str(e)}')
    
    return render(request, 'app/admin/productos_form.html', {'accion': 'Crear'})

def editar_producto(request, producto_id):
    """Edita un producto existente (admin)"""
    producto = get_object_or_404(Producto, id_producto=producto_id)
    
    if request.method == 'POST':
        try:
            producto.nombre_producto = request.POST.get('nombre_producto')
            producto.descripcion_producto = request.POST.get('descripcion_producto', '')
            producto.categoria_producto = request.POST.get('categoria_producto', '')
            producto.precio_producto = request.POST.get('precio_producto')
            producto.stock_producto = request.POST.get('stock_producto', 0)
            producto.imagen_producto = request.POST.get('imagen_producto', '')
            producto.codigo_producto = request.POST.get('codigo_producto', '')
            producto.activo_producto = request.POST.get('activo_producto', 'on') == 'on'
            producto.save()
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('listar_productos')
        except Exception as e:
            messages.error(request, f'Error al actualizar producto: {str(e)}')
    
    return render(request, 'app/admin/productos_form.html', {
        'producto': producto,
        'accion': 'Editar'
    })

def eliminar_producto(request, producto_id):
    """Elimina un producto (admin)"""
    producto = get_object_or_404(Producto, id_producto=producto_id)
    
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente')
        return redirect('listar_productos')
    
    return render(request, 'app/admin/productos_confirm_delete.html', {'producto': producto})

# Vistas de Autenticación
def registro(request):
    """Registro de nuevos usuarios"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre_usuario')
        apellido = request.POST.get('apellido_usuario')
        email = request.POST.get('email_usuario')
        password = request.POST.get('contraseña_usuario')
        telefono = request.POST.get('telefono_usuario', '')
        
        if not all([nombre, apellido, email, password]):
            messages.error(request, 'Por favor completa todos los campos requeridos')
            return render(request, 'app/registro.html')
        
        # Verificar si el email ya existe
        if Usuario.objects.filter(email_usuario=email).exists():
            messages.error(request, 'Este email ya está registrado')
            return render(request, 'app/registro.html')
        
        try:
            usuario = Usuario.objects.create(
                nombre_usuario=nombre,
                apellido_usuario=apellido,
                email_usuario=email,
                contraseña_usuario=make_password(password),
                telefono_usuario=telefono,
                rol_usuario='cliente',
                activo_usuario=True
            )
            messages.success(request, 'Registro exitoso. Por favor inicia sesión')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error al registrar: {str(e)}')
    
    return render(request, 'app/registro.html')

def login(request):
    """Inicio de sesión"""
    if request.method == 'POST':
        email = request.POST.get('email_usuario')
        password = request.POST.get('contraseña_usuario')
        
        if not email or not password:
            messages.error(request, 'Por favor completa todos los campos')
            return render(request, 'app/login.html')
        
        try:
            usuario = Usuario.objects.get(email_usuario=email, activo_usuario=True)
            if check_password(password, usuario.contraseña_usuario):
                request.session['usuario_id'] = usuario.id_usuario
                request.session['usuario_nombre'] = f"{usuario.nombre_usuario} {usuario.apellido_usuario}"
                request.session['usuario_rol'] = usuario.rol_usuario
                messages.success(request, f'Bienvenido, {usuario.nombre_usuario}!')
                return redirect('home')
            else:
                messages.error(request, 'Contraseña incorrecta')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado o inactivo')
    
    return render(request, 'app/login.html')

def logout(request):
    """Cerrar sesión"""
    request.session.flush()
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('home')

def perfil(request):
    """Perfil del usuario"""
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.info(request, 'Debes iniciar sesión para ver tu perfil')
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id_usuario=usuario_id)
        direcciones = Direccion.objects.filter(id_usuario=usuario)
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        return redirect('home')
    
    return render(request, 'app/perfil.html', {
        'usuario': usuario,
        'direcciones': direcciones,
    })

def agregar_direccion(request):
    """Agregar una nueva dirección"""
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.info(request, 'Debes iniciar sesión')
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id_usuario=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        return redirect('home')
    
    if request.method == 'POST':
        provincia = request.POST.get('provincia_direccion', '')
        canton = request.POST.get('canton_direccion', '')
        distrito = request.POST.get('distrito_direccion', '')
        direccion_detallada = request.POST.get('direccion_detallada_direccion', '')
        predeterminada = request.POST.get('predeterminada_direccion') == 'on'
        
        # Si se marca como predeterminada, desmarcar las demás
        if predeterminada:
            Direccion.objects.filter(id_usuario=usuario).update(predeterminada_direccion=False)
        
        try:
            Direccion.objects.create(
                id_usuario=usuario,
                provincia_direccion=provincia,
                canton_direccion=canton,
                distrito_direccion=distrito,
                direccion_detallada_direccion=direccion_detallada,
                predeterminada_direccion=predeterminada
            )
            messages.success(request, 'Dirección agregada exitosamente')
            return redirect('perfil')
        except Exception as e:
            messages.error(request, f'Error al agregar dirección: {str(e)}')
    
    return render(request, 'app/agregar_direccion.html')
