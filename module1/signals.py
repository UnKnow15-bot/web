from django.db.models.signals import pre_save, post_save
from .models import Task, Blog
from django.dispatch import receiver




@receiver(post_save, sender=Task)
def after_save_task(sender,instance, created, **kwargs):
    if created:
        Blog.objects.create(title="create a blog", content=" ... ")
    else:
        print("Task was not created.")