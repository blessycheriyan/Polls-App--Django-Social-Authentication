import pyshorteners
import random
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse, request
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic


from .forms import *
from .models import Question, Choice, Profile
from django.views.generic import View, TemplateView, RedirectView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from .utils import account_activation_token
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import UpdateView
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
decorators = [login_required, ]
from django.utils.translation import gettext as _

from django.utils.translation import get_language, activate, gettext
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        return Question.objects.all()[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    pk_url_kwarg = 'question_id'


# Get question and display results
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    pk_url_kwarg = 'question_id'


class PollView(generic.View):
    model = Question

    # asusual function
    def post(self, request, *args, **kwargs):

        question = get_object_or_404(self.model, pk=kwargs.get('question_id'))
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            if request.is_ajax():
                return JsonResponse({'message': "You didn't select a choice"})
            return render(request, 'polls/detail.html', {

                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()

            # user hits the Back button.
            if request.is_ajax():
                return JsonResponse({'message': 'Success'})
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



class LoginView(View):

    def get(self, request):
        return render(request, 'login/userlogin.html')

    def post(self, request, meessages=None):


        username = request.POST.get('username')
        password = request.POST.get('passw')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("polls:userindexview"))
        else:
            messages.error(request, 'Please Check Your Username & Password')
            return redirect('polls:userlogin')


from contactforms.forms import ContactForm

from django.views.decorators.cache import cache_page
@cache_page(60*5)
def Home(request):
        request.session.get_expiry_at_browser_close()

        forms = ContactForm()
        trans = translate(language='fr')
        return render(request, 'homepage.html', {'trans': trans,'forms':forms})



class translate(TemplateView):
    def get_context_data(self, language,**kwargs):
        cur_language = get_language()
        try:
            activate(language)
            text = gettext('Polling System')
            text1 = gettext('Welcome to')

            text2 = gettext(
                'At least 60 per cent of the country wants the strikers to win, polls show in our website · We are doing a weekly poll on the president, and clearly his popularity has declined.')
            text3 = gettext(
                'A sampling or collection of opinions on a subject, taken from either a selected or a random group of persons, as for the purpose of analysis.')
            text4 = gettext('Read More')
        finally:
            activate(cur_language)
        return text, text1, text2, text3, text4



class UserindexView(TemplateView):
    template_name = "pages/index.html"


class LogoutView(View):
      def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)


def email(a, b):
    subject = 'Activation Email through Account'
    message = a
    email_from = settings.EMAIL_HOST_USER
    recipient_list = {b, }
    send_mail(subject, message, email_from, recipient_list)
    return redirect('polls:register')


class RegisterView(View):
    def get(self, request):

        f1 = userform()
        f2 = UserProfileForm()
        f3 = CaptchaForm()

        context = {
            'f1': f1,
            'f2': f2,
            'f3': f3,
        }
        return render(request, "registration/register.html", context)


    def post(self, request):
        user_form = userform(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)

            user.active = False
            user.save()

            profile = profile_form.save(commit=False)

            profile.user = user
            profile.save()
            print("sucessssssssssssssssssssssssss")
            to_email = user.email
            print(to_email)
            user =  user_form.save(commit=False)
            user.is_active = False

            user.save()
            uname = user.username
            current_Site = get_current_site(request).domain
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            _x = reverse("polls:activate", kwargs={'uidb64': uid, 'token': token})
            myrl = 'http://' + current_Site + _x
            msg = "Welcome To PollApp Website" + "\n" "Hello" + "\t" + str(
                user.username) + "\n" "Please Click the below link and activate your account" + "\n" + myrl
            email(msg, to_email)
            messages.success(request, 'Please check your email and confirm your account')
            return redirect(reverse('polls:register'))


        else:
            print(user_form.errors)
            messages.error(request, user_form.errors)
            return redirect(reverse('polls:register'))


class Delete_View(View):
    def get(self, request,id, *args, **kwargs):
        f1 = User.objects.get(pk=id)
        print(f1)
        f1.delete()
        return redirect('/')

from .task import add
from django.http import HttpResponse
#from .signals import notification

def Home(request):
    #add.delay(0)
    #notification.send(sender=None,request=request,user=['john'])
    forms = ContactForm()
    trans = translate(language='fr')
    return render(request, 'homepage.html', {'trans': trans, 'forms': forms})


class AccountActivation(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if user is not None and account_activation_token.check_token(user, token):
                user.is_active = True

                user.save()

                messages.success(request,
                                 'Account activated successfully ,Thank you for your email confirmation. Now you can login your account')
                return redirect('polls:userlogin')



            if user.is_active:


                return redirect('polls:userlogin')


        except:
            return HttpResponse('<center><h1>Activation link is expired!<h1></center>')






@method_decorator(decorators, name='dispatch')

class ProfileUpdate(generic.View):
    def get(self, request):
        Profile.objects.get_or_create(user=request.user)
        f1 = userformedit(instance=request.user)
        f2 = UserProfileForm(instance=request.user.profile)

        context = {
            'f1': f1,
            'f2': f2,
        }
        return render(request, "userprofiles/userprofile.html", context)

    def post(self, request):
        Profile.objects.get_or_create(user=request.user)
        user_obj = userformedit(request.POST, instance=request.user)
        pro1_obj = UserProfileForm(request.POST,request.FILES or None,instance=request.user.profile)

        if user_obj.is_valid() and pro1_obj.is_valid():

            user_obj.save()
            pro1_obj.save()
            if request.is_ajax():
                return JsonResponse({'message': 'Success'})

            return redirect('polls:update')

        else:
            #print("error=", user_obj.errors)
            messages.error(request, user_obj.errors)
            messages.error(request, pro1_obj.errors)

            if request.is_ajax():
                return JsonResponse({'message': "erorr"})

            return HttpResponseRedirect(reverse('polls:update'))


@method_decorator(decorators, name='dispatch')
class PasswordChange(View):
    def get(self, request):

        f2 = PasswordChangeForm(user=request.user)

        context = {

            'f2': f2,
        }
        return render(request, "registration/changepassword.html", context)

    def post(self, request, *args, **kwargs):
        user_obj = PasswordChangeForm(data=request.POST,user=request.user)

        print(user_obj)
        if user_obj.is_valid():
            user_obj.save()



            print("update")

            return redirect('polls:userindexview')

        else:
            print("error=", user_obj.errors)
            messages.error(request, user_obj.errors)

            return HttpResponseRedirect(reverse('polls:password'))


class Paypall(TemplateView):
    template_name = "paypal.html"

from django.conf import settings
from .forms import NewsletterForm
import json
import requests

MAILCHIMP_API_KEY = settings.MAILCHIMP_API_KEY
MAILCHIMP_DATA_CENTER = settings.MAILCHIMP_DATA_CENTER
MAILCHIMP_EMAIL_LIST_ID = settings.MAILCHIMP_EMAIL_LIST_ID

api_url = ''.format(dc=MAILCHIMP_DATA_CENTER)
members_endpoint = '{api_url}/lists/{list_id}/members'.format(
    api_url=api_url,
    list_id=MAILCHIMP_EMAIL_LIST_ID
)


def subscribe(email):
    data = {
        "email_address": email,
        "status": "subscribed"
    }
    r = requests.post(
        members_endpoint,
        auth=("", MAILCHIMP_API_KEY),
        data=json.dumps(data)
    )
    return r.status_code, r.json()


def email_list_signup(request):

    if request.method == "POST":
        fm = NewsletterForm(request.POST)
        if fm.is_valid():
           email=fm.cleaned_data['email']
           fm.save()
           subscribe(email)
    else:
        fm=NewsletterForm()


    context={'fm':fm}
    return render(request,"homepage.html",context)



from datetime import datetime

class Weather(View):

    def get(self, request,*args, **kwargs):
        url = ""
        api_key = ''
        cityname = request.GET.get('city')
        try:

            if cityname is None:
                context = {
                    'date': datetime.now,
                    'celsius': 'NA-/',
                    'country': 'NA-/',
                    'celsius': 'NA-/',
                    'fahrenheit': 'NA-/',
                    'feel': 'NA-/',
                    'wind_speed': 'NA-/',
                    'weather': 'NA-/',
                    'pressure': 'NA-/',
                    'humidity': 'NA-/',
                    'visibility': 'NA-/'}
                return render(request, 'weather.html', context)
            else:
                response = requests.get(url + cityname + '&appid=' + api_key).json()
                cel = response['main']['temp_max'] - 273.15
                fr = cel * 9 / 5 + 32
                city = response['name']
                country = response['sys']['country']
                feel = response['main']['feels_like']
                wind_speed = response['wind']['speed']
                weather = response['weather'][0]['description']
                pressure = response['main']['pressure']
                humidity = response['main']['humidity']
                visibility = response['visibility']

                next_5_day_url = ""
                next_5_day_url_response = requests.get(
                    next_5_day_url + cityname + '&mode=json' + '&appid=' + api_key).json()

                cel_5 = []
                fr_5 = []
                feel_5 = []
                wind_speed_5 = []
                weather_5 = []
                pressure_5 = []
                humidity_5 = []
                visibility_5 = []
                date_5 = []

                for i in range(0, 40):
                    cel_5.append(next_5_day_url_response['list'][i:i + 1][0]['main']['temp_max'] - 273.15)
                    fr_5.append(cel_5[i] * 9 / 5 + 32)
                    wind_speed_5.append(next_5_day_url_response['list'][i:i + 1][0]['wind']['speed'])
                    weather_5.append(next_5_day_url_response['list'][i:i + 1][0]['weather'][0]['main'])
                    pressure_5.append(next_5_day_url_response['list'][i:i + 1][0]['main']['pressure'])
                    humidity_5.append(next_5_day_url_response['list'][i:i + 1][0]['main']['humidity'])
                    visibility_5.append(next_5_day_url_response['list'][i:i + 1][0]['visibility'])
                    date_5.append(next_5_day_url_response['list'][i:i + 1][0]['dt_txt'])

                five_days_data = list(
                    zip(cel_5, fr_5, wind_speed_5, weather_5, pressure_5, humidity_5, visibility_5, date_5))

                context = {'date': datetime.now,
                           'celsius': cel,
                           'fahrenheit': fr,
                           'city': city,
                           'country': country,
                           'feel': feel,
                           'wind_speed': wind_speed,
                           'weather': weather,
                           'pressure': pressure,
                           'humidity': humidity,
                           'visibility': visibility,
                           'five_days_data': five_days_data,
                           }
                return render(request, 'weather.html', context)

        except:
            return render(request, 'error.html')

class url_shortner(View):

    def post(self,request):
        long_url = 'url' in request.POST and request.POST['url']
        pys = pyshorteners.Shortener()
        short_url = pys.tinyurl.short(long_url)
        return render(request,'urlShortner.html', context={'short_url':short_url,'long_url':long_url})

    def get(self,request):
        return render(request,'urlShortner.html')

from django.contrib.auth import authenticate, login


class userLogin(View):
    def get(self, request):
        return render(request, 'login/userlogin.html')

    def post(self, request):

        try:
            if request.session.get('failed') > 2:
                return HttpResponse('<h1> <center>You have to wait for 5 minutes to login again</center></h1>')
        except:
            request.session['failed'] = 0
            request.session.set_expiry(100)
        if request.method == 'POST':

            username = request.POST['username']
            password = request.POST['passw']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("polls:userindexview"))
            else:
                messages.error(request, 'Please Check Your Username & Password')
                return redirect('polls:userlogin')
        return render(request, 'login/userlogin.html')

import requests
from django.core.paginator import Paginator


class News_Application(View):
    paginate_by=2
    def get(self, request):
        url = ('')


        response = requests.get(url).json()
        author = []
        title = []
        description = []
        url = []
        image = []
        publishAt = []

        for i in range(len(response['articles'])):
            author.append(response['articles'][i]['author'])
            title.append(response['articles'][i]['title'])
            description.append(response['articles'][i]['description'])
            url.append(response['articles'][i]['url'])
            image.append(response['articles'][i]['urlToImage'])
            publishAt.append(response['articles'][i]['publishedAt'])

        headline_url = ('')

        headline_response = requests.get(headline_url).json()
        headline_author = []
        headline_title = []
        headline_description = []
        headline_url = []
        headline_image = []
        headline_publishAt = []

        for i in range(6):
            headline_author.append(headline_response['articles'][i]['author'])
            headline_title.append(headline_response['articles'][i]['title'])
            headline_description.append(headline_response['articles'][i]['description'])
            headline_url.append(headline_response['articles'][i]['url'])
            headline_image.append(headline_response['articles'][i]['urlToImage'])
            headline_publishAt.append(headline_response['articles'][i]['publishedAt'])

        News = list(zip(author, title, description, url, image, publishAt))
        headline = list(
            zip(headline_author, headline_title, headline_description, headline_url, headline_image,
                headline_publishAt))
        paginator = Paginator(News, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'news.html', context={'news': page_obj, 'headline': headline})








from .models import Product

class Barcode(View):
    def post(self, request, *args, **kwargs):
        p_name = request.POST['product-name']
        b_number = request.POST['batch-number']
        Product.objects.create(name=p_name, batch_number=b_number)
        messages.success(request, 'barcode generated')
        p = Product.objects.all()
        return render(request, 'barcode.html', {'p': p})

    def get(self, request, *args, **kwargs):

        p = Product.objects.all()
        return render(request, 'barcode.html', {'p': p})


from pollapp.models import QRCode

class Qrcode(View):

    def get(self, request, *args, **kwargs):
        qr_code = QRCode.objects.all()
        return render(request, 'qrcode.html', {'qr_code': qr_code})

    def post(self, request, *args, **kwargs):
        URL = request.POST.get('url')
        QRCode.objects.create(url=URL)
        pass

        qr_code = QRCode.objects.all()
        return render(request, 'qrcode.html', {'qr_code': qr_code})
'''
def trial(request):
    #data=list(User.objects.values())
    #return JsonResponse(data,safe=False)
    request.session['name']='h1'
    return render(request,'test.html')

class trial(RedirectView):

    url='/home'
    '''

import random
import pyautogui
from django.conf import settings
from django.contrib import messages


    class screenshot(View):
        def post (self,request):
            ss = pyautogui.screenshot()
            img = f'myimg{random.randint(1000, 9999)}.png'
            ss.save(settings.MEDIA_ROOT / img)
            messages.success(request, 'screenshot has been taken')
            return render(request, 'screenshot.html', {'img': img})



