def posts(request):
    from .models import AnimePost
    post_html = AnimePost.objects.all().order_by('-key_map__date_posted')
    return {
        'posts': post_html,
    }


def popular(request):
    from .models import AnimeSeries
    post_html = AnimeSeries.objects.all().order_by('-rating')[:10]
    return {
        'popular': post_html,
    }

def english_titles(request):
    english = request.COOKIES.get('englishTitles') == 'true'
    return {
        'english_titles': english,
    }
