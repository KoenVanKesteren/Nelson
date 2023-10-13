"""
    opmerkingen:

        - bij de detail pagina's van ziengs kreeg ik alleen foute pagina's binnen.
            - Er zullen er ook goeie bij gezeten hebben maar die kon ik zo snel niet vinden,
            - de eerste 1000 waren in ieder geval pagina's met een foutmelding

        - ik zou hier in ieder geval de volgende methode hanteren als ik meer tijd had:

            - Als je veel verschillende soorten pagina's hebt die ook constant veranderen van structuur ...
                ... dan wil je niet iedere keer je scripts aanpassen
                ... maar dan wordt het zinvol om gebruik te maken van meer generieke functionaliteit voor parsen

                - als je kennis hebt over de locatie van alle informatie ...
                    ...zou je daar paden van kunnen maken per type data:

                    - soms zal bijvoorbeeld een enkele class name volstaan om de juist info te vinden
                    ... maar indien je gebruik moet maken van geneste nodes dan kunnen die toegevoegd worden

                    bijvoorbeeld zoiets:

                        ziengs_config = {
                            product: {
                                path: 			[ { class: 'content' }, ],
                                attributes:		[
                                    price: {
                                        path: 			[
                                                            { elem: 'span', class: 'price', index: -1 },
                                                            { elem: 'span', class: 'main' }
                                                        ],
                                    }
                                ]
                            }
                        }

                - vervolgens kan je dan de ongeparste data en de bijbehorende configuratie ...
                    ... aan een generieke parse functie meegeven
                - zou nog ff wat beter uitgewerkt moeten worden maar dan krijg je zoiets

                    def parse_page( unparsed_data, config ):

                        # loop through config

                            # for each key: get the path

                                # for each path node we can use a recursive function to search for nested nodes

                                # return the found node

                            # if there are attributes:
                            # we can use a recursive function ...
                            # ...to pass the raw html of the parent and the path for attributes


    - Als er veel verschillende pagina's zijn die constant verander van structuur ...
        ... dan zal je die waarschijnlijk geautomatiseerd willen analyseren

    - verschillende methodes om data te analyseren

        - obv voorkennis:

            - zoeken op specifieke brand namen
            - product namen
            - zoeken op bekende manieren waarop prijzen staan vermeld
                - op symbool van bekende currencies
                - getallen na woorden als: prijs, price, ...
            - ...

        - mbv LLM

            - ChatGpt:
                - voordeel: werkt met api
                - nadeel: wordt bijzonder duur bij grote hoeveelheden
                - data voorbewerken zodat je de api gerichter kan bevragen


            - Llama 2:

                - voordeel: kan je lokaal installeren en bevragen
                - nadelen: minder goed dan ChatGpt, meer werk


"""
from bs4 import BeautifulSoup
import json


def extract_zieng_product_listing(page):

    product_data = []

    soup = BeautifulSoup(page, 'html.parser')

    tags = soup.select(selector=".content")

    for tag in tags:

        product_info = {}

        titles = tag.findChildren('a', attrs={"class": "title"})

        # get the product name
        product_info['product_name'] = titles[0].getText()

        # get the price
        prices = tag.findChildren('span', attrs={"class": "price"})
        last_price = prices[-1]

        value_main = last_price.findChildren('span', attrs={"class": "main"})[0]
        value_cents = last_price.findChildren('span', attrs={"class": "cents"})[0]
        product_info['price'] = float("{0}.{1}".format(value_main.getText().strip(), value_cents.getText().strip()))
        product_info['currency'] = last_price.findChildren('span', attrs={"class": "valuta"})[0].getText()

        product_data.append(product_info)

    return product_data