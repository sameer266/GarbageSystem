from django import forms
from products.models import *
from order.models import *
from .models import *
from accounts.models import UserReward,Reward
from accounting.models import Daily,DailyTransaction


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'



class Pick_Up_PlanForm(forms.ModelForm):
    class Meta:
        model = Pick_Up_Plan
        fields = '__all__'




class CustomersForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = '__all__'



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
            super(ProductForm, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'



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
        
# from django import forms
# from django.contrib.auth.forms import UserCreationForm

# class AgentRegistrationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['email', 'name', 'phone_no','address','image', 'password1', 'password2']


from django.core.exceptions import ValidationError

from accounts.models import User


class AgentRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'name', 'phone_no','address','image', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(AgentRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

            

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'phone_no','email', 'address', 'image'] 
        
        

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
        
        
        
class SaveInvoice(forms.ModelForm):
    customer = forms.CharField(max_length=250)
    total = forms.FloatField()

    class Meta:
        model = Invoice
        fields = ('customer', 'total')

    # def clean_transaction(self):
    #     pref = datetime.today().strftime('%Y%m%d')
    #     transaction= ''
    #     code = str(1).zfill(4)
    #     while True:
    #         invoice = Invoice.objects.filter(transaction=str(pref + code)).count()
    #         if invoice > 0:
    #             code = str(int(code) + 1).zfill(4)
    #         else:
    #             transaction = str(pref + code)
    #             break
    #     return transaction

class SaveInvoiceItem(forms.ModelForm):
    invoice = forms.CharField(max_length=30)
    product = forms.CharField(max_length=30)
    quantity = forms.CharField(max_length=100)
    price = forms.CharField(max_length=100)

    class Meta:
        model = Invoice_Item
        fields = ('invoice','product','quantity','price')

    def clean_invoice(self):
        iid = self.cleaned_data['invoice']
        try:
            invoice = Invoice.objects.get(id=iid)
            return invoice
        except:
            raise forms.ValidationError("Invoice ID is not valid")

    def clean_product(self):
        pid = self.cleaned_data['product']
        try:
            product = Product.objects.get(id=pid)
            return product
        except:
            raise forms.ValidationError("Product is not valid")

    def clean_quantity(self):
        qty = self.cleaned_data['quantity']
        if qty.isnumeric():
            return int(qty)
        raise forms.ValidationError("Quantity is not valid")
        
        
''' reward form'''
class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super(RewardForm, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                


''' user reward form'''
class UserRewardForm(forms.ModelForm):
    class Meta:
        model  = UserReward
        fields = '__all__'
    



