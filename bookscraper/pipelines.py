# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class BookscraperPipeline:

    def __init__(self):

        ## Create/Connect to database
        self.con = sqlite3.connect('newpokemon.db')

        ## Create cursor, used to execute commands
        self.cur = self.con.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS pokemon(
            name TEXT,
            prix FLOAT,
            description TEXT,
            url TEXT,
            stock INTEGER,
            categories TEXT,
            tags TEXT,
            sku INTEGER,
            poids FLOAT,
            longueur INTEGER,
            largeur INTEGER,
            hauteur INTEGER      
                         
        )
        """)

    def process_item(self, item, spider):

        adapter = ItemAdapter(item)
        print(adapter)

        #nettoyer le champ stock et le mettre en int
        value_stock = adapter.get('stock')
        value_stock = value_stock.replace(' in stock','') 
        adapter['stock'] = int(value_stock)

        value_poids = adapter.get('poids')
        value_poids = value_poids.replace(' kg','') 
        adapter['poids'] = float(value_poids)

        #mettre en minuscule
        lowercase_keys = ['categories','tags']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        #convertir les string en nombre
        int_keys = ['sku','longueur', 'largeur', 'hauteur']
        for int_key in int_keys:
            value = adapter.get(int_key)
            if value is not None:
                adapter[int_key] = int(value)

        #prix converti de string en float
        value_prix = adapter.get('prix')
        adapter['prix'] = float(value_prix)

         ## Define insert statement
        self.cur.execute("""
            INSERT INTO pokemon (name, prix, description, url, stock, categories, tags, sku, poids,
                         longueur, largeur, hauteur) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            adapter['name'],
            adapter['prix'],
            adapter['description'],
            adapter['url'],
            adapter['stock'],
            adapter['categories'],
            adapter['tags'],
            adapter['sku'],
            adapter['poids'],
            adapter['longueur'],
            adapter['largeur'],
            adapter['hauteur']
        ))

        ## Execute insert of data into database
        self.con.commit()

        return item
