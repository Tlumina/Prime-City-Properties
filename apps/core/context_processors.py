from .models import SiteSetting


def site_settings(request):
    """
    Inject global site settings into all templates.
    """
    try:
        settings_obj = SiteSetting.load()
    except Exception:
        settings_obj = None
    return {
        'site_settings': settings_obj
    }
