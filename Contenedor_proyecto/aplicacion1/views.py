# aplicacion1/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login #, User
from django.db import transaction
from .models import Producto, Cliente, Usuario, Venta, DetalleVenta, Proveedor, OrdenCompra, DetalleOrdenCompra
from .forms import ProductoForm, VentaForm, DetalleVentaForm, ClienteForm, ProveedorForm, OrdenCompraForm, UsuarioForm, DetalleOrdenFormSet
from django.forms import modelformset_factory

# Crear un formset para DetalleVenta
DetalleVentaFormSet = modelformset_factory(DetalleVenta, fields=['producto', 'cantidad', 'precio_unitario'])

def index(request):
    return render(request, 'index.html')

def productos(request):
    # Obtener todos los productos desde la base de datos
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            # Extraer los datos del formulario
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            precio = form.cleaned_data['precio']
            stock = form.cleaned_data['stock']

            # Buscar el producto existente
            producto, created = Producto.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'descripcion': descripcion,
                    'precio': precio,
                    'stock': stock
                }
            )

            if not created:
                # Actualizar el stock si el producto ya existe
                producto.descripcion = descripcion
                producto.precio = precio
                producto.stock += stock  # Acumular el stock
                producto.save()

            return HttpResponseRedirect(reverse('productos'))  # Redirige a la lista de productos

    else:
        form = ProductoForm()
    
    return render(request, 'agregar_producto.html', {'form': form})

def editar_producto(request, producto_id):
    # Obtener el producto a editar
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)  # Se pasa el producto al formulario
        if form.is_valid():
            # Guardar los datos actualizados
            form.save()
            return HttpResponseRedirect(reverse('productos'))  # Redirige a la lista de productos

    else:
        form = ProductoForm(instance=producto)  # Rellenar el formulario con los datos del producto

    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})

# Vista para listar ventas
def ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'ventas.html', {'ventas': ventas})

# Vista para agregar una nueva venta
@transaction.atomic
def agregar_venta(request):
    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        detalle_venta_formset = DetalleVentaFormSet(request.POST)

        if venta_form.is_valid() and detalle_venta_formset.is_valid():
            try:
                # Guardar la venta
                venta = venta_form.save()

                # Procesar cada uno de los detalles
                for detalle_form in detalle_venta_formset:
                    detalle = detalle_form.save(commit=False)
                    producto = detalle.producto

                    # Verificar si hay suficiente stock
                    if producto.stock < detalle.cantidad:
                        # Si no hay suficiente stock, no continuar con la transacción
                        messages.error(request, f"Stock insuficiente para {producto.nombre}. Stock actual: {producto.stock}")
                        return render(request, 'agregar_venta.html', {
                            'venta_form': venta_form,
                            'detalle_venta_formset': detalle_venta_formset,
                        })

                    # Restar el stock del producto y guardar el detalle
                    producto.stock -= detalle.cantidad
                    producto.save()  # Guardar el producto con el stock actualizado

                    detalle.venta = venta
                    detalle.subtotal = detalle.cantidad * detalle.precio_unitario  # Calcular subtotal
                    detalle.save()  # Guardar el detalle de la venta

                # Calcular el total de la venta
                total_venta = sum(detalle.cantidad * detalle.precio_unitario for detalle in detalle_venta_formset)
                venta.total_venta = total_venta
                venta.save()  # Guardar la venta con el total calculado

                messages.success(request, "Venta registrada correctamente.")
                return redirect('ventas')  # Redirigir a la lista de ventas
            
            except Exception as e:
                # Si ocurre una excepción, no se realiza un rollback dentro de `atomic`
                messages.error(request, f"Hubo un error al procesar la venta: {str(e)}")
                return render(request, 'agregar_venta.html', {
                    'venta_form': venta_form,
                    'detalle_venta_formset': detalle_venta_formset,
                })
        else:
            # Si los formularios no son válidos, renderizar la página con errores
            messages.error(request, "Hay errores en el formulario. Por favor, verifica los datos ingresados.")
            return render(request, 'agregar_venta.html', {
                'venta_form': venta_form,
                'detalle_venta_formset': detalle_venta_formset,
            })
    else:
        venta_form = VentaForm()
        detalle_venta_formset = DetalleVentaFormSet(queryset=DetalleVenta.objects.none())  # Pasamos un queryset vacío

    return render(request, 'agregar_venta.html', {
        'venta_form': venta_form,
        'detalle_venta_formset': detalle_venta_formset,
    })

# Vista para mostrar los detalles de una venta específica
def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)

    return render(request, 'detalle_venta.html', {
        'venta': venta,
        'detalles': detalles
    })


# Vistas para Cliente
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})

def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm()
    return render(request, 'agregar_cliente.html', {'form': form})

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'editar_cliente.html', {'form': form})

def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('clientes')

# Vistas para Proveedor
def lista_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores.html', {'proveedores': proveedores})

def agregar_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'agregar_proveedor.html', {'form': form})

def editar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'editar_proveedor.html', {'form': form})

def eliminar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    proveedor.delete()
    return redirect('proveedores')

# Vistas para OrdenCompra
def lista_ordenes(request):
    ordenes = OrdenCompra.objects.all()
    return render(request, 'ordenes.html', {'ordenes': ordenes})

