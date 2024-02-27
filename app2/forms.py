from django import forms
from products.models import *
from order.models import *
from .models import *
from accounting.models import Daily,DailyTransaction


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'



class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = '__all__'



class Pick_Up_PlanForm(forms.ModelForm):
    class Meta:
        model = Pick_Up_Plan
        fields = '__all__'



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'




class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'





class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = '__all__'



class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = '__all__'
        

class AboutUSForm(forms.ModelForm):
    class Meta:
        model = AboutUS
        fields = '__all__'



class RequestAddressForm(forms.ModelForm):
    class Meta:
        model = RequestAddress
        fields = '__all__'        
        
        
class UserForm(forms.ModelForm):
    class Meta:
        model  = User
        fields ='__all__'  
        


class OrderForm(forms.ModelForm):
    class Meta:
        model  = Order
        fields ='__all__'   
    

class OrderItemForm(forms.ModelForm):
    class Meta:
        model  = OrderItem
        fields ='__all__'   
    
    
NewsVideoFormSet = forms.inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)



class InvoiceForm(forms.ModelForm):
    class Meta:
        model  = Invoice
        fields ='__all__'

        def __init__(self, *args, **kwargs):
            super(InvoiceForm, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                


class DailyForm(forms.ModelForm):
    class Meta:
        model =Daily
        fields ='__all__'

class DailyTransactionForm(forms.ModelForm):
    class Meta:
        model = DailyTransaction
        fields =['product','quantity','unite','remarks']




class Pick_Up_PlanForm(forms.ModelForm):
    class Meta:
        model = Pick_Up_Plan
        fields ='__all__'
        
        
        
        