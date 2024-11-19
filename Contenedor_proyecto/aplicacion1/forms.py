# aplicacion1/forms.py
from django import forms
from .models import Cliente, Producto, Proveedor, Usuario, OrdenCompra, DetalleOrdenCompra, Venta, DetalleVenta
from django.forms import modelformset_factory

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'


class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = '__all__'


class DetalleOrdenCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleOrdenCompra
        fields = '__all__'  # Usa '__all__' o selecciona los campos específicos que necesitas

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')

        if producto and cantidad:
            cleaned_data['subtotal'] = producto.precio * cantidad  # Calcula el subtotal
        return cleaned_data


DetalleOrdenFormSet = modelformset_factory(DetalleOrdenCompra, form=DetalleOrdenCompraForm, extra=1)


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VentaForm, self).__init__(*args, **kwargs)
        # Filtra clientes con un documento registrado para la selección en ventas
        self.fields['cliente'].queryset = Cliente.objects.exclude(documento__isnull=True)


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')

        if producto and cantidad:
            cleaned_data['subtotal'] = producto.precio * cantidad  # Calcula el subtotal automáticamente
        return cleaned_data
