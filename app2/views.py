from django.shortcuts import render,HttpResponse, HttpResponseRedirect,redirect,get_object_or_404
from django.views import View
from accounts.models import *
from accounting.models import Daily,DailyTransaction
from django.contrib.auth import authenticate, login, logout
from . decorators import *
from django.contrib import messages
from django.contrib import auth
from . forms import *
# from app.models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from . new_file_handler import validate_file
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import *

from products.models import Product


def custom_404_view(request, exception):
    return render(request, 'app2/error.html')

from django.urls import reverse

def login(request):
    try:
        if request.user.is_authenticated:
            return render(request, 'app2/index.html')
        
        if request.method == "POST":
            email = request.POST.get('useremail')
            password = request.POST.get('password')
            
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                auth.login(request, user)
                if user.is_superuser or user.is_editor:
                    return redirect('dashboard:index')
                else:
                    messages.warning(request, 'Invalid user role')
            else:
                messages.warning(request, 'Invalid email or password')
                return redirect(reverse('dashboard:login'))  # Use reverse lookup here
        
        return render(request, 'app2/login.html')
    
    except Exception as e:
        print(e)
        messages.warning(request, 'Something went wrong...')
        return redirect(reverse('dashboard:login'))
    
@login_required
def userlogout(request):
    auth.logout(request)
    messages.info(request,"logout successfully..")
    return redirect('dashboard:login')


@login_required
def index(request):
    form =Pick_Up_PlanForm()
    return render(request,'app2/index.html',{'form':form})




def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard:logout')  # Redirect to the same view after successful password change
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'app2/change_password.html', {'form': form})


from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            # You can customize the response here, like redirecting to a success page
            return render(request, 'password_reset_done.html')
    else:
        form = PasswordResetForm()
    return render(request, 'reset_password.html', {'form': form})

reset_password_done = PasswordResetDoneView.as_view(template_name='password_reset_done.html')
reset_password_confirm = PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html')
reset_password_complete = PasswordResetCompleteView.as_view(template_name='password_reset_complete.html')





@user_role_required('admin')
def add_edit_Category(request, id=None):
    instance = None
    try:
        if id:
            instance = Category.objects.get(pk=id)
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the Category.')
        return redirect('dashboard:add_Category')

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'Category edited successfully.')
                return redirect('dashboard:edit_Category', id=instance.id)  # Redirect to the edited Category's details page
            else:  # Add operation
                messages.success(request, 'Category added successfully.')
                return redirect('dashboard:add_Category')  # Redirect to the page for adding new Categorys
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = CategoryForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_Category.html', context)

@user_role_required('admin')
def categories(request):
    categories=Category.objects.all()
    p=Paginator(categories,4)
    page_number= request.GET.get('page')
    categories=p.get_page(page_number)
    return render(request, 'app2/category.html',{'details':categories})

@user_role_required('admin')
def deleteCategory(request, id):
    record = Category.objects.get(pk=id)
    if request.method == 'POST':
        record.delete()
        messages.success(request,'Sub Categorie Deleted Successfully !')
        return redirect('dashboard:Category')  # Redirect to a list view after deletion
    else:
        return render(request, 'app2/category.html', {'details': record})











import json


#news subcategorie
# @user_role_required('admin')
# def add_edit_Product(request, id=None):
#     instance = None
#     try:
#         if id:
#             instance = Product.objects.get(pk=id)
#     except Exception as e:
#         messages.warning(request, 'An error occurred while retrieving the Product.')
#         return redirect('dashboard:add_Product')
    
#     subcategories_dict = {}
#     for category in Category.objects.all():
#         subcategories_dict[category.id] = list(category.category_name.values_list('id', 'sub_category_name'))

#     # Convert to JSON to pass to the template
#     subcategories_json = json.dumps(subcategories_dict)

#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES, instance=instance)
#         if form.is_valid():
#             form.save()
#             if instance:  # Edit operation
#                 messages.success(request, 'Product edited successfully.')
#                 return redirect('dashboard:edit_Product', id=instance.id)  # Redirect to the edited Product's details page
#             else:  # Add operation
#                 messages.success(request, 'Product added successfully.')
#                 return redirect('dashboard:add_Product')  # Redirect to the page for adding new Products
#         else:
#             messages.warning(request, 'Form is not valid. Please correct the errors.')
#     else:
#         form = ProductForm(instance=instance)

#     context = {'form': form, 'instance': instance,'subcategories_json': subcategories_json,}
    
#     return render(request, 'app2/create_Product.html', context)
from django.core.serializers.json import DjangoJSONEncoder


def add_edit_Product(request, id=None):
    instance = None
    try:
        if id:
            instance = Product.objects.get(pk=id)
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the Product.')
        return redirect('dashboard:add_Product')
    
    # Populate subcategories_dict
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'Product edited successfully.')
                return redirect('dashboard:edit_Product', id=instance.id)  # Redirect to the edited Product's details page
            else:  # Add operation
                messages.success(request, 'Product added successfully.')
                return redirect('dashboard:add_Product')  # Redirect to the page for adding new Products
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = ProductForm(instance=instance)

    context = {'form': form, 'instance': instance}
    
    return render(request, 'app2/create_Product.html', context)


# def get_subcategories(request):
#     category_id = request.GET.get('category_id')
#     if category_id:
#         subcategories = SubCategory.objects.filter(category_id=category_id).values_list('id', 'sub_category_name')
#         subcategories_dict = {id: name for id, name in subcategories}
#         return JsonResponse({'subcategories': subcategories_dict})
#     else:
#         return JsonResponse({'subcategories': {}})
    
@user_role_required('admin')
def Products(request):
    Products=Product.objects.all()
    p=Paginator(Products,10)
    page_number= request.GET.get('page')
    Products=p.get_page(page_number)
    return render(request, 'app2/Product.html',{'details':Products})


@user_role_required('admin')
def deleteProduct(request, id):
    record = Product.objects.get(pk=id)
    if request.method == 'POST':
        record.delete()
        messages.success(request,'Sub Categorie Deleted Successfully !')
        return redirect('dashboard:Product')  # Redirect to a list view after deletion
    else:
        return render(request, 'app2/Product.html', {'details': record})


from django.http import JsonResponse







