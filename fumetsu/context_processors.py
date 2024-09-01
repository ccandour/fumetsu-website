
def posts(request):
    from anime.models import AnimePost
    post_html = AnimePost.objects.all().order_by('-odc_nm__date_posted')
    return {
        'posts': post_html,
    }


def popular(request):
    from .models import AnimeSeries
    post_html = AnimeSeries.objects.all().order_by('-rating')[:10]
    return {
        'popular': post_html,
    }
