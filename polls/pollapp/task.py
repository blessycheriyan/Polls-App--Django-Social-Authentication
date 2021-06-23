from celery import shared_task


@shared_task(name="homepage")
def add(x):


        return 'homepage.html'
