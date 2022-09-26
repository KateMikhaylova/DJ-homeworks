from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    'soup': {
        'мясные фрикадельки, кг': 0.2,
        'картофель, кг': 0.3,
        'кабачок, кг': 0.3,
        'помидор, шт': 0.5,
        'морковь, кг': 0.1,
        'лук, кг': 0.1,
        'болгарский перец': 0.1,
        'соль, ч.л.': 0.5
    },
}

def calculate_recipy(request, dish):
    needed_recipy = DATA.get(dish, {})
    persons = int(request.GET.get('servings', 1))
    context = {'recipe': {}}
    for name, quantity in needed_recipy.items():
        context['recipe'][name] = round(quantity * persons, 2)
    return render(request, 'calculator/index.html', context)
