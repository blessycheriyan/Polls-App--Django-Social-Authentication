
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    objects = None
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


from django_countries.fields import CountryField
class Profile(models.Model):
    objects = None
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True,null=True,upload_to='images')
    phone = models.CharField(blank=True,null=True,max_length=10)
    country=CountryField()


    def get_image(self):
        try:
            url = self.profile_pic.url
        except:
            url = ''
        return url



class newsletter(models.Model):
    email = models.EmailField(max_length=100,unique=True)

    def __str__(self):
        return self.email
import barcode
from io import BytesIO
from barcode.writer import ImageWriter
from django.core.files import File
class Product(models.Model):
    name = models.CharField(max_length=100)
    barcode = models.ImageField(upload_to = 'barcode', blank=True)
    batch_number = models.CharField(max_length=12,null=True,unique=True)

    def save(self, *args, **kwargs):
        EAN = barcode.get_barcode_class('ean13')
        ean = EAN(f'{self.batch_number}', writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        self.barcode.save('barcode.png',File(buffer),save=False)
        return super().save(*args, **kwargs)



class QRCode(models.Model):
    url = models.URLField()
    image = models.ImageField(upload_to='qrcode',blank=True)

    def save(self,*args,**kwargs):

        super().save(*args,**kwargs)
    '''@property
    def qr(self):
        try:
            s = self.image.url
        except:
            s=""
        return s
    '''
class emp(models.Model):
    name = models.CharField(max_length=23)
    address = models.CharField(max_length=23)
    location = models.CharField(max_length=23)

