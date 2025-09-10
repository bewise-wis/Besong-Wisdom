# feeds.py
from django.contrib.syndication.views import Feed
from .models import BlogPost

class LatestPostsFeed(Feed):
    title = "Your Portfolio Blog"
    link = "/blog/"
    description = "Latest blog posts from my portfolio"
    
    def items(self):
        return BlogPost.objects.filter(published=True).order_by('-created_at')[:10]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.excerpt