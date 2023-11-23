# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PokeItem(scrapy.Item):
    name  = scrapy.Field()
    prix = scrapy.Field() 
    description = scrapy.Field()
    url = scrapy.Field()
    stock  = scrapy.Field()
    categories = scrapy.Field()
    tags = scrapy.Field() 
    sku = scrapy.Field()
    poids = scrapy.Field()
    longueur = scrapy.Field() 
    largeur = scrapy.Field()
    hauteur = scrapy.Field()
    
