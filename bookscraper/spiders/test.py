#code pour scraper uniquement une page
# import scrapy


# class PokespiderSpider(scrapy.Spider):
#     name = "pokespider"
#     allowed_domains = ["scrapeme.live"]
#     start_urls = ["https://scrapeme.live/shop"]

#     def parse(self, response):
#         pokemons = response.css('li.product')
        

#         for pokemon in pokemons:
         
#             yield{
#                 'name' : pokemon.css('h2.woocommerce-loop-product__title::text').get(),
#                 'prix' : pokemon.css('span.amount::text').get(),
#                 #'url' : pokemon.css('li.product a').attrib['href'],
#             }


#         #prendre toutes les autres pages

#         current_page_number = response.url.split("/")[-2]  #récupère le numéro de la page actuelle de l'URL
#         if current_page_number.isdigit():  # Vérifie si le numéro de page est un nombre
#             next_page_number = int(current_page_number) + 1
#             next_page = f"https://scrapeme.live/shop/page/{next_page_number}/"
#             yield scrapy.Request(next_page, callback=self.parse)
#         else:  # Si on est sur la première page, où il n'y a pas de numéro de page dans l'URL
#             next_page = "https://scrapeme.live/shop/page/2/"
#             yield scrapy.Request(next_page, callback=self.parse)