#news subcategorie
@user_role_required('admin')
def add_edit_Vehicle(request, id=None):
    instance = None
    try:
        if id:
            instance = Vehicle.objects.get(pk=id)
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the Vehicle.')
        return redirect('dashboard:add_Vehicle')

    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'Vehicle edited successfully.')
                return redirect('dashboard:edit_Vehicle', id=instance.id)  # Redirect to the edited Vehicle's details page
            else:  # Add operation
                messages.success(request, 'Vehicle added successfully.')
                return redirect('dashboard:add_Vehicle')  # Redirect to the page for adding new Vehicles
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = VehicleForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_Vehicle.html', context)

@user_role_required('admin')
def Vehicles(request):
    Vehicles=Vehicle.objects.all()
    p=Paginator(Vehicles,4)
    page_number= request.GET.get('page')
    Vehicles=p.get_page(page_number)
    return render(request, 'app2/Vehicle.html',{'details':Vehicles})


@user_role_required('admin')
def deleteVehicle(request, id):
    record = Vehicle.objects.get(pk=id)
    if request.method == 'POST':
        record.delete()
        messages.success(request,'Sub Categorie Deleted Successfully !')
        return redirect('dashboard:Vehicle')  # Redirect to a list view after deletion
    else:
        return render(request, 'app2/Vehicle.html', {'details': record})
    
    
    
    


#news subcategorie
@user_role_required('admin')
def add_edit_Unit(request, id=None):
    instance = None
    try:
        if id:
            instance = Unit.objects.get(pk=id)
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the Unit.')
        return redirect('dashboard:add_Unit')

    if request.method == 'POST':
        form = UnitForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'Unit edited successfully.')
                return redirect('dashboard:edit_Unit', id=instance.id)  # Redirect to the edited Unit's details page
            else:  # Add operation
                messages.success(request, 'Unit added successfully.')
                return redirect('dashboard:add_Unit')  # Redirect to the page for adding new Units
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = UnitForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_Unit.html', context)


@user_role_required('admin')
def Units(request):
    Units=Unit.objects.all()
    p=Paginator(Units,4)
    page_number= request.GET.get('page')
    Units=p.get_page(page_number)
    return render(request, 'app2/Unit.html',{'details':Units})


@user_role_required('admin')
def deleteUnit(request, id):
    record = Unit.objects.get(pk=id)
    if request.method == 'POST':
        record.delete()
        messages.success(request,'Sub Categorie Deleted Successfully !')
        return redirect('dashboard:Unit')  # Redirect to a list view after deletion
    else:
        return render(request, 'app2/Unit.html', {'details': record})
    
    
    
    

#news subcategorie

@user_role_required('admin')
def add_edit_Advertisement(request, id=None):
    instance = None
    try:
        if id:
            instance = Advertisement.objects.get(pk=id)
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the Advertisement.')
        return redirect('dashboard:add_Advertisement')

    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'Advertisement edited successfully.')
                return redirect('dashboard:edit_Advertisement', id=instance.id)  # Redirect to the edited Advertisement's details page
            else:  # Add operation
                messages.success(request, 'Advertisement added successfully.')
                return redirect('dashboard:add_Advertisement')  # Redirect to the page for adding new Advertisements
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = AdvertisementForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_Advertisement.html', context)


@user_role_required('admin')
def Advertisements(request):
    Advertisements=Advertisement.objects.all()
    p=Paginator(Advertisements,4)
    page_number= request.GET.get('page')
    Advertisements=p.get_page(page_number)
    return render(request, 'app2/Advertisement.html',{'details':Advertisements})

@user_role_required('admin')
def deleteAdvertisement(request, id):
    record = Advertisement.objects.get(pk=id)
    if request.method == 'POST':
        record.delete()
        messages.success(request,'Sub Categorie Deleted Successfully !')
        return redirect('dashboard:Advertisement')  # Redirect to a list view after deletion
    else:
        return render(request, 'app2/Advertisement.html', {'details': record})
    
    
    





#news subcategorie
@user_role_required('admin')
def add_edit_Banner(request, id=None):
    instance = None
    try:
        if id:
            instance = Banner.objects.get(pk=id)
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the Banner.')
        return redirect('dashboard:add_Banner')

    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'Banner edited successfully.')
                return redirect('dashboard:edit_Banner', id=instance.id)  # Redirect to the edited Banner's details page
            else:  # Add operation
                messages.success(request, 'Banner added successfully.')
                return redirect('dashboard:add_Banner')  # Redirect to the page for adding new Banners
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = BannerForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_Banner.html', context)


@user_role_required('admin')
def Banners(request):
    Banners=Banner.objects.all()
    p=Paginator(Banners,4)
    page_number= request.GET.get('page')
    Banners=p.get_page(page_number)
    return render(request, 'app2/Banner.html',{'details':Banners})


@user_role_required('admin')
def deleteBanner(request, id):
    record = Banner.objects.get(pk=id)
    if request.method == 'POST':
        record.delete()
        messages.success(request,'Sub Categorie Deleted Successfully !')
        return redirect('dashboard:Banner')  # Redirect to a list view after deletion
    else:
        return render(request, 'app2/Banner.html', {'details': record})
    
    
    


@user_role_required('admin')
def RequestAddresss(request):
    RequestAddresss=RequestAddress.objects.all()
    p=Paginator(RequestAddresss,4)
    page_number= request.GET.get('page')
    RequestAddresss=p.get_page(page_number)
    return render(request, 'app2/RequestAddress.html',{'details':RequestAddresss})


@user_role_required('admin')
def deleteRequestAddress(request, id):
    record = RequestAddress.objects.get(pk=id)
    if request.method == 'POST':
        record.delete()
        messages.success(request,'Sub Categorie Deleted Successfully !')
        return redirect('dashboard:RequestAddress')  # Redirect to a list view after deletion
    else:
        return render(request, 'app2/RequestAddress.html', {'details': record})
    
from django.db.models import Q

@method_decorator(all_users_required, name='dispatch')
class active_order_listListView(View):
    template_name = 'app2/active_order_list.html'
    paginate_by = 10

    def get(self, request):
        agent = User.objects.filter(is_agent=True)  # Filter orders with delivery agents

        user_search = request.GET.get('user_search')
        date_search = request.GET.get('date_search')

        if request.user.is_admin  or request.user.is_sub_admin:
            prod = Order.objects.exclude(Q(order_status='received')).order_by('-id')
        else:
            prod = Order.objects.filter(driver=request.user).exclude(Q(order_status='pending') | Q(order_status='received'))

        # Apply user search filter if provided
        if user_search:
            prod = prod.filter(user__name__icontains=user_search)

        # Apply date search filter if provided
        if date_search:
            prod = prod.filter(created__date=date_search)

        paginator = Paginator(prod, self.paginate_by)
        page_number = request.GET.get('page')
        prod_page = paginator.get_page(page_number)

        return render(request, self.template_name, {'orders': prod_page, 'agent': agent})

    
