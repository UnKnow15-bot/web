from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import User, Task, Category, Course, Contact, Blog, Cart , CartItem
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings
import random 
import string
from django.db.models import Q
from .forms import ContactForm
from django.core.paginator import Paginator

import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY

def  create_checkout_session(request,course_id):
    if 'user_id' not in request.session:
        return redirect('login')
    course =  Course.objects.filter(id=course_id).first()


    session =stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items =
    [
        {
            'price_data':{
                            'currency':'inr',
                            'product_data':{'name': course.name,},
                            'unit_amount':int(course.price*100),
                          },
            'quantity':1,
        }
    ],
    mode='payment',
    success_url = "http://127.0.0.1:8000/",
    cancel_url = "http://127.0.0.1:8000/contact"

    )
    return redirect(session.url)
 
 



def home(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    user = User.objects.get(id=request.session['user_id'])

    tasks = Task.objects.all()
    # print(students)
    return render(request,'home.html', {'tasks': tasks, 'user':user} )


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password != confirm:
            messages.error(request, 'Password and confirm password do not match !')
            return redirect('login')
            
        user = User.objects.filter(email=email).first()

        if user:
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                messages.success(request, 'Login successfully !')
                return redirect('home')
            else:
                messages.error(request, 'Invalid password !')
                return redirect('login')
        else:
            messages.error(request, 'User not found !')
            return redirect('login')
        
    return render(request,'login.html')
 
def logout(request):

    request.session.flush()

    messages.success(request, 'Logout successfully !')
    return redirect('login')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        
        User.objects.create(
            name=name,
            age=age,
            gender=gender,
            email=email,
            password=make_password(password)
        )
     
        return redirect('home')
    
    return render(request, 'register.html')



def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
         
        Task.objects.create(
            title=title,
            description=description
        )
        return redirect('home')
    return render(request, 'add_task.html')

def delete_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    task.delete()
    return redirect('home')

def update_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.save()
        
        return redirect('home')
    
    return render(request, 'update_task.html', {"task": task })



def about(request):
    if 'user_id' not in request.session:
        return redirect('login')
    blogs = Blog.objects.all()
    return render(request, 'about.html', {'blogs': blogs})

def contact(request):
    contact_form = ContactForm()
    if request.method=='POST':
        contact =  ContactForm(request.POST)
        if contact.is_valid():
            contact.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('home')

    return render(request, 'contact.html', {'contact_form': contact_form})


def send_otp(request):

    user = User.objects.get(id=request.session['user_id'])

    charc =  string.digits
    otp = ''.join(random.choice(charc) for _ in range(6))
    print(otp)
    send_mail(
        subject='OTP for your account',
        message=f'Your OTP is {otp}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[],
        fail_silently=False
    )
    return redirect('login')



def course_form(request):
    categories =  Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        is_avail = 'is_avail' in request.POST
        image = request.FILES.get('image')
        file = request.FILES.get('file')

        category_id = request.POST['category']
        category = Category.objects.get(id=category_id)
        
        Course.objects.create(
            name=name,
            price=price,
            is_avail=is_avail,
            image=image,
            file=file,
            category=category
        )
        return redirect('home')
    return render(request, 'course_form.html', {'categories': categories})




def course_list(request):

    query = request.GET.get('q','')
    if query:
        courses = Course.objects.filter(  Q(name__icontains=query) | Q(category__name__icontains=query) )

    else:
        courses = Course.objects.all()


    
    paginator = Paginator(courses, 3)
    page_number = request.GET.get('page')    
    page_obj = paginator.get_page(page_number)

    return render(request, 'course_list.html', {'page_obj': page_obj, 'query':query})



def blog_details(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'blog_detail.html', {'blog': blog})





def buy_now(request):

    user = User.objects.get(id=request.session['user_id'])
    course = Course.objects.filter(id=9).first()

    course.user.add(user)
    print(course.user)
    course.save()
    return redirect('home')





 
def google_login_success(request):
    # This user is authenticated by Google and available in request.user
    social_user = request.user

    if not social_user.is_authenticated:
        messages.error(request, 'Google login failed!')
        return redirect('login')

    # Get email from Google account
    email = social_user.email
    name = social_user.get_full_name()

    # Check if user exists in your custom User model
    user = User.objects.filter(email=email).first()

    if not user:
        # Create new user in your custom table
        user = User.objects.create(
            name=name,
            email=email,
            gender='Other',  # Or skip/default
            age=0,
            password=''  # Not needed since login is via Google
        )

    # Set session manually
    request.session['user_id'] = user.id
    messages.success(request, 'Login with Google successful!')

    return redirect('home')
 
from django.shortcuts import get_object_or_404, redirect
from .models import Cart, CartItem, Course

def add_to_cart(request, course_id):
    user = User.objects.get(id=request.session['user_id'])  # Or use request.user if logged in
    course = get_object_or_404(Course, id=course_id)

    cart, _ = Cart.objects.get_or_create(user=user)

    # Try to get item, but don't save yet
    item = CartItem.objects.filter(cart=cart, course=course).first()
    if item:
        item.quantity += 1
    else:
        item = CartItem(cart=cart, course=course, quantity=1)

    item.total_price = item.quantity * course.price
    item.save()

    # Recalculate cart totals
    cart_items = cart.items.all()
    subtotal = sum(i.total_price for i in cart_items)
    discount = cart.discount or 0
    cart.subtotal = subtotal
    cart.grandtotal = subtotal - discount
    cart.save()

    return redirect('view_cart')

 
def remove_from_cart(request, course_id):
    user = User.objects.get(id=request.session['user_id'])
    cart = Cart.objects.filter(user=user).first()
    if not cart:
        return redirect('view_cart')

    item = CartItem.objects.filter(cart=cart, course_id=course_id).first()
    if item:
        item.delete()

        # Recalculate totals
        subtotal = sum(i.total_price for i in cart.items.all())
        cart.subtotal = subtotal
        cart.grandtotal = subtotal - cart.discount
        cart.save()

    return redirect('view_cart')
 

def view_cart(request):
    user = User.objects.get(id=request.session['user_id'])
    cart = Cart.objects.filter(user=user).first()
    items = cart.items.all() if cart else []
    return render(request, 'cart.html', {'cart': cart, 'items': items})

 
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse

@csrf_exempt  # Only for testing without CSRF token. Remove in production.
def update_cart(request, course_id):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['user_id'])
        cart = Cart.objects.filter(user=user).first()
        if not cart:
            return redirect('view_cart')

        item = CartItem.objects.filter(cart=cart, course_id=course_id).first()
        if not item:
            return redirect('view_cart')

        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1

        if quantity <= 0:
            item.delete()
        else:
            item.quantity = quantity
            item.total_price = quantity * item.course.price
            item.save()

        # Update cart totals
        subtotal = sum(i.total_price for i in cart.items.all())
        discount = cart.discount or 0
        cart.subtotal = subtotal
        cart.grandtotal = subtotal - discount
        cart.save()

    return HttpResponseRedirect(reverse('view_cart'))





from rest_framework import viewsets
 
from .serializers import ContactSerializer, TaskSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

 # views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task

# List all tasks
class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

# View a single task
class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'

# Create a new task
class TaskCreateView(CreateView):
    model = Task
    fields = ['title', 'description']
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

# Update an existing task
class TaskUpdateView(UpdateView):
    model = Task
    fields = ['title', 'description']
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

# Delete a task
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('task-list')
