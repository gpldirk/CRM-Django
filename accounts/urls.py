from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('customer/<str:customer_id>/', views.customer, name="customer"),
    path('create_order/<str:customer_id>', views.create_order, name='create_order'),
    path('update_order/<str:order_id>/', views.update_order, name='update_order'),
    path('delete/<str:order_id>', views.delete_order, name='delete_order'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_page, name='logout'),
    path('user/', views.user_page, name='user'),
    path('profile/', views.user_profile, name='profile'),

    # send password reset form
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name="password_reset"),
    # send password reset email
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name="password_reset_done"),
    # check password reset token with encoded uid
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'), name="password_reset_confirm"),
    # send password reset ok message
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'), name="password_reset_complete"),

]