# @all_users_required
@all_users_required
def update_active_order_list(request, id):
    orders = get_object_or_404(Order, id=id)
    orders1 = Order.objects.all() 
    agent=User.objects.filter(is_agent=True)# Filter orders with delivery agents
    if request.method == "POST":
        orders.order_status = request.POST['order_status']
        agent = request.POST['driver']
        print(User.objects.get(id=agent))
        delivery_agent=User.objects.get(id=agent)
        orders.driver=delivery_agent
        orders.save()
        return redirect('dashboard:active_order_list')
    
    return render(request, 'app2/active_order_list.html', {'agent': agent})


@method_decorator(all_users_required, name='dispatch')
class order_listListView(View):
    template_name = 'app2/order_list.html'
    paginate_by = 10

    def get(self, request):
        agent = User.objects.filter(is_agent=True)  # Filter orders with delivery agents

        user_search = request.GET.get('user_search')
        date_search = request.GET.get('date_search')

        if request.user.is_admin or request.user.is_sub_admin:
            prod = Order.objects.filter(order_status='received')
        else:
            prod = Order.objects.filter(order_status='received', driver=request.user)

        # Apply user search filter if provided
        if user_search:
            prod = prod.filter(user__name__icontains=user_search)

        # Apply date search filter if provided
        if date_search:
            prod = prod.filter(created__date=date_search)

        paginator = Paginator(prod, self.paginate_by)
        page_number = request.GET.get('page')
        prod_page = paginator.get_page(page_number)

        return render(request, self.template_name, {'orders': prod_page, 'agent': agent})

# @method_decorator(all_users_required, name='dispatch')
@method_decorator(all_users_required, name='dispatch')
class order_listDeleteView(View):
    template_name = 'app2/active_order_list.html'

    def get(self, request, id):
        record = get_object_or_404(Order, id=id)
        
        return render(request, self.template_name, {'orders': record})

    def post(self, request, id):
        record = get_object_or_404(Order, id=id)
        record.delete()
        messages.success(request, 'order_list deleted successfully.')

        return redirect('dashboard:active_order_list')
    
from django.template.loader import get_template

@all_users_required
def invoice1(request, id):
    order = get_object_or_404(Order, id=id)
    shipping_details = order.address
    # contactus = AboutUS.objects.first()
    template_path = "app2/invoice.html"
    context = {'order': order, 'shipping_details': shipping_details}

    if 'print_button' in request.GET:
        # Create a response object
        response = HttpResponse(content_type='application/pdf')
        
        # Set the Content-Disposition to attachment to make it downloadable
        response['Content-Disposition'] = 'attachment; filename=invoice.pdf'

        # Create a PDF object, using the response object as its "file."
        template = get_template(template_path)
        html = template.render(context)
        pdf_file = open("temp_file.pdf", "w+b")
        # pisa_status = pisa.CreatePDF(html, dest=pdf_file, encoding='utf-8')

        # if pisa_status.err:
        #     return HttpResponse('We had some errors <pre>' + html + '</pre>')

        pdf_file.seek(0)
        response.write(pdf_file.read())
        pdf_file.close()
        
        return response  # Return the response with the PDF for download
    
    else:
        return render(request,'app2/invoice1.html', context)
    

@all_users_required
def OrderDetail(request, id):
    order = get_object_or_404(Order, id=id)
    order_items = order.items.all()  # Fetch related order items

    shipping_details = order.address
    context = {
        'order': order,
        'items': order_items,  # Ensure items are passed to the template
        'Shipping': shipping_details
    }

    return render(request, 'app2/orderDetail.html', context)

    
@method_decorator(all_users_required, name='dispatch')
class deliveredorder_listDeleteView(View):
    template_name = 'app2/order_list.html'

    def get(self, request, id):
        record = get_object_or_404(Order, id=id)
        
        return render(request, self.template_name, {'orders': record})

    def post(self, request, id):
        record = get_object_or_404(Order, id=id)
        record.delete()
        messages.success(request, 'order_list deleted successfully.')

        return redirect('dashboard:order_list')
    
    
@all_users_required
def update_order_list(request, id):
    orders = get_object_or_404(Order, id=id)
    orders1 = Order.objects.all() 
    agent=User.objects.filter(is_agent=True)# Filter orders with delivery agents
    if request.method == "POST":
        orders.order_status = request.POST['order_status']
        agent = request.POST['driver']
        print(User.objects.get(id=agent))
        delivery_agent=User.objects.get(id=agent)
        orders.driver=delivery_agent
        orders.save()
        return redirect('dashboard:order_list')
    
    return render(request, 'app2/order_list.html', {'agent': agent})


@method_decorator(user_role_required('admin'), name='dispatch')
# class DriverView(View):
#     template_name = 'app2/create_Driver.html'

#     def get_instance(self, id):
#         try:
#             return User.objects.get(pk=id)
#         except User.DoesNotExist as e:
#             return None

#     def get(self, request, id=None):
#         instance = self.get_instance(id)
#         form = AgentRegistrationForm(instance=instance)
#         context = {'form': form, 'instance': instance}
#         return render(request, self.template_name, context)

#     def post(self, request, id=None):
#         instance = self.get_instance(id)
#         form = AgentRegistrationForm(request.POST, request.FILES, instance=instance)

#         if form.is_valid():
#             agent=form.save(commit=False)
#             agent.is_agent=True
#             agent.save()
#             if instance:  # Edit operation
#                 messages.success(request, 'Driver edited successfully.')
#                 return redirect('dashboard:edit_Driver', id=instance.id)
#             else:  # Add operation
#                 messages.success(request, 'Driver added successfully.')
#                 return redirect('dashboard:add_Driver')
#         else:
#             messages.warning(request, 'Email is already taken . Please correct the errors.')

#         context = {'form': form, 'instance': instance}
#         return render(request, self.template_name, context)



