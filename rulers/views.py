from django.shortcuts import render
from rulers.models import Monarch, Capital

# Create your views here.
def home(request):
    monarch_by_year_result = None
    monarch_by_name_results = []
    family_by_name_results = []
    add_monarch_result = None
    capital_by_year_result = None

    if 'find_monarch_by_year' in request.GET:
        year = request.GET.get('year')
        try:
            year = int(year)
            monarch = Monarch.objects.filter(start_year__lte=year, end_year__gte=year).first()
            if monarch:
                capital_name = monarch.capital.name if monarch.capital else 'неизвестна столица'
                monarch_by_year_result = f'Владетелят от {monarch.start_year} до {monarch.end_year} бил {monarch.name} {monarch.family if monarch.family else ''}. Управлявал от {capital_name}.'
            else:
                monarch_by_year_result = 'България не е имала владетел през този период.'
        except (ValueError, TypeError):
            monarch_by_year_result = 'Моля, въведи правилна година.'

    elif 'find_monarch_by_name' in request.GET:
        name = request.GET.get('name')
        monarchs = Monarch.objects.filter(name__icontains=name)
        if monarchs.exists():
            monarch_by_name_results = [
                f'През {monarch.start_year} до {monarch.end_year} управлянал {monarch.name} {monarch.family if monarch.family else ''}. Управлявал от {monarch.capital.name if monarch.capital else 'неизвестна столиза'}.'
                for monarch in monarchs
            ]
        else:
            monarch_by_name_results = ['България не е имала владетел през този период']

    elif 'find_capital_by_year' in request.GET:
        year = request.GET.get('year')
        try:
            year = int(year)
            capital = Capital.objects.filter(start_year__lte=year, end_year__gte=year).first()
            if capital:
                capital_by_year_result = f'През {capital.start_year} до {capital.end_year} България е управлявана от {capital.name}.'
            else:
                capital_by_year_result = f'Няма известна столица през тази година.'
        except (ValueError, TypeError):
            capital_by_year_result = 'Моля, въведи правилна година.'

    elif 'add_monarch' in request.POST:
        name = request.POST.get('name')
        family = request.POST.get('family')
        start_year = request.POST.get('start_year')
        end_year = request.POST.get('end_year')
        try:
            start_year = int(start_year)
            end_year = int(end_year)
            if Monarch.objects.filter(start_year=start_year, end_year=end_year).exists():
                add_monarch_result = f'Вече съществува владетел за този период.'
            else:
                capital = Capital.objects.filter(start_year__lte=start_year, end_year__gte=end_year).first()
                if not capital:
                    add_monarch_result = 'Няма съответна столица през този период.'
                else:
                    monarch = Monarch.objects.create(name=name, family=family, start_year=start_year, end_year=end_year, capital=capital)
                    add_monarch_result = f'Владетелят {name} {family} е добавен за периода {start_year}-{end_year}. Със столица на царуване {capital.name}.'
        except ValueError:
            add_monarch_result = 'Моля, въведи правилна година.'

    context = {
        'monarch_by_year_result': monarch_by_year_result,
        'monarch_by_name_results': monarch_by_name_results,
        'family_by_name_results': family_by_name_results,
        'add_monarch_result': add_monarch_result,
        'capital_by_year_result': capital_by_year_result,
    }
    return render(request, 'home.html', context)