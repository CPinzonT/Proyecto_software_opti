
# Register your models here.
from django.contrib import admin
from .models import OrdenCompra, Producto, DetalleOrdenCompra, Usuario


#from django.contrib.admin import AdminSite

# class MyAdminSite(AdminSite):
#     site_header = "Panel de Administración"
#     site_title = "Administración del Proyecto"
#     index_title = "Bienvenido al Panel"
#     site_url = 'index/'  # Enlace al index del proyecto

#admin_site = MyAdminSite(name='myadmin')

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'precio', 'stock')  # campos
    search_fields = ('nombre', 'descripcion')  
    list_filter = ('precio', 'stock')  
admin.site.register(Producto, ProductoAdmin)



# Personaliza el panel de administración para DetalleOrdenCompra
class DetalleOrdenCompraAdmin(admin.ModelAdmin):
    # Definir los campos que quieres mostrar en la lista de objetos
    list_display = ('orden_compra', 'producto', 'cantidad', 'precio_unitario', 'subtotal')

    # Permitir la búsqueda por ciertos campos
    search_fields = ('producto__Nombre', 'orden_compra__id')

    # Filtrar los detalles por orden de compra y producto
    list_filter = ('orden_compra', 'producto')

    # Mostrar un formulario de edición detallado
    ordering = ('orden_compra', 'producto')

# Registrar los modelos en el panel de administración
#admin.site.register(OrdenCompra)  # Asegúrate de registrar también la orden de compra
#admin.site.register(Producto)  # Si aún no has registrado el modelo Producto
admin.site.register(DetalleOrdenCompra, DetalleOrdenCompraAdmin)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'rol')  # Campos visibles en la lista
    list_filter = ('rol',)  # Filtro por roles
    search_fields = ('nombre', 'usuario')  # Búsqueda

