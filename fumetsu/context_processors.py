def harmon(request):
    from .models import Harmonogram, Anime_list
    day_nm = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]

    harmon_html = Harmonogram.objects.all().order_by('day')
    for ff in harmon_html:
        ff.day = day_nm[ff.day - 1]

    return {
        'harmon': harmon_html,
    }


def posts(request):
    from anime.models import Post
    post_html = Post.objects.all().order_by('-odc_nm__date_posted')
    return {
        'posts': post_html,
    }


def popular(request):
    from .models import Anime_list
    post_html = Anime_list.objects.all().order_by('-rating')[:10]
    return {
        'popular': post_html,
    }
