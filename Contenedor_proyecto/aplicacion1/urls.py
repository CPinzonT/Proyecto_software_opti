
# aplicacion1/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('productos/', views.productos, name='productos'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('editar_producto/<int:producto_id>/', views.editar_producto, name='editar_producto' ),
    path('ventas/', views.ventas, name='ventas'),
    path('agregar_venta/', views.agregar_venta, name='agregar_venta'),
    path('detalle_venta/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
     # URLs para Cliente
    path('clientes/', views.lista_clientes, name='clientes'),
    path('agregar_cliente/', views.agregar_cliente, name='agregar_cliente'),
    path('editar_cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('eliminar_cliente/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),

    # URLs para Proveedor
    path('proveedores/', views.lista_proveedores, name='proveedores'),
    path('agregar_proveedor/', views.agregar_proveedor, name='agregar_proveedor'),
    path('editar_proveedor/<int:proveedor_id>/', views.editar_proveedor, name='editar_proveedor'),
    path('eliminar_proveedor/<int:proveedor_id>/', views.eliminar_proveedor, name='eliminar_proveedor'),

    # URLs para OrdenCompra
    path('ordenes/', views.lista_ordenes, name='ordenes'),
    path('agregar_orden/', views.agregar_orden_compra, name='agregar_orden'),
    path('editar_orden/<int:orden_id>/', views.editar_orden_compra, name='editar_orden'),
    path('eliminar_orden/<int:orden_id>/', views.eliminar_orden_compra, name='eliminar_orden'),

    #url para usuarios
    path('usuarios/', views.lista_usuarios, name='usuarios'),
    path('agregar_usuario/', views.agregar_usuario, name='agregar_usuario'),
    path('editar_usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
]


