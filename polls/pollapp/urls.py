from django.urls import path
from django.http import HttpResponse
from . import views
from pollapp import views
from django.conf import settings
from django.conf.urls.static import static
from pollapp.views import UserindexView, AccountActivation, ProfileUpdate, PasswordChange, url_shortner, userLogin, Home

app_name = 'polls'
urlpatterns = [

    path('index/', views.IndexView.as_view(), name='index'),
    path('<int:question_id>/', views.DetailView.as_view(), name='detail'),
    path('<int:question_id>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.PollView.as_view(), name='vote'),
    path('register/', views.RegisterView.as_view(), name='register'),
    #path('sum', views.sum, name='sum'),

path('', views.Home,name='home'),
    #path('mysession', views.mysession, name='mysession'),
    path('userindexview/', UserindexView.as_view(), name='userindexview'),
    #path('userlogin/',views.LoginView.as_view(),name="userlogin"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>',AccountActivation.as_view(), name='activate'),

    path('update/', views.ProfileUpdate.as_view(), name='update'),
    path('password/', views.PasswordChange.as_view(), name='password'),
    path('email', views.email,name='email'),
    #path('trial', views.trial.as_view(), name='trial'),
    #path('trial', views.trial, name='trial'),
    #path('email', views.email.as_view(), name='email'),


    path('paypal', views.Paypall.as_view(), name='paypal'),
    path('email_list_signup', views.email_list_signup, name='email_list_signup'),
    path('weather', views.Weather.as_view(), name='weather'),

    path('url-shortner',url_shortner.as_view(),name="url-shortner"),
    path('userlogin/', views.userLogin.as_view(), name="userlogin"),

    path('news', views.News_Application.as_view(),name="news"),


    path('barcode', views.Barcode.as_view(), name="barcode"),

    path('QRCodeGenerator', views.Qrcode.as_view(), name='QRCodeGenerator'),

    path('delete_view/<id>', views.Delete_View.as_view(), name='delete_view'),



path('screenshot', views.screenshot.as_view(),name='screenshot')]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)





