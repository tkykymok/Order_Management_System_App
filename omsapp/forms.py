from django.forms import ModelForm
from .models import OrderNumber,Order

class OrderNumberForm(ModelForm):
    class Meta:
        model = OrderNumber
        fields = ['order_number']
        
    def save(self, commit=True):
        instance = super(OrderNumberForm, self).save(commit=commit)

        if commit:
            instance.save()
            return instance
            
            
        
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
