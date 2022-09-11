# fil.xml

import os
from datetime import datetime as dt

from dateutil.tz import gettz

from bs4 import BeautifulSoup

from feedgen.feed import FeedGenerator

# où se trouvent les fichiers du site concerné
path_to_website = "site-internet/"

# création d'un fil
fg = FeedGenerator()

# https://feedgen.kiesow.be/ext/api.ext.base.html
# dans la documentation:
# "Basic FeedGenerator extension which does nothing but provides all necessary methods."
fg.load_extension('base')

# l'identifiant unique du site répertorié par le fil - pour ATOM seulement
fg.id('https://www.eviau.net/mtlpy-feedgen/site-internet')

# le titre et sous-titre du site
fg.title('un blogue minimaliste')
fg.subtitle("RSS/Atom - eviau - pour mtlpy")

# informations sur l'auteur.rice
fg.author({'name': 'eviau', 'email': 'info@eviau.net'})

fg.link(href="https://www.eviau.net/mtlpy-feedgen/site-internet", rel="self")

# la langue du fil
fg.language("fr")

# on déambule dans le répertoire `path_to_website`
# pour créer une entrée par page HTML trouvée.
for root, subFolders, files in os.walk(path_to_website):
    # comme on a pas de subFolders, on peut lire les fichiers
    # directement
    for f in files:
    	# on veut juste les billets, pas la page `index.html`
        if f != "index.html":
            path_to_html = path_to_website + f
            with open('./' + path_to_html) as html_text:
                soup = BeautifulSoup(html_text, 'html.parser')
                title = soup.title.string

            fe = fg.add_entry()
            fe.id("https://www.eviau.net/mtlpy-feedgen/" + path_to_html)
            fe.title(title)
            fe.link(href="https://www.eviau.net/mtlpy-feedgen/" + path_to_html)
            fe.updated(dt.fromtimestamp(os.path.getmtime(
                path_to_html), tz=gettz("America/New York")))

fg.atom_file('fil-atom.xml')
fg.rss_file('fil-rss.xml')

