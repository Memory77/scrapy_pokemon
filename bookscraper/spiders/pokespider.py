import scrapy
import re
from bookscraper.items import PokeItem


class PokespiderSpider(scrapy.Spider):
    name = "pokespider"
    allowed_domains = ["scrapeme.live"]
    start_urls = ["https://scrapeme.live/shop"]


    #fonction doit s'occuper de parcourir la liste des produits sur chaque page et de suivre le lien de chaque produit
    #pour obtenir plus de détails.
    def parse(self, response):
        pokemons = response.css('li.product')
        for pokemon in pokemons: #on parcours chaque pokemon un pokemon = li.product
            name = pokemon.css('h2.woocommerce-loop-product__title::text').get()
            pokemon_url = pokemon.css('a::attr(href)').get() #on prend le href a chaque pokemon
            yield response.follow(pokemon_url, self.parse_product, meta = {'name': name})

        #Pagination
        next_page = response.css('.page-numbers a.next::attr(href)').get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)


    #fonction est appelée pour chaque page de produit. 
    #elle extrait et enregistre les détails tels que le nom, le prix, la description, et l'URL.
    def parse_product(self, response):
        name = response.meta.get('name')
        dimension = response.css('td.product_dimensions::text').get()
        longueur = largeur = hauteur = None
        if dimension: 
            #regex pour prendre les differentes dimensions sur le string 6x6x6
            pattern = r"(\d) x (\d) x (\d)"
            match = re.search(pattern, dimension)
            if match:
                longueur = match.group(1)
                largeur = match.group(2)
                hauteur = match.group(3)
            else:
                print('rien trouvé')
        else:
            print('rien trouvé')

        
        poke_item = PokeItem()

        
        poke_item['name'] = name
        poke_item['prix'] = response.css('p.price span.woocommerce-Price-amount::text').get()
        poke_item['description'] = response.css('div.woocommerce-product-details__short-description p::text').get()
        poke_item['url'] = response.url
        poke_item['stock'] = response.css('p.stock::text').get()
        poke_item['categories'] = response.css('span.posted_in a::text').get()
        poke_item['tags'] = response.css('span.tagged_as a::text').get()
        poke_item['sku'] = response.css('span.sku::text').get()
        poke_item['poids'] = response.css('td.product_weight::text').get()
        poke_item['longueur'] = longueur
        poke_item['largeur'] = largeur
        poke_item['hauteur'] = hauteur
    

        yield poke_item