from .models import ASO_Configuration,LU_Category,LU_Item,Product,LU_Value
from django.db.models import Q, Count
from django.contrib.auth import authenticate,login,decorators
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from .forms import RegistrationForm
from django.db import connection
from django.contrib import messages
import time
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

###############################################################################
@decorators.login_required(login_url='/login/')
def home(request):
    ASO_Configurations = ASO_Configuration.objects.all()
    LU_Categorys = LU_Category.objects.all()
    LU_Items = LU_Item.objects.all()
    Products = Product.objects.all()
    LU_Values = LU_Value.objects.all()

    total_ASO_Configuration = ASO_Configurations.count()
    total_LU_Category = LU_Categorys.count()
    total_LU_Item = LU_Items.count()
    total_Product = Products.count()
    total_LU_Value = LU_Items.count()

    # delivered = orders.filter(status='Delivered').count()
    # pending = orders.filter(status='Pending').count()

    context={
        'ASO_Configuration':ASO_Configurations,
        'LU_Category':LU_Categorys,
        'LU_Item':LU_Items,
        'Product':Products,
        'LU_Value':LU_Values,

        'total_ASO_Configuration':total_ASO_Configuration,
        'total_LU_Category':total_LU_Category,
        'total_LU_Item':total_LU_Item,
        'total_Product':total_Product,
        'total_LU_Value':total_LU_Value,
    }
    return render(request, 'pages/dashboard.html', context)

###############################################################################

@decorators.login_required(login_url='/login/')
def view_Aso(request):
    ASO_Configurations = ASO_Configuration.objects.all()
    context={'ds_aso':ASO_Configurations}
    return render(request, "pages/list_aso.html",context)

###############################################################################

@decorators.login_required(login_url='/login/')
def view_Cat(request):
    LU_Categorys = LU_Category.objects.all()
    context={'ds_cat':LU_Categorys}
    return render(request, "pages/list_cat.html",context) 

###############################################################################

@decorators.login_required(login_url='/login/')
def view_Item(request):
    LU_Items = LU_Item.objects.all()
    context={'ds_item':LU_Items}
    return render(request, "pages/list_item.html",context)

###############################################################################

@decorators.login_required(login_url='/login/')
def view_Pro(request):
    Products = Product.objects.all()
    context={'ds_pro':Products}
    return render(request, "pages/list_pro.html",context)

###############################################################################

@decorators.login_required(login_url='/login/')
def view_Value(request):
    LU_Values = LU_Value.objects.all()
    context={'ds_value':LU_Values}
    return render(request, "pages/list_value.html",context)

###############################################################################
def index(request):
    return render(request, 'pages/home.html')
def contact(request):
    return render(request,'pages/contact.html')
def document(request):
    return render(request,'pages/document.html')
###############################################################################


###############################################################################

def is_valid_queryparam(param):
    return param!="" and param is not None
@decorators.login_required(login_url='/login/')
def filter(request):
    qs=ASO_Configuration.objects.all()
    total_query=request.GET.get('total')
    category = request.GET.get('category')
    product = request.GET.get('product')
    item = request.GET.get('item')
    value= request.GET.get('value')

    if is_valid_queryparam(total_query):
        qs=qs.filter(
            (Q(Project__icontains=total_query))|
            (Q(Customer__icontains=total_query))|
            (Q(Product__Product__icontains=total_query))|
            (Q(Value__Category__Category__icontains=total_query))|
            (Q(Value__Item__Item__icontains=total_query))
            ).distinct()
    if is_valid_queryparam(category) and category != 'Choose...':
        qs = qs.filter(Value__Category__Category=category)
    if is_valid_queryparam(product) and product != 'Choose...':
        qs = qs.filter(Product__Product=product)
    if is_valid_queryparam(item) and item != 'Choose...':
        qs = qs.filter(Value__Item__Item=item)
    number=qs.count()
    context ={
        'queryset':qs,
        'n' : number,
        'products': Product.objects.all(),
        'categories': LU_Category.objects.all(),
        'Item': LU_Item.objects.all(),
    }
    return render(request,'pages/filter.html',context)

###############################################################################


