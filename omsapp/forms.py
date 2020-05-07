from django import forms  
from .models import Customer, Supplier, Project, Task


class CustomerCreateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_code', 'name', 'address', 'phone']
        
class SupplierCreateForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['supplier_code', 'name', 'address', 'phone']
        
class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['prj_code', 'customer']
        
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['user','title']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }
        