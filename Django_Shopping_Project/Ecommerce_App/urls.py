from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm


urlpatterns = [
    path('', views.ProductView.as_view(), name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('mobile/', views.MobileView.as_view(), name='mobile'),
    path('mobile/<slug:data>', views.MobileView.as_view(), name='mobiledata'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='registration'),
    path('logout/', views.logoutview, name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),


    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    
    
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.AddressView.as_view(), name='address'),
    path('add-to-cart/', views.AddtoCartView.as_view(), name='add-to-cart'),
    path('cart/', views.ShowCartView.as_view(), name='showcart'),
    path('empty/', views.empty, name='emptycart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.minus_cart, name='removecart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('paymentdone/', views.PaymentdoneView.as_view(), name='paymentdone'),
    path('orders/', views.ordersview.as_view(), name='orders'),
    path('buynow/', views.buynow, name='buynow'),
    path('about/', views.about, name='about'),
   
  

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)