def is_valid_queryparam(param):
    return param!="" and param is not None

###############################################################################


@decorators.login_required(login_url='/login/')
def compare(request):
    project_1=request.GET.get('project_1')
    project_2=request.GET.get('project_2')
    category = request.GET.get('category')
    product = request.GET.get('product')
    item = request.GET.get('item')
    value= request.GET.get('value')
    different = request.GET.get('different')

    project_list=[]
    with connection.cursor() as cursor:
        cursor.callproc('GetAllProducts',[])
        query=cursor.fetchall()
    

    for i in query: 
        project_list.append(i[1])
    project_list=list(set(project_list))
    project_list.sort()

    if different == 'on':
        diff=True
    else:
        diff=False
###############################################################################

    param_1=[project_1,project_2,product,category,item,diff]

###############################################################################

    with connection.cursor() as cursor:
        cursor.callproc('CompareProc',param_1)
        query_1=cursor.fetchall()

###############################################################################
    param_2=[project_1,project_2]

###############################################################################

    with connection.cursor() as cursor:
        cursor.callproc('GetProjectDetail',param_2)
        query_2=cursor.fetchall()

###############################################################################

    number=len(query_1)
    context ={
        "projects":project_list,
        'n' : number,
        'project':query_1,
        'detail':query_2,
        'number':number,
        'products': Product.objects.all(),
        'categories': LU_Category.objects.all(),
        'Item': LU_Item.objects.all(),
    }
    return render(request,'pages/compare.html',context)

##############################################################################
#@decorators.login_required(login_url='/login/')
@decorators.permission_required('database.can_delete', login_url='/login/') #allow only admin to use the copy function
def copy_function(request):
    qs=ASO_Configuration.objects.all()
    project_list=[]
    full_project_list=[]
    project_1=request.GET.get('project_1')
    project_2=request.GET.get('project_2')
    customer = request.GET.get('customer_2')

    with connection.cursor() as cursor:
        cursor.callproc('GetAllProducts',[])
        query=cursor.fetchall()
    

    for i in query:
        #a=[i[1],i[2]]
        project_list.append(i[1])

    project_list=list(set(project_list))
    project_list.sort()

    if "copy" in request.POST:
        full_project_list.clear()
    
    for i in project_list:
        full_project_list.append([i,qs.filter(Project=i).count()])
    
    
###############################################################################

    if project_2 is not None : # check project        input yet?
        if project_2 is not None and len(customer) != 0: # check project and customer input yet?
            if not project_2.isdecimal():
                messages.error(request,'Project must contain only digit number (0-9)!')

            elif project_list.count(int(project_2)) == 1:
                #return HttpResponse('<h1> Project exists </h1>')
                messages.error(request,'Project exists in the database!')

            elif len(project_2) != 7:
                messages.error(request,'Project must contain 7 digits number (0-9)!')
            
            #elif c != 7:
            #elif int(project_2) < 1000000 or int(project_2) > 9999999:
            elif not 999999 < int(project_2) < 10000000:
                messages.error(request,'Project must in range 1000000 to 9999999!')

            elif project_1 == 'Choose...':
                messages.error(request,'Please choose the project source to copy!')

            else:
                #messages.info(request,'Please wait! Process copy in progress!')
                param=[project_1,project_2,customer]
                with connection.cursor() as cursor:
                    cursor.callproc('CopyProc',param)
                
                                

                qs=ASO_Configuration.objects.all()
                time.sleep(5) # time delay to copy function run
                number_1= qs.filter(Project=project_1).count()
                number_2= qs.filter(Project=project_2).count()

                if number_1 != number_2:
                    messages.error(request,'Copy error!!!')
                else:
                    messages.success(request,'Copy successfully. Please refresh to load data')
                
        elif len(customer)== 0:
            #return HttpResponse('<h1>Please enter name new customer</h1>')
            messages.error(request,'Please enter name new customer!')
    # else:
    #     messages.error(request,'Please enter name new project!')       
###############################################################################

    context ={"projects":project_list,"full_projects":full_project_list}
    return render(request,'pages/copy_function.html',context)

###############################################################################
###############################################################################

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'pages/signup.html', {'form': form})

###############################################################################