class DriverView(View):
    template_name = 'app2/create_Driver.html'

    def get_instance(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist as e:
            return None

    def get(self, request, id=None):
        instance = self.get_instance(id)
        form = AgentRegistrationForm(instance=instance)
        context = {'form': form, 'instance': instance}
        return render(request, self.template_name, context)

    def post(self, request, id=None):
        instance = self.get_instance(id)
        form = AgentRegistrationForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            agent = form.save(commit=False)
            agent.is_agent = True
            agent.save()
            if instance:  # Edit operation
                messages.success(request, 'Driver edited successfully.')
                return redirect('dashboard:edit_Driver', id=instance.id)
            else:  # Add operation
                messages.success(request, 'Driver added successfully.')
                return redirect('dashboard:add_Driver')
        else:
            messages.warning(request, form.errors)

        context = {'form': form, 'instance': instance}
        return render(request, self.template_name, context)
    

@method_decorator(user_role_required('admin'), name='dispatch')
class SubAdminView(View):
    template_name = 'app2/create_SubAdmin.html'

    def get_instance(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist as e:
            return None

    def get(self, request, id=None):
        instance = self.get_instance(id)
        form = AgentRegistrationForm(instance=instance)
        context = {'form': form, 'instance': instance}
        return render(request, self.template_name, context)

    def post(self, request, id=None):
        instance = self.get_instance(id)
        form = AgentRegistrationForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            agent=form.save(commit=False)
            agent.is_sub_admin=True
            agent.save()
            if instance:  # Edit operation
                messages.success(request, 'Sub Admin edited successfully.')
                return redirect('dashboard:edit_SubAdmin', id=instance.id)
            else:  # Add operation
                messages.success(request, 'SubAdmin added successfully.')
                return redirect('dashboard:add_SubAdmin')
        else:
            messages.warning(request, form.errors)

        context = {'form': form, 'instance': instance}
        return render(request, self.template_name, context)
    
    
    
# @method_decorator(user_role_required('admin'), name='dispatch')
@method_decorator(user_role_required('admin'), name='dispatch')
class DriverListView(View):
    template_name = 'app2/Driver.html'
    paginate_by = 10

    def get(self, request):
        prod = User.objects.filter(is_agent=True)
        paginator = Paginator(prod, self.paginate_by)
        page_number = request.GET.get('page')
        prod_page = paginator.get_page(page_number)
        return render(request, self.template_name, {'details': prod_page})
    
 
# @method_decorator(user_role_required('admin'), name='dispatch')
class DriverDeleteView(View):
    template_name = 'app2/Driver.html'

    def get(self, request, id):
        record = get_object_or_404(User, id=id)
        return render(request, self.template_name, {'details': record})

    def post(self, request, id):
        record = get_object_or_404(User, id=id)
        record.delete()
        messages.success(request, 'Driver deleted successfully.')

        return redirect('dashboard:Driver')
    


# =====================
# ====== USer =========
@method_decorator(user_role_required('admin'), name='dispatch')  
class UserAdd(View):
    template_name = 'app2/user_add.html'  # Ensure you have this template

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            print(request.POST)
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            image = request.FILES.get('image')  
            address = request.POST.get('address')
            is_user = request.POST.get('isUser') == 'on'  # Convert checkbox value to boolean
            activated = request.POST.get('activated') == 'on'

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect('dashboard:add_user') 

            user = User.objects.create(
                name=name,
                email=email,
                phone_no=phone,
                image=image,
                address=address,
                is_user=is_user,
                activate=activated
            )
            messages.success(request, "User added successfully!")
            return redirect('dashboard:User')  # Redirect to user list page
        except Exception as e:
            print(e)
            messages.error(request, "An error occurred while adding the user.")
            return redirect('dashboard:add_user')
        
        

@method_decorator(user_role_required('admin'), name='dispatch')  
class UserListView(View):
    template_name = 'app2/User.html'
    paginate_by = 10

    def get(self, request):
        prod = User.objects.filter(is_user=True)
        paginator = Paginator(prod, self.paginate_by)
        page_number = request.GET.get('page')
        prod_page = paginator.get_page(page_number)
        return render(request, self.template_name, {'details': prod_page})
    
    
@method_decorator(user_role_required('admin'), name='dispatch')
class SubAdminListView(View):
    template_name = 'app2/SubAdmin.html'
    paginate_by = 10

    def get(self, request):
        prod = User.objects.filter(is_sub_admin=True)
        paginator = Paginator(prod, self.paginate_by)
        page_number = request.GET.get('page')
        prod_page = paginator.get_page(page_number)
        return render(request, self.template_name, {'details': prod_page})
    
    
    
@method_decorator(user_role_required('admin'), name='dispatch')
class SubAdminDeleteView(View):
    template_name = 'app2/SubAdmin.html'

    def get(self, request, id):
        record = get_object_or_404(User, id=id)
        return render(request, self.template_name, {'details': record})

    def post(self, request, id):
        record = get_object_or_404(User, id=id)
        record.delete()
        messages.success(request, 'User deleted successfully.')

        return redirect('dashboard:SubAdmin')
    
@method_decorator(user_role_required('admin'), name='dispatch')
class UserDeleteView(View):
    template_name = 'app2/User.html'

    def get(self, request, id):
        record = get_object_or_404(User, id=id)
        return render(request, self.template_name, {'details': record})

    def post(self, request, id):
        record = get_object_or_404(User, id=id)
        record.delete()
        messages.success(request, 'User deleted successfully.')

        return redirect('dashboard:User')



@user_role_required('admin')
def aboutUs(request):
    instance = None
    try:
        if id:
            instance = AboutUS.objects.first()
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the AboutUS.')
        return redirect('dashboard:AboutUs')

    if request.method == 'POST':
        form = AboutUSForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'AboutUS edited successfully.')
                return redirect('dashboard:AboutUs')  # Redirect to the edited AboutUS's details page
            else:  # Add operation
                messages.success(request, 'AboutUS added successfully.')
                return redirect('dashboard:AboutUs')  # Redirect to the page for adding new AboutUS
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = AboutUSForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_aboutUs.html', context)






    
from django.forms import inlineformset_factory


def stock_update_create( order_instance):
    print("order_instance:",order_instance)
    if order_instance.order_status == 'received':
        for order_item in order_instance.items.all():
            product = order_item.product
            quantity = order_item.quantity

            stock, created = Stock.objects.get_or_create(product=product)

            if order_instance.id:  
                stock.quantity -= order_item.quantity
            else:
                stock.quantity += quantity

            # Save the stock
            stock.save()


def create_Order(request, id=None):
    products = Product.objects.all()
    order_instance = get_object_or_404(Order, id=id) if id else Order()
    OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1, max_num=1, can_delete=False)

    if request.method == 'POST':
        order_form = OrderForm(request.POST, request.FILES, instance=order_instance)
        formset = OrderItemFormSet(request.POST, request.FILES, instance=order_instance)

        if order_form.is_valid() and formset.is_valid():
            order_instance = order_form.save(commit=False)
            order_items = formset.save(commit=False)
            total_price = 0

            # Calculate total price
            for item in order_items:
                item.order = order_instance
                item.price = item.product.rate
                total_price += item.price * item.quantity

            # Set total price and save the order instance
            order_instance.totalPrice = total_price
            order_instance.save()  # Save the order instance first

            # Save the formset with the updated order instance
            formset.save()

            # Display success message
            message = 'Order updated successfully.' if id else 'Order created successfully.'
            messages.success(request, message)
            return redirect('dashboard:edit_Order', id=order_instance.id)

    else:
        order_form = OrderForm(instance=order_instance)
        formset = OrderItemFormSet(instance=order_instance)

    # Calculate total price for existing order
    total_price = sum(item.product.rate * item.quantity for item in order_instance.items.all()) if order_instance.pk else 0

    context = {
        'form': order_form,
        'formset': formset,
        'instance': order_instance,
        'products': products,
        'total_price': total_price,
    }

    return render(request, 'app2/create_Order.html', context)


