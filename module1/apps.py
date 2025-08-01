from django.apps import AppConfig


class Module1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'module1'
     
    def ready(self):
       import module1.signals

 
 