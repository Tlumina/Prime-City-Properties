from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Property, Location, PropertyType, PropertyFeature, PropertyImage
from .forms import PropertySearchFilterForm, PropertyCreateForm
from tours.forms import TourBookingForm


class PropertyListView(ListView):
    model = Property
    template_name = 'properties/listing_list.html'
    context_object_name = 'properties'
    paginate_by = 9

    def get_queryset(self):
        queryset = Property.objects.filter(is_published=True).select_related('location', 'property_type').prefetch_related('images', 'features')
        form = PropertySearchFilterForm(self.request.GET)

        if form.is_valid():
            location = form.cleaned_data.get('location')
            if location:
                queryset = queryset.filter(location=location)

            property_type = form.cleaned_data.get('property_type')
            if property_type:
                queryset = queryset.filter(property_type=property_type)

            status = form.cleaned_data.get('status')
            if status:
                queryset = queryset.filter(status=status)

            bedrooms = form.cleaned_data.get('bedrooms')
            if bedrooms is not None:
                queryset = queryset.filter(bedrooms__gte=bedrooms)

            bathrooms = form.cleaned_data.get('bathrooms')
            if bathrooms is not None:
                queryset = queryset.filter(bathrooms__gte=bathrooms)

            min_price = form.cleaned_data.get('min_price')
            if min_price is not None:
                queryset = queryset.filter(price__gte=min_price)

            max_price = form.cleaned_data.get('max_price')
            if max_price is not None:
                queryset = queryset.filter(price__lte=max_price)

            min_sqm = form.cleaned_data.get('min_sqm')
            if min_sqm is not None:
                queryset = queryset.filter(size_sqm__gte=min_sqm)

            if form.cleaned_data.get('has_garage'):
                queryset = queryset.filter(garage_spaces__gt=0)

            if form.cleaned_data.get('has_pool'):
                queryset = queryset.filter(has_swimming_pool=True)

            keyword = form.cleaned_data.get('keyword')
            if keyword:
                queryset = queryset.filter(
                    Q(title__icontains=keyword) |
                    Q(description__icontains=keyword) |
                    Q(address__icontains=keyword) |
                    Q(landmark_notes__icontains=keyword)
                )

            sort_by = form.cleaned_data.get('sort_by') or '-created_at'
            queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PropertySearchFilterForm(self.request.GET or None)
        context['locations'] = Location.objects.all()
        context['property_types'] = PropertyType.objects.all()
        
        # Build query string for pagination links preserving active filters
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        context['query_string'] = query_params.urlencode()
        
        context['total_count'] = self.get_queryset().count()
        return context


class PropertyDetailView(DetailView):
    model = Property
    template_name = 'properties/listing_detail.html'
    context_object_name = 'property'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Property.objects.filter(is_published=True).select_related('location', 'property_type').prefetch_related('images', 'features')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment views count safely
        Property.objects.filter(pk=obj.pk).update(views_count=obj.views_count + 1)
        obj.refresh_from_db()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prop = self.object
        context['tour_form'] = TourBookingForm(initial={'property': prop})
        context['images'] = prop.images.all()
        context['similar_properties'] = Property.objects.filter(
            is_published=True,
            location=prop.location
        ).exclude(pk=prop.pk)[:3]
        return context


class PropertyCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'properties/listing_create.html'
    login_url = '/login/'

    def test_func(self):
        return self.request.user.is_real_estate_agent or self.request.user.is_staff

    def get(self, request):
        form = PropertyCreateForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PropertyCreateForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.is_published = True
            property_obj.save()
            form.save_m2m() # Save features

            # Primary image handling (uploaded file takes precedence, fallback to URL)
            primary_file = request.FILES.get('primary_image')
            img_url = form.cleaned_data.get('primary_image_url')
            
            has_primary = False
            if primary_file:
                PropertyImage.objects.create(
                    property=property_obj,
                    image=primary_file,
                    caption=property_obj.title,
                    is_primary=True,
                    display_order=0
                )
                has_primary = True
            elif img_url:
                PropertyImage.objects.create(
                    property=property_obj,
                    image_url=img_url,
                    caption=property_obj.title,
                    is_primary=True,
                    display_order=0
                )
                has_primary = True

            # Additional gallery images handling
            gallery_files = request.FILES.getlist('gallery_images')
            for index, g_file in enumerate(gallery_files, start=1):
                is_first_as_primary = (not has_primary and index == 1)
                PropertyImage.objects.create(
                    property=property_obj,
                    image=g_file,
                    caption=f"{property_obj.title} - View {index}",
                    is_primary=is_first_as_primary,
                    display_order=index
                )

            messages.success(request, f"Property '{property_obj.title}' successfully published!")
            return redirect(property_obj.get_absolute_url())

        return render(request, self.template_name, {'form': form})