def get_product_price(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        return JsonResponse({'price': float(product.rate)})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
#     # ======= Calculate price  in  Create Order ===========
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.authentication import SessionAuthentication
# class CalculatePrice(APIView):
#     authentication_classes=[SessionAuthentication]
    
#     def get(self,request):
#         try:
#             product=request.data.get('product')
#             quantity=request.data.get('quantity')
#             product_obj=Product.objects.get(product_name=product)
#             total_price=product_obj.rate*quantity
#             return Response({'total_price':total_price},status=200)
#         except Product.DoesNotExist:
#             return Response({'error':'Product not found'},status=400)
#         except Exception as e:
#             return Response({error':str(e)},status=400)
    



from django.db.models import Sum

# ======== accounting ========
def accounting(request):
    # Accounting Data
    orders = Order.objects.exclude(order_status='pending')
    
    # Cashbook Data
    today = nepali_datetime.date.today()
    enddate = today + timedelta(days=1)
    dailytrasactions_list = Daily.objects.all()
    grand_total = dailytrasactions_list.aggregate(Sum('total'))['total__sum']

    # Combine data into a single context
    context = {
        'orders': orders,
        'dailytrasactions_list': dailytrasactions_list,
        'today': today,
        'enddate': enddate,
        'grand_total': grand_total,
    }
    return render(request, 'app2/accounting.html', context)
    
def invoice(request,order_id=None):
    order_detail =Order.objects.get(id=order_id)
    print(order_detail)
    return render(request,'app2/invoice.html',{'order_detail':order_detail})

def add_edit_invoice(request):
    invoiceForm= InvoiceForm()
    return render(request,'app2/edit_invoice.html',{'invoiceForm':invoiceForm})

import nepali_datetime
from django.utils import timezone
from datetime import datetime,timedelta


from nepali_datetime import date

nepali_month_mapping = {
    'Baishakh': 1,
    'Jestha': 2,
    'Ashadh': 3,
    'Shrawan': 4,
    'Bhadra': 5,
    'Ashwin': 6,
    'Kartik': 7,
    'Mangsir': 8,
    'Poush': 9,
    'Magh': 10,
    'Falgun': 11,
    'Chaitra': 12,
}






@login_required
def dailytransaction(request, id=None):
    instance= None
    formatted_date= None
    data=None
    if id:
        instance = Daily.objects.get(id=id)
        data = DailyTransaction.objects.select_related('dailyid').filter(dailyid=instance).all()

        create_date = Daily.objects.get(id = instance.id)
        nepali_date_str = create_date.nepali_date
        day, month_name, year = nepali_date_str.split('-')

        nepali_month = nepali_month_mapping.get(month_name)

        if nepali_month is not None:
            nepali_date = date(int(year), nepali_month, int(day))
            formatted_date = nepali_date.strftime('%Y-%m-%d')
        else:
            print("Invalid Nepali month name")


    if request.method == "POST":
        today  = request.POST['nepali_date']
        year, month, day = map(int, today.split('-'))
        nepali_date = date(year, month, day)
        today = nepali_date.strftime("%d-%B-%Y")
        daily = Daily.objects.filter(nepali_date = today).first()
        # total = request.POST['total']
        if daily is None:
            dailyobj = Daily.objects.create(nepali_date=today)
            dailyobj.save()
            dailyobj  = Daily.objects.get(id=dailyobj.id)
            
        # else:
        #     daily.total+=(float(total))
        #     daily.save()

        
        form = DailyTransactionForm(request.POST, instance=instance)
        
        if form.is_valid():
            instacne_data= form.save(commit=False)
            if daily:
                instacne_data.dailyid = daily
            else:
                instacne_data.dailyid = dailyobj

           
            # instacne_data.save()

            additional_fields = {}


            for key, value in request.POST.items():
                if key.startswith(('product', 'quantity', 'unite', 'remarks')):
                    field_type, *rest = key.split('_')
                    index = rest[0] if rest else '0'
                    additional_fields.setdefault(int(index), {})[field_type] = value

                            
            
            try:
                for index, fields in additional_fields.items():
                    print("aAA:", fields)

                    daily_instance = instacne_data.dailyid  
                    fields['dailyid'] = daily_instance

                    product_id = fields['product']
                    product_instance = Product.objects.get(id=product_id)  
                    fields['product'] = product_instance

                    unite_id = fields['unite']
                    unite_instance = Unit.objects.get(id=unite_id)  
                    fields['unite'] = unite_instance
                    
                    DailyTransaction.objects.create(**fields)
                            

            except Exception as e:
                print(e)
                return redirect('dashboard:daily_transaction')
            if instance:
                messages.success(request,"Transaction Update Successfully !")
                return redirect('dashboard:update_trasancation', instance.id)
            else:
                messages.success(request,"Transaction Added Successfully !")
                return redirect('/dashboard:inventory')
            
        else:
            messages.warning(request,"Please fill out the all form fields !")
            return redirect('dashboard:daily_transaction')
    else:
        dailytrasactions_list = Daily.objects.all()
        data = DailyTransaction.objects.all()
        daily_form  = DailyTransactionForm(instance=instance)
        product = Product.objects.all()
        unites = Unit.objects.all()
        nepalidate = nepali_datetime.date.today()
        form = DailyForm()
        return render(request,'app2/create_dailytransaction.html',{'daily_form':daily_form,
                                                           'dailytrasactions_list':dailytrasactions_list,
                                                           'products':product,
                                                           'unites':unites,
                                                            'data':data,
                                                            'instance':instance,
                                                            'date':formatted_date,
                                                            'nepalidate':nepalidate,
                                                            'form':form,
                                                            'data':data
                                                           }) 
@login_required
def dailytrasactionfilter(request):
    today  = nepali_datetime.date.today()
    enddate=today + timedelta(days=1)
    if request.method =="POST":
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        year, month, day = map(int, startdate.split('-'))
        nepali_date = date(year, month, day)
        start_date = nepali_date.strftime("%d-%B-%Y")

        year, month, day = map(int, enddate.split('-'))
        nepali_date = date(year, month, day)
        end_date = nepali_date.strftime("%d-%B-%Y")

        if start_date <= end_date:
            dailyobjlist = Daily.objects.filter(Q(nepali_date__range=(start_date, end_date)))
            grand_total = dailyobjlist.aggregate(Sum('total'))['total__sum']
            return render(request,'app2/table.html',{'daily_list':dailyobjlist,'startdate':today,
                                                'enddate':enddate,'grand_total':grand_total})
        else:
            dailyobjlist= Daily.objects.all()
            messages.warning(request,'Start date cannot be greater than the end date.')
            return render(request,'app2/table.html',{'daily_list':dailyobjlist,'startdate':today,
                                                'enddate':enddate})
        
    else:
        dailyobjlist= Daily.objects.all()
        grand_total = dailyobjlist.aggregate(Sum('total'))['total__sum']
        return render(request,'app2/table.html',{'daily_list':dailyobjlist,
                                                'startdate':today,
                                                'enddate':enddate
                                                })

@login_required
def delete_transaction(request):
    if request.method=="POST":
        id = request.POST['daily_transactionID']
        transaction_obje = Daily.objects.get(id= id)
        transaction_obje.delete()
        messages.info(request,"Deleted Successfully !")
        return redirect('dashboard:accounting')
    else:
        return redirect('dashboard:accounting')


@login_required
def delete_daily_transaction_item(request):
    if request.method=="POST":
        id = request.POST['transactionID']
        daily_id = request.POST['daily_id']
        transaction_obje = DailyTransaction.objects.get(id= id)
        transaction_obje.delete()
        messages.info(request,"Deleted Successfully !")
        return redirect('dashboard:update_trasancation', daily_id)
    else:
        return redirect('dashboard:daily')
    

@login_required
def edite_dailytransaction(request, id= None):
    formatted_date= None
    instance=Daily.objects.get(id=id)
    selectdata =DailyTransaction.objects.select_related('dailyid').filter(dailyid=instance).all()

    nepali_date_str = instance.nepali_date
    day, month_name, year = nepali_date_str.split('-')

    nepali_month = nepali_month_mapping.get(month_name)

    if nepali_month is not None:
        nepali_date = date(int(year), nepali_month, int(day))
        formatted_date = nepali_date.strftime('%Y-%m-%d')
    else:
        print("Invalid Nepali month name")
    # formatted_date=instance.nepali_date
    
    if request.method == "POST":
        instance = Daily.objects.get(id=id)
        
        form = DailyForm(request.POST, instance=instance)
        daily_instance=form.save(commit=False)
        today  = request.POST['nepali_date']
        year, month, day = map(int, today.split('-'))
        nepali_date = date(year, month, day)
        today = nepali_date.strftime("%d-%B-%Y")
        daily_instance.nepali_date = today
        daily_instance.save()
        transaction_ids = request.POST.getlist('transaction_id')

        for transaction_id in transaction_ids:
            product_id = request.POST.get(f'product_{transaction_id}')
            quantity = request.POST.get(f'quantity_{transaction_id}')
            unite_id = request.POST.get(f'unite_{transaction_id}')
            remarks = request.POST.get(f'remarks_{transaction_id}')
            daily_transaction = DailyTransaction.objects.get(id=transaction_id)

            daily_transaction.product_id = product_id
            daily_transaction.quantity = quantity
            daily_transaction.unite_id = unite_id
            daily_transaction.remarks = remarks
            daily_transaction.save()

        messages.success(request,"Transaction Update Successfully !")
        return redirect('dashboard:update_trasancation', instance.id)
    else:
        data = DailyTransaction.objects.all()
        daily_form  = DailyTransactionForm(instance=instance)
        product = Product.objects.all()
        unites = Unit.objects.all()
        nepalidate = nepali_datetime.date.today()
        form = DailyForm()
        return render(request,'app2/edite_daily_transaction.html',{'daily_form':daily_form,
                                                           'products':product,
                                                           'unites':unites,
                                                            'data':data,
                                                            'instance':instance,
                                                            'date':formatted_date,
                                                            'nepalidate':nepalidate,
                                                            'form':form,
                                                            'selectdata':selectdata
                                                           })






@user_role_required('admin')
def add_edit_Pick_Up_Plan(request, id=None):
    instance = None
    try:
        if id:
            instance = Pick_Up_Plan.objects.get(pk=id)
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the Pick_Up_Plan.')
        return redirect('dashboard:add_Pick_Up_Plan')

    if request.method == 'POST':
        form = Pick_Up_PlanForm(request.POST, request.FILES, instance=instance)
        

        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'Pick_Up_Plan edited successfully.')
                return redirect('dashboard:pick_up_plans')  # Redirect to the edited Pick_Up_Plan's details page
            else:  # Add operation
                messages.success(request, 'Pick_Up_Plan added successfully.')
                return redirect('dashboard:pick_up_plans')  # Redirect to the page for adding new Pick_Up_Plans
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = Pick_Up_PlanForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_Pick_Up_Plan.html', context)

