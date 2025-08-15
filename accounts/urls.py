from django.urls import path, include
from .import views


urlpatterns = [
    path('', views.home, name="home"),
    path("about/", views.about, name="about"),
    path("charity/", views.charity_view, name="charity"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms-and-conditions/", views.terms, name="terms"),
    path("contact/", views.contact, name="contact"),

    path("super-admin/login/", views.custom_admin_login, name="super_admin_login"),
    path("logout/", views.custom_admin_logout, name="super_admin_logout"),
    path("super-admin/dashboard/", views.custom_admin_dashboard, name="super_admin_dashboard"),


    path('news/', views.news_list, name='news_list'),
    path('news/create/', views.news_create, name='news_create'),
    path('news/update/', views.news_update, name='news_update'),
    path('news/delete/<int:pk>/', views.news_delete, name='news_delete'),

    path("banners/", views.banner_list_view, name="banner-list"),
    path("banners/add/", views.banner_add_view, name="banner-add"),
    path("banners/<int:pk>/edit/", views.banner_edit, name="banner-edit"),
    path("banners/<int:pk>/delete/", views.banner_delete, name="banner-delete"),

    path('customers/', views.customer_list, name='customer-list'),

    path("about-us/", views.about_us_list, name="about-us-list"),
    path('about-us/add/', views.about_us_add, name='about-us-add'),


    path('register-customer/', views.register_customer, name='register_customer'),
    path('customer-login/', views.customer_login, name='customer-login'),
    path("customer/dashboard/", views.customer_dashboard, name="customer_dashboard"),
]

