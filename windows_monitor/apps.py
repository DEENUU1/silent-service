from django.apps import AppConfig


class WindowsMonitorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'windows_monitor'

    def ready(self):
        import windows_monitor.signals
