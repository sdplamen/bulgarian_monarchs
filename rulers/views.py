from django.shortcuts import render
from rulers.models import Monarch, Capital

# Create your views here.
def home(request):
    monarch_by_year_result = None
    monarch_by_name_results = []
    add_monarch_result = None
    capital_by_year_result = None

    if 'find_monarch_by_year' in request.GET:
        year = request.GET.get('year')
        try:
            year = int(year)
            monarch = Monarch.objects.filter(start_year__lte=year, end_year__gte=year).first()
            if monarch:
                capital_name = monarch.capital.name if monarch.capital else 'No capital assigned'
                monarch_by_year_result = f'The monarch in {monarch.start_year} to {monarch.end_year} was {monarch.name}. Governed from {capital_name}.'
            else:
                monarch_by_year_result = 'Bulgaria had no such monarch for this year.'
        except (ValueError, TypeError): # Added TypeError to catch cases where `year` might still be None after .get() if it's missing entirely
            monarch_by_year_result = 'Please enter a valid year.'

    elif 'find_monarch_by_name' in request.GET:
        name = request.GET.get('name')
        monarchs = Monarch.objects.filter(name__icontains=name)
        if monarchs.exists():
            monarch_by_name_results = [
                f'In {monarch.start_year} to {monarch.end_year} has governed {monarch.name}. Governed from {monarch.capital.name if monarch.capital else "No capital assigned"}.'
                for monarch in monarchs
            ]
        else:
            monarch_by_name_results = ['Bulgaria had no such monarch with this name.']

    elif 'find_capital_by_year' in request.GET:
        year = request.GET.get('year')
        try:
            year = int(year)
            capital = Capital.objects.filter(start_year__lte=year, end_year__gte=year).first()
            if capital:
                capital_by_year_result = f'In {capital.start_year} to {capital.end_year} Bulgaria was governed in {capital.name}.'
            else:
                capital_by_year_result = f'There is no capital found for this year.'
        except (ValueError, TypeError): # Added TypeError
            capital_by_year_result = 'Please enter a valid year.'

    elif 'add_monarch' in request.POST: # This block correctly uses request.POST
        name = request.POST.get('name')
        start_year = request.POST.get('start_year')
        end_year = request.POST.get('end_year')
        try:
            start_year = int(start_year)
            end_year = int(end_year)
            if Monarch.objects.filter(start_year=start_year, end_year=end_year).exists():
                add_monarch_result = f'A monarch already exists for this period.'
            else:
                capital = Capital.objects.filter(start_year__lte=start_year, end_year__gte=end_year).first()
                if not capital:
                    add_monarch_result = 'No suitable capital found for this period.'
                else:
                    monarch = Monarch.objects.create(name=name, start_year=start_year, end_year=end_year, capital=capital)
                    add_monarch_result = f'Monarch {name} added for the period {start_year}-{end_year}. Assigned to capital {capital.name}.'
        except ValueError:
            add_monarch_result = 'Please enter valid years.'

    context = {
        'monarch_by_year_result': monarch_by_year_result,
        'monarch_by_name_results': monarch_by_name_results,
        'add_monarch_result': add_monarch_result,
        'capital_by_year_result': capital_by_year_result,
    }
    return render(request, 'home.html', context)