from django.apps import AppConfig


class MedicalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medical'
    verbose_name = 'Sistema Médico'
    
    def ready(self):
        """Register signals when the app is ready."""
        import medical.signals  # Import signals here to avoid circular import
