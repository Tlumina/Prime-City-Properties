from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def robots_txt(request):
    content = "User-agent: *\nDisallow: /admin/\nSitemap: " + request.build_absolute_uri('/sitemap.xml')
    return HttpResponse(content, content_type="text/plain")

def sitemap_xml(request):
    from apps.properties.models import Property
    properties = Property.objects.filter(is_published=True)
    urls_xml = "".join([f"<url><loc>{request.build_absolute_uri(p.get_absolute_url())}</loc><lastmod>{p.updated_at.strftime('%Y-%m-%d')}</lastmod><changefreq>weekly</changefreq></url>" for p in properties])
    xml_content = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9"><url><loc>{request.build_absolute_uri("/")}</loc></url><url><loc>{request.build_absolute_uri("/listings/")}</loc></url>{urls_xml}</urlset>'
    return HttpResponse(xml_content, content_type="application/xml")

from django.views.static import serve
from django.urls import re_path

handler404 = 'core.views.custom_404_view'
handler500 = 'core.views.custom_500_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('accounts.urls')),
    path('listings/', include('properties.urls')),
    path('tour/', include('tours.urls')),
    path('contact/', include('contact.urls')),
    path('robots.txt', robots_txt),
    path('sitemap.xml', sitemap_xml),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


