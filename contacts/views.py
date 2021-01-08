from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail

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
        realtor_email = request.POST.get('realtor_email')

        # check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.filter(
                listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(
                    request, 'You have already made an inquiry for this listing')
                return redirect(reverse('listings:listing', kwargs={
                    'listing_id': listing_id
                }))

        contact = Contact(
            listing=listing,
            name=name,
            email=email,
            phone=phone,
            listing_id=listing_id,
            message=message,
            user_id=user_id)

        contact.save()

        # Send email
        send_mail(
            'Property Listing Inquiry',
            f'There has been an inquiry for {listing}. Sign into the admin panel for more information.',
            'arik4test@gmail.com',
            [realtor_email, 'arik4test@gmail.com'],
            fail_silently=False

        )

        messages.success(
            request, 'Your request has been submitted, a realtor will get back to you soon.')
        return redirect(reverse('listings:listing', kwargs={
            'listing_id': listing_id
        }))
