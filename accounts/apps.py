from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    # overwrite ready func to use signals
    def ready(self):
    	import accounts.signals
