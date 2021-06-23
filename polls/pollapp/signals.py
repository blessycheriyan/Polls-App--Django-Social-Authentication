from django.contrib.auth.models import User
from django.core.signals import request_started, request_finished, setting_changed
from django.db.models.signals import pre_save, post_delete, pre_delete, pre_migrate, post_migrate
from django.dispatch import receiver, Signal
from django.contrib.auth.signals import user_login_failed, user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.test.signals import template_rendered


@receiver(user_login_failed)
def login_failed(sender,request,credentials,**kwargs):
	request.session['failed'] += 1
	print(request.session['failed'])

''''
@receiver(pre_save,sender=User)
def model_psave(sender, instance, **kwargs):
	print("before model received")


@receiver(post_save,sender=User)
def model_postsave(sender, instance, **kwargs):
	print("after model received............")



@receiver(post_delete,sender=User)
def model_post_delete(sender, instance, **kwargs):
	print(" after deleted model received............")




@receiver(pre_delete,sender=User)
def model_pre_delete(sender, instance, **kwargs):
	print("deleted model received............")



@receiver(pre_migrate)
def p_migrate(sender,
			  app_config,verbosity,interactive,using,plan,apps, **kwargs):
	print(" Just Migrate START............")



@receiver(post_migrate)
def p_migrate(sender,
			  app_config,verbosity,interactive,using,plan,apps, **kwargs):
	print(" Just Migrate Completed............")



@receiver(request_started)
def request_beg(sender, **kwargs):
	print(" Request START............")

@receiver(request_finished)
def request_end(sender, **kwargs):
	print(" Request Finished............")



@receiver(setting_changed)
def ChangeSetting(sender,setting,value,enter, **kwargs):
	print("Setting Changed............")



@receiver(template_rendered)
def templateRendered(sender,template,context, **kwargs):
	print("template render...........")




@receiver(user_logged_out)
def logged_out_user(sender, request, user, **kwargs):
	print("User Logged Out Successfully............")



@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
	print("User Logged Successfully............")



notification=Signal(providing_args=['request','user'])


@receiver(notification)
def show_notification(sender, **kwargs):
	print("Notification")


'''