@user_role_required('admin')
def pick_Up_plans(request):
    Pick_Up_Plans=Pick_Up_Plan.objects.all()
    return render(request, 'app2/pick_plan.html',{'details':Pick_Up_Plans})


@user_role_required('admin')
def deletePick_Up_Plan(request, id):
    record = Pick_Up_Plan.objects.get(pk=id)
    if request.method == 'POST':
        record.delete()
        messages.success(request,'Deleted Successfully !')
        return redirect('dashboard:pick_up_plans')
    else:
        return redirect('dashboard:index')
    
    
    
# ====== Inventory ========

def inventory(request):
   
    products = Stock.objects.all()
    return render(request,'app2/stock.html',{'products':products})


def inventory_add(request):
    products= Product.objects.all()
    if request.method=="POST":
        product_name=request.POST.get('product_name')
        product_obj=Product.objects.get(product_name=product_name)
        quantity=request.POST.get('quantity')
        sold_quantity=request.POST.get('sold_quantity')
        stock_obj=Stock.objects.create(product=product_obj,quantity=quantity,sold_quantity=sold_quantity)
        messages.success(request,"Inventory added successfully")
        return redirect('/inventory')
    return render(request,'app2/stockAdd.html',{'products':products})
    
    
# edit inventory
def edit_inventory(request,id):
    stocK_obj=Stock.objects.get(id=id)
    if request.method=="POST":
        quantity=request.POST.get('quantity')
        sold_quantity=request.POST.get('sold_quantity')
        stocK_obj.quantity=float(quantity)
        stocK_obj.sold_quantity=float(sold_quantity)
        stocK_obj.save()
        messages.success(request,'Inventory updated succesfully')
        return  redirect('/inventory')
    return render(request, 'app2/stockEdit.html', {'stock_item': stocK_obj})
        
