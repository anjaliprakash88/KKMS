from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.db import IntegrityError
from django.http import JsonResponse
from accounts.models import Customer,NewsEvents,Banners, Payment, AboutUs, CharityManagement
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
User = get_user_model()

def banner_list_view(request):
    banners = Banners.objects.filter(is_active=True).order_by("-id")
    return render(request, "super_admin/banner.html", {"banners": banners})


def banner_add_view(request):
    if request.method == "POST":
        banner_image = request.FILES.get("banner_image")
        banner_text1 = request.POST.get("banner_text1")
        banner_text2 = request.POST.get("banner_text2")
        banner_text3 = request.POST.get("banner_text3")
        status = request.POST.get("status") or 1

        Banners.objects.create(
            banner_image=banner_image,
            banner_text1=banner_text1,
            banner_text2=banner_text2,
            banner_text3=banner_text3,
            status=status
        )
        messages.success(request, "Banner added successfully!")
        return redirect("banner-list")    

def banner_edit(request, pk):
    banner = get_object_or_404(Banners, pk=pk)
    if request.method == "POST":
        banner.banner_text1 = request.POST.get("banner_text1")
        banner.banner_text2 = request.POST.get("banner_text2")
        banner.banner_text3 = request.POST.get("banner_text3")
        banner.status = request.POST.get("status")
        if request.FILES.get("banner_image"):
            banner.banner_image = request.FILES.get("banner_image")
        banner.save()
        return redirect("banner-list")  # redirect to the banner table page

    return redirect("banner-list")

def banner_delete(request, pk):
    banner = get_object_or_404(Banners, pk=pk)
    banner.is_active = False  # soft delete
    banner.save()
    return redirect('banner-list') 


def contact(request):
    return render(request, "accounts/contact.html")
    
def privacy_policy(request):
    return render(request, "accounts/privacy_policy.html")


def terms(request):
    return render(request, "accounts/terms.html")

def charity_view(request):
    """
    Display all charity items.
    """
    charities = CharityManagement.objects.all()  # Get all charity entries
    return render(request, "accounts/charity.html", {"charities": charities})

def about(request):
    about_us = AboutUs.objects.first()  
    images = about_us.images.all() if about_us else []  

    context = {
        "about_us": about_us,
        "images": images,
    }

    return render(request, "accounts/about.html", context)

def home(request):
    banners = Banners.objects.filter(status=1).order_by("-id") 
    news_articles = NewsEvents.objects.filter(status=1).order_by("-id")
    return render(
        request,
        "accounts/index.html",
        {
            "banners": banners,
            "news_articles": news_articles,
        },
    )


@login_required
def customer_list(request):
    customers = Customer.objects.select_related('user').all()  # fetch related user
    return render(request, 'super_admin/customers.html', {'customers': customers})



@login_required
def customer_dashboard(request):
    # Ensure the logged-in user is a customer
    if not hasattr(request.user, "customer_profile"):
        return redirect("login")  # redirect non-customers to login or error page

    customer = request.user.customer_profile  # get Customer object
    return render(request, "customer_dashboard/dashboard.html", {"customer": customer})


def customer_login(request):
    if request.method == "POST":
        identifier = request.POST.get("email_or_mobile")
        password = request.POST.get("password")

        # Try to authenticate using email first, then phone
        user = authenticate(request, email=identifier, phone=identifier, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.email}!")
            return redirect("customer_dashboard")  # replace with your dashboard URL
        else:
            messages.error(request, "Invalid email/phone or password.")

    return render(request, "customer/login.html")

