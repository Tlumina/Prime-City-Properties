from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import ContactForm


class ContactView(View):
    template_name = 'contact/contact.html'

    def get(self, request):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for contacting Prime City Properties. Your message has been received and an advisor will respond shortly.")
            return redirect('contact:index')
        
        return render(request, self.template_name, {'form': form})