#  delete inventory
def inventory_delete(request,id):
    try:
        stock=Stock.objects.get(id=id)
        stock.delete()
        messages.success(request,"Stock deleted successfully")
        return redirect('/inventory')
    except Exception as e:
        print(e)
    
        
        

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def sales(request):
    items_per_page = 10  
    sales_list = Invoice.objects.all()
    paginator = Paginator(sales_list, items_per_page)
    page = request.GET.get('page')

    try:
        sales = paginator.page(page)
    except PageNotAnInteger:
        sales = paginator.page(1)
    except EmptyPage:
        sales = paginator.page(paginator.num_pages)

    total_amount = sales_list.aggregate(total_cost=Sum('total'))['total_cost'] or 0
    total_sales= sales_list.count()
    return render(request,'app2/sales_table.html',{'sales':sales,'total_sales':total_sales,'total_amount':total_amount})

    
    
def create_sales(request):
    product = Product.objects.all()
    customer = Customers.objects.all()
    return render(request,'app2/sales.html',{'products':product,'customers':customer})

def sales_details(request, id=None):
    sales_instance = Invoice.objects.get(id=id)
    return render(request, 'app2/sales_detail.html',{'sales_instance':sales_instance})

def sales_invoice(request,id=None):
    sales_instance = Invoice.objects.get(id=id)
    return render(request, 'app2/sales_invoice.html',{'sales_instance':sales_instance})
    
def get_product(request):
    resp = {'status':'failed','data':{},'msg':''}
    pk= request.GET.get('pk')
    print(pk)
    if pk is None:
        resp['msg'] = 'Product ID is not recognized'
    else:
        product = Product.objects.get(id = pk)
        # Invoice_Item.objects.create(product=product)
        resp['data']['product'] = str(product.product_name)
        resp['data']['unit'] = str(product.unit)
        resp['data']['id'] = str(product.id)
        resp['data']['price'] = product.rate
        resp['status'] = 'success'
    return HttpResponse(json.dumps(resp),content_type="application/json")


def save_sales(request):
    resp = {'status':'failed', 'msg' : ''}
    id = 2
    if request.method == 'POST':
        pids = request.POST.getlist('pid[]')
        cus_id=request.POST['customer']
        print(cus_id)
        print(request.POST['total'])
        customer=Customers.objects.get(id=cus_id)
        # invoice_form = SaveInvoice(request.POST)
        invoice_instance= Invoice.objects.create(customer=customer,total=request.POST['total'])
        print(request.POST)
        if invoice_instance:
            invoice = Invoice.objects.first()
            for pid in pids:
                data = {
                    'invoice':invoice.id,
                    'product':Product.objects.get(id=pid).id,
                    'quantity':request.POST['quantity['+str(pid)+']'],
                    'price':request.POST['price['+str(pid)+']'],
                }
                print(data)
                ii_form = SaveInvoiceItem(data=data)
                if ii_form.is_valid():
                    ii_form.save()
                else:
                    print(ii_form.errors)
                    for fields in ii_form:
                        for error in fields.errors:
                            resp['msg'] += str(error + "<br>")
                    break
            messages.success(request, "Sale Transaction has been saved.")
            resp['status'] = 'success'
            # invoice.delete()
        else:
            
            for error in fields.errors:
                resp['msg'] += str(error + "<br>")

    return HttpResponse(json.dumps(resp),content_type="application/json")
    
    
    
    





@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile Updated Successfully !')
            return redirect('dashboard:edit_profile')  # Redirect to the profile page after saving
        
        
        else:
            messages.warning(request,form.errors)
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'app2/updateProfile.html', {'form': form})




