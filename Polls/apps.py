from django.apps import AppConfig


class PollsConfig(AppConfig):
    name = 'Polls'

    def ready(self):
    	""" activate signals """
    	from Polls import signals
