def harmon(request):
    from .models import Harmonogram, Anime_list
    """
    harmon_html = Harmonogram.objects.all()
    key = []
    for ff in harmon_html:
        g = Anime_list.objects.filter(id_anime=ff.id_anime)[0]
        ff.title= g.title
        ff.web_name = g.web_name
        key.append(ff)
    """

    day_nm = ["Poniedziałek","Wtorek","Środa","Czwartek","Piątek","Sobota","Niedziela"]

    harmon_html = Harmonogram.objects.all().order_by('day')
    for ff in harmon_html:
        ff.day = day_nm[ff.day-1]

    return {
        'harmon': harmon_html,
    }