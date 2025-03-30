from django.contrib.sitemaps import Sitemap
from store.models import Product


class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Product.objects.filter(is_available=True)

    def lastmod(self, obj: Product):
        return obj.modified_date
