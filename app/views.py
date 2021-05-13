from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    counter_click.update([request.GET.get('from-landing')])
    return render(request, 'index.html')


def landing(request):
    template = 'landing.html'
    if request.GET.get('ab-test-arg') == 'test':
        template = 'landing_alternate.html'
    counter_show.update([request.GET.get('ab-test-arg')])
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    return render(request, template)


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    test_stat = 0
    original_stat = 0
    try:
        test_stat = counter_show['test'] / counter_click['test']
    except ZeroDivisionError:
        pass

    try:
        original_stat = counter_show['original'] / counter_click['original']
    except ZeroDivisionError:
        pass
    return render(request, 'stats.html', context={
        'test_conversion': test_stat,
        'original_conversion': original_stat,
    })
