from django.db.models.query import ValuesListIterable
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from listings.choices import price_choices, bedroom_choices, state_choices

from .models import Listing


def index(request):
    listings = Listing.objects.order_by('list_date').filter(is_published=True)
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings,
    }
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    context = {
        'listing': listing,
    }
    return render(request, 'listings/listing.html', context)


def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET.get('keywords')
        if keywords:
            queryset_list = queryset_list.filter(
                description__icontains=keywords)

        # city
        if 'city' in request.GET:
            city = request.GET.get('city')
            if city:
                queryset_list = queryset_list.filter(city__iexact=city)

        # state
        if 'state' in request.GET:
            state = request.GET.get('state')
            if state:
                queryset_list = queryset_list.filter(state__iexact=state)

        # bedrooms
        if 'bedrooms' in request.GET:
            bedrooms = request.GET.get('bedrooms')
            if bedrooms:
                queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

        # price
        if 'price' in request.GET:
            price = request.GET.get('price')
            if price:
                queryset_list = queryset_list.filter(price__lte=price)

    paginator = Paginator(queryset_list, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': Listing.objects.order_by('-list_date'),

    }

    if 'clear' not in request.GET:
        context['values'] = request.GET
        context['listings'] = paged_listings

    return render(request, 'listings/search.html', context)
