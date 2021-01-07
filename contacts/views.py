from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Contact


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST.get('listing_id')
        listing = request.POST.get('listing')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        user_id = request.POST.get('user_id')
        realtors_email = request.POST.get('realtors_email')

        contact = Contact(
            listing=listing,
            name=name,
            email=email,
            phone=phone,
            listing_id=listing_id,
            message=message,
            user_id=user_id)

        contact.save()

        messages.success(
            request, 'Your request has been submitted, a realtor will get back to you soon.')
        return redirect(reverse('listings:listing', kwargs={'listing_id': listing_id}))
