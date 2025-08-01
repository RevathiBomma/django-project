import feedparser
from django.shortcuts import render, redirect
from django.http import HttpResponse
from news.models import Headline

def scrape(request, name):
    Headline.objects.all().delete()

    RSS_FEEDS = {
    'politics': 'https://www.theguardian.com/politics/rss',
    'sports': 'https://www.theguardian.com/sport/rss',
    'entertainment': 'https://www.theguardian.com/culture/rss',
    'opinion': 'https://www.theguardian.com/commentisfree/rss',
    'breaking-news': 'https://www.theguardian.com/world/rss',
    'latest': 'https://www.theguardian.com/international/rss',
}



    rss_url = RSS_FEEDS.get(name)
    if not rss_url:
        return HttpResponse("Invalid category.", status=400)

    feed = feedparser.parse(rss_url)

    if not feed.entries:
        return HttpResponse("No news found for this category.", status=404)

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        media_content = entry.get("media_content", [])
        image = media_content[0]['url'] if media_content else ""

        Headline.objects.create(
            title=title,
            url=link,
            image=image
        )

    return redirect("news_list")
def news_list(request):
    headlines = Headline.objects.all().order_by('-id')
    return render(request, "news/home.html", {"object_list": headlines})