@method_decorator(user_role_required('admin'), name='dispatch')
class UpdateSubAdminView(View):
    template_name = 'app2/edit_subadmin.html'

    def get_instance(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist as e:
            return None

    def get(self, request, id=None):
        instance = self.get_instance(id)
        form = UserProfileForm(instance=instance)
        context = {'form': form, 'instance': instance}
        return render(request, self.template_name, context)

    def post(self, request, id=None):
        instance = self.get_instance(id)
        form = UserProfileForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            agent=form.save(commit=False)
            agent.is_sub_admin=True
            agent.save()
            if instance:  # Edit operation
                messages.success(request, 'Sub Admin edited successfully.')
                return redirect('dashboard:edit_Sub_Admin', id=instance.id)
            else:  # Add operation
                messages.success(request, 'SubAdmin added successfully.')
                return redirect('dashboard:add_SubAdmin')
        else:
            messages.warning(request, form.errors)

        context = {'form': form, 'instance': instance}
        return render(request, self.template_name, context)
    




@method_decorator(user_role_required('admin'), name='dispatch')
class UpdateAgentView(View):
    template_name = 'app2/edit_agent.html'

    def get_instance(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist as e:
            return None

    def get(self, request, id=None):
        instance = self.get_instance(id)
        form = UserProfileForm(instance=instance)
        context = {'form': form, 'instance': instance}
        return render(request, self.template_name, context)

    def post(self, request, id=None):
        instance = self.get_instance(id)
        form = UserProfileForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            agent=form.save(commit=False)
            agent.is_agent=True
            agent.save()
            if instance:  # Edit operation
                messages.success(request, 'Agent edited successfully.')
                return redirect('dashboard:update_agent', id=instance.id)
            else:  # Add operation
                messages.success(request, 'Agent added successfully.')
                return redirect('dashboard:add_agent')
        else:
            messages.warning(request, form.errors)

        context = {'form': form, 'instance': instance}
        return render(request, self.template_name, context)
        
        
        

def privacy(request):
    privacy=PrivacyPolicy.objects.first()
    return render(request, 'app2/privacypolicy.html',{'privacy':privacy})
    
    

#news subcategorie
@user_role_required('admin')
def add_edit_Customers(request, id=None):
    instance = None
    try:
        if id:
            instance = Customers.objects.get(pk=id)
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the suppliers.')
        return redirect('dashboard:add_Customers')

    if request.method == 'POST':
        form = CustomersForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'supplier edited successfully.')
                return redirect('dashboard:edit_Customers', id=instance.id)  # Redirect to the edited Customers's details page
            else:  # Add operation
                messages.success(request, 'supplier added successfully.')
                return redirect('dashboard:add_Customers')  # Redirect to the page for adding new Customerss
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = CustomersForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_Customers.html', context)

@user_role_required('admin')
def Customerss(request):
    if request.method =="POST":
        company_name= request.POST.get('company_name')
        print(company_name)
        owner_name= request.POST.get('owner_name')
        address= request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        customers = Customers.objects.all()
        if company_name:
            customers = customers.filter(companyName__icontains=company_name)
        if owner_name:
            customers = customers.filter(ownerName__icontains=owner_name)
        if address:
            customers = customers.filter(address__icontains=address)
        if phone_number:
            customers = customers.filter(phoneNo__icontains=phone_number)
        print(customers)
        return render(request, 'app2/Customers.html',{'details':customers})
    else:
        Customerss=Customers.objects.all()
        # p=Paginator(Customerss,10)
        # page_number= request.GET.get('page')
        # Customerss=p.get_page(page_number)
        return render(request, 'app2/Customers.html',{'details':Customerss})


@user_role_required('admin')
def deleteCustomers(request, id):
    record = Customers.objects.get(pk=id)
    if request.method == 'POST':
        record.delete()
        messages.success(request,'suppliers Deleted Successfully !')
        return redirect('dashboard:Customers')  # Redirect to a list view after deletion
    else:
        return render(request, 'app2/Customers.html', {'details': record})
    
    

def customer_invoices(request, customer_id):
    customer = get_object_or_404(Customers, pk=customer_id)
    invoices = Invoice.objects.filter(customer=customer)


    # Pagination
    paginator = Paginator(invoices, 10)  # Show 10 invoices per page
    page = request.GET.get('page')
    try:
        invoices = paginator.page(page)
    except PageNotAnInteger:
        invoices = paginator.page(1)
    except EmptyPage:
        invoices = paginator.page(paginator.num_pages)

    return render(request, 'app2/Customers_sales_detail.html', {'customer': customer, 'invoices': invoices})
    
    

''' export file in excel csv and pdf '''
import csv
import xlsxwriter
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from .models import Customers

@login_required
def export_data(request, format):
    data = Customers.objects.all()

    if format == 'excel':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="suppliers.xlsx"'
        workbook = xlsxwriter.Workbook(response)
        worksheet = workbook.add_worksheet()

        headers = ['Company Name', 'Owner Name', 'Address','Phone Number'] 
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        for row, obj in enumerate(data, start=1):
            worksheet.write(row, 0, obj.companyName)  
            worksheet.write(row, 1, obj.ownerName)
            worksheet.write(row, 2, obj.address)
            worksheet.write(row, 3, obj.phoneNo)


        workbook.close()
        

    elif format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="suppliers.csv"'
        writer = csv.writer(response)

        headers = ['Company Name', 'Owner Name', 'Address','Phone Number'] 
        writer.writerow(headers)

        for obj in data:
            writer.writerow([obj.companyName, obj.ownerName, obj.address,obj.phoneNo]) 
        
    elif format == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="suppliers.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        table_data = []
        headers = ['Company Name', 'Owner Name', 'Address', 'Phone Number']
        table_data.append(headers)

        for obj in data:
            row = [obj.companyName, obj.ownerName, obj.address, obj.phoneNo]
            table_data.append(row)

        table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                  ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                  ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                  ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                  ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                  ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                  ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        table = Table(table_data)
        table.setStyle(table_style)

        doc.build([table])

        return response

    else:
        return HttpResponse("Invalid format")

    return response
    

''' reward points'''
@login_required
def rewards_create_or_update(request):
    instance = Reward.objects.all().first()
    user_rewards = UserReward.objects.all()
    if request.method =="POST":
        forms = RewardForm(request.POST, instance=instance)
        if forms.is_valid():
            forms.save()
            messages.success(request,"Update Successfully !")
        else:
            print(forms.errors)
   
    forms = RewardForm(instance=instance)
    return render(request, 'app2/rewards.html',{'forms':forms,'customers_rewards':user_rewards})

@login_required
def user_reward_update(request, id = None):
    user_instance = get_object_or_404(User, id=id)

    if request.method == "POST":
        user_reward_form = UserRewardForm(request.POST, instance=user_instance)

        if user_reward_form.is_valid():
            user_reward_form.save()
            messages.success(request, 'Update Successfully !')

    else:
        user_reward_form = UserRewardForm(instance=user_instance)

    return render(request, "app2/user_reward_form.html", {'user_reward_form': user_reward_form})

''' user order history'''
@login_required
def user_order_history(request, id=None):
    user_orders = Order.objects.filter(user=id).order_by('-created')
    user_reward = UserReward.objects.filter(user=id).first()
    return render(request, 'app2/user_order_histroy.html', {'user_orders':user_orders, 'user_reward':user_reward})



# ======= Notification ==========

@login_required
def notification_list(request):
    notifications = Notification.objects.all()[ :30]
    return render(request, 'app2/notification_list.html', {'notifications': notifications})


# @login_required
# def notification_add(request):
#     if request.method == "POST":
#         message = request.POST.get('message')
#         status = request.POST.get('status') == "on"
#         order_number = Notification.objects.count() + 1
#         Notification.objects.create(user=request.user, message=message, read=status, order_number=order_number)
#         messages.success(request, "Notification Added Successfully")
#         return redirect('/notification_list')
#     return render(request, 'app2/notification_add.html')

@login_required
def notification_edit(request, id):
    notification = Notification.objects.get(id=id)
    if request.method == "POST":
        notification.message = request.POST.get('message')
        notification.read = request.POST.get('status') == "on"
        notification.save()
        messages.success(request, "Notification Updated Successfully")
        return redirect('/notification_list')
    return render(request, 'app2/notification_edit.html', {'notification': notification})

@login_required
def notification_delete(request, id):
    notification = Notification.objects.get(id=id)
    notification.delete()
    messages.success(request,"Notification deleted successfully")
    return redirect('/notification_list')


    