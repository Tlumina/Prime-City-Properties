from django.shortcuts import render, get_object_or_404
from django.views import View
from properties.models import Property, Location, PropertyType
from properties.forms import PropertySearchFilterForm
from core.models import Testimonial, LegalPage


class HomeView(View):
    template_name = 'core/index.html'

    def get(self, request):
        search_form = PropertySearchFilterForm()
        featured_properties = Property.objects.filter(is_published=True, is_featured=True).select_related('location', 'property_type').prefetch_related('images')[:6]
        locations = Location.objects.filter(is_featured=True)[:6]
        categories = PropertyType.objects.all()[:6]
        testimonials = Testimonial.objects.filter(is_featured=True)[:6]
        recent_properties = Property.objects.filter(is_published=True).order_by('-created_at')[:6]

        context = {
            'search_form': search_form,
            'featured_properties': featured_properties,
            'recent_properties': recent_properties,
            'locations': locations,
            'categories': categories,
            'testimonials': testimonials,
            'stats': {
                'properties_count': Property.objects.filter(is_published=True).count(),
                'locations_count': Location.objects.count(),
                'satisfied_clients': '1,200+',
                'portfolio_value': '₦150B+'
            }
        }
        return render(request, self.template_name, context)


class AboutView(View):
    template_name = 'core/about.html'

    def get(self, request):
        return render(request, self.template_name, {
            'testimonials': Testimonial.objects.filter(is_featured=True)[:4]
        })


class LegalPageView(View):
    template_name = 'core/legal_page.html'

    def get(self, request, slug):
        page = get_object_or_404(LegalPage, slug=slug)
        return render(request, self.template_name, {'page': page})


def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)


def custom_500_view(request):
    return render(request, '500.html', status=500)
