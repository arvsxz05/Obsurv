from django.apps import AppConfig


class ProfileConfig(AppConfig):
    name = 'Profile'

    def ready(self):
    	""" activate signals """
    	from Profile import signals