def register_customer(request):
    if request.method == "POST":
        # Get basic user info
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Set username to email
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            is_customer=True
        )

        # Create Customer record
        customer = Customer.objects.create(
            user=user,
            father_name=request.POST.get("father_name"),
            age=request.POST.get("age") or None,
            gender=request.POST.get("gender"),
            contact_no=request.POST.get("mobile"),
            description=request.POST.get("expectation"),
            profile_image=request.FILES.get("profile_image"),
            id_proof=request.POST.get("id_proof"),
            address=request.POST.get("current_address"),
            star=request.POST.get("customer_star") or None,
            married_sisters=request.POST.get("married_sisters"),
            married_brothers=request.POST.get("married_brothers"),
            no_sisters=request.POST.get("no_sisters"),
            no_brothers=request.POST.get("no_brothers"),
            mother_job=request.POST.get("mother_job"),
            father_job=request.POST.get("father_job"),
            mother_name=request.POST.get("mother_name"),
            landline_no=request.POST.get("landline_no") or None,
            year=request.POST.get("year"),
            school=request.POST.get("school"),
            education=request.POST.get("education"),
            income=request.POST.get("monthly_income"),
            job_city=request.POST.get("job_city"),
            job_department=request.POST.get("job_department"),
            company=request.POST.get("company"),
            job=request.POST.get("job"),
            caste=request.POST.get("caste"),
            marital_status=request.POST.get("marital_status"),
            physical_condition=request.POST.get("physical_condition"),
            weight=request.POST.get("weight"),
            complexion=request.POST.get("complexion"),
            height=request.POST.get("height"),
            time_birth=request.POST.get("birth_time"),
            place_birth=request.POST.get("birth_place"),
            dob=request.POST.get("dob"),
            district=request.POST.get("district"),
            city=request.POST.get("city"),
            post=request.POST.get("post"),
            pin_code=request.POST.get("pincode"),
            street=request.POST.get("street"),
            house_name=request.POST.get("house_name"),
            status=request.POST.get("status") or None,
            is_active=request.POST.get("is_active") or 0,
            dosham=request.POST.get("dosham"),
        )

        messages.success(request, "Customer registered successfully!")
        return redirect("register_customer")  # redirect back to form

    return render(request, "customer/register.html")




def news_delete(request, pk):
    news = get_object_or_404(NewsEvents, id=pk)
    
    # Delete the image file if it exists
    if news.image:
        image_path = news.image.path
        if os.path.isfile(image_path):
            os.remove(image_path)
    
    # Delete the database record
    news.delete()
    
    return redirect('news_list')

def news_update(request):
    if request.method == "POST":
        news_id = request.POST.get("news_id")
        news = NewsEvents.objects.get(id=news_id)
        news.title = request.POST.get("title")
        news.content = request.POST.get("content")
        news.status = request.POST.get("status", 1)

        if request.FILES.get("image"):
            news.image = request.FILES.get("image")
        news.save()
        return redirect('news_list')
    return redirect('news_list')

def news_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        status = request.POST.get("status", 1)
        image = request.FILES.get("image")

        NewsEvents.objects.create(
            title=title,
            content=content,
            status=status,
            image=image
        )
        return redirect('news_list')  # reload page after adding
    return redirect('news_list')

def news_list(request):
    news_list = NewsEvents.objects.all().order_by('-id')  # latest first
    return render(request, 'super_admin/news.html', {'news_list': news_list})

# ------------SUPERADMIN LOGOUT------------
def custom_admin_logout(request):
    logout(request)
    return redirect("super_admin_login")

# ------------SUPERADMIN LOGIN------------
def custom_admin_login(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        return redirect("super_admin_dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember = request.POST.get("remember")

        user = authenticate(request, username=username, password=password)
        print("AUTH RESULT:", user)
        if user is not None:
            login(request, user)
            
            if not remember:
                request.session.set_expiry(0)

            if user.is_superadmin:
                return redirect("super_admin_dashboard")
            else:
                return redirect("user_dashboard")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("super_admin_login")
    
    return render(request, "super_admin/login.html")


# ------------SUPERADMIN DASHBOARD------------
@login_required(login_url="super_admin_login")
def custom_admin_dashboard(request):
    total_customers = Customer.objects.count()

    # Fetch Total Published News
    published_news = NewsEvents.objects.filter(status=1).count()

    # Fetch Active Banners
    active_banners = Banners.objects.filter(status=1).count()

    # Fetch Total Revenue
    total_revenue = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'total_customers': total_customers,
        'published_news': published_news,
        'active_banners': active_banners,
        'total_revenue': total_revenue,
    }
    return render(request, "super_admin/dashboard.html", context)    