def agregar_orden_compra(request):
    if request.method == 'POST':
        # Procesar los formularios y el formset
        form = OrdenCompraForm(request.POST)
        detalle_formset = DetalleOrdenFormSet(request.POST)

        # Verificar si los formularios y el formset son válidos
        if form.is_valid() and detalle_formset.is_valid():
            # Guardar la orden de compra sin confirmarla aún
            orden = form.save(commit=False)
            total_compra = 0  # Inicializamos el total de la compra

            # Guardar la orden de compra
            orden.save()

            # Procesar cada detalle de la orden
            for detalle_form in detalle_formset:
                producto = detalle_form.cleaned_data.get('producto')
                cantidad = detalle_form.cleaned_data.get('cantidad')

                if producto and cantidad:
                    precio = producto.precio
                    subtotal = precio * cantidad  # Calcular el subtotal de este producto
                    total_compra += subtotal  # Acumular el total de la compra

                    # Crear el detalle de la orden y guardarlo
                    DetalleOrdenCompra.objects.create(
                        orden_compra=orden,  # Cambié de "orden" a "orden_compra"
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=precio,
                        subtotal=subtotal
                    )

            # Actualizar el campo 'total_compra' con el total calculado
            orden.total_compra = total_compra
            orden.save()  # Guardar la orden con el total actualizado

            return redirect('ordenes')  # Redirigir a la lista de órdenes

    else:
        # Si no es POST, crear formularios vacíos
        form = OrdenCompraForm()
        detalle_formset = DetalleOrdenFormSet(queryset=DetalleOrdenCompra.objects.none())

    # Renderizar la plantilla con los formularios
    return render(request, 'agregar_orden.html', {'form': form, 'detalle_formset': detalle_formset})

def editar_orden_compra(request, orden_id):
    orden = get_object_or_404(OrdenCompra, id=orden_id)

    if request.method == 'POST':
        # Procesar los formularios y el formset
        form = OrdenCompraForm(request.POST, instance=orden)
        detalle_formset = DetalleOrdenFormSet(request.POST, queryset=orden.detalleordencompra_set.all())

        # Verificar si los formularios y el formset son válidos
        if form.is_valid() and detalle_formset.is_valid():
            # Guardar la orden de compra
            orden = form.save(commit=False)
            total_compra = 0  # Inicializamos el total de la compra

            # Guardar la orden de compra
            orden.save()

            # Procesar los detalles de la orden
            for detalle_form in detalle_formset:
                producto = detalle_form.cleaned_data.get('producto')
                cantidad = detalle_form.cleaned_data.get('cantidad')

                if producto and cantidad:
                    precio = producto.precio
                    subtotal = precio * cantidad  # Calcular el subtotal de este producto
                    total_compra += subtotal  # Acumular el total de la compra

                    # Si el detalle ya existe, actualízalo
                    if detalle_form.instance.id:
                        detalle_form.instance.subtotal = subtotal
                        detalle_form.instance.precio_unitario = precio
                        detalle_form.instance.save()
                    else:
                        # Si el detalle es nuevo, creamos uno nuevo
                        DetalleOrdenCompra.objects.create(
                            orden_compra=orden,  # Cambié de "orden" a "orden_compra"
                            producto=producto,
                            cantidad=cantidad,
                            precio_unitario=precio,
                            subtotal=subtotal
                        )

            # Actualizar el campo 'total_compra' con el total calculado
            orden.total_compra = total_compra
            orden.save()  # Guardar la orden con el total actualizado

            return redirect('ordenes')  # Redirigir a la lista de órdenes

    else:
        # Si no es POST, crear los formularios con los datos existentes
        form = OrdenCompraForm(instance=orden)
        detalle_formset = DetalleOrdenFormSet(queryset=orden.detalleordencompra_set.all())

    # Renderizar la plantilla con los formularios
    return render(request, 'editar_orden.html', {'form': form, 'detalle_formset': detalle_formset})


def eliminar_orden_compra(request, orden_id):
    orden = get_object_or_404(OrdenCompra, id=orden_id)
    orden.delete()
    return redirect('ordenes')


# Vista para listar usuarios
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios.html', {'usuarios': usuarios})

# Vista para agregar un nuevo usuario
def agregar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'agregar_usuario.html', {'form': form})

# Vista para editar un usuario existente
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'editar_usuario.html', {'form': form})

# Vista para eliminar un usuario
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('usuarios')
    return render(request, 'eliminar_usuario.html', {'usuario': usuario})

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')

        try:
            # Validar usuario y contraseña
            user = authenticate(request, username=usuario, password=password)

            if user:
                # Iniciar sesión si es válido
                login(request, user)

                # Enviar usuario a la base de datos personalizada
                Usuario.objects.update_or_create(
                    usuario=user.username,
                    defaults={
                        'nombre': user.get_full_name(),
                        'rol': 'admin' if user.is_superuser else 'cajero'
                    }
                )

                return redirect('index')  # Redirigir al index después de iniciar sesión
            else:
                # Si la autenticación falla
                return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos.'})
        except Exception as e:
            # Manejo general de errores
            return render(request, 'login.html', {'error': 'Ocurrió un error al iniciar sesión. Inténtalo nuevamente.'})

    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')
        rol = request.POST.get('rol')

        try:
            # Crear usuario si no existe
            if Usuario.objects.filter(username=usuario).exists():
                return render(request, 'register.html', {'error': 'El usuario ya existe.'})

            nuevo_usuario = Usuario.objects.create_user(
                username=usuario,
                password=password,
                first_name=nombre.split()[0],
                last_name=' '.join(nombre.split()[1:]),
                rol=rol
            )
            nuevo_usuario.save()

            return render(request, 'register.html', {'success': 'Usuario registrado exitosamente.'})

        except Exception as e:
            return render(request, 'register.html', {'error': f'Ocurrió un error: {str(e)}'})

    return render(request, 'register.html')