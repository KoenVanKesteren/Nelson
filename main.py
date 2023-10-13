
import html
import auth
from flask import Flask, make_response
import data_manager
import data_parser
import json


app = Flask(__name__)


@app.route("/store-data")
def store_data():
    """
    Opmerkingen bij opslaan data:

        - voor nu een simpele versie
        - ipv gelijk parsen vanuit de file vind ik het mooier om de data eerst in een database te zetten ...
            ... zodat je die gecontroleerd kan verwerken

        - zou normaal mooier zijn om geautomatiseerd te doen:

            - downloaden mbv urllib

                url =  'http://dump.dataplatform.shoes/20160530_nelson_mini_project_crawls.tar.gz'
                urllib.request.urlretrieve(url,'download.tar.gz')

            - en vervolgens uitlezen met de tarfile library

                file_name = '20160530_nelson_mini_project_crawls.tar.gz'
                tar = tarfile.open(file_name, "r:gz")
                tar.extractall()
                tar.close()

        - als dit een geautomatiseerd proces zou moeten zijn ...
            ... dan lijkt het me mooier om hier een queue voor te maken die de pagina's in batches van x stuks uitleest

    """
    data_file = "crawl_ziengs.nl_2016-05-30T23-15-20.jl"
    batch_size = 100
    product_listing_data = []
    product_detail_data = []

    with open(data_file, "r") as file:
        for _ in range(batch_size):
            json_data = file.readline()
            item = json.loads(json_data)
            item['body'] = html.escape(item['body'])

            if item["page_type"] == "product_listing":
                print("store listing page")
                item['product_category'] = ','.join(item['product_category'])
                product_listing_data.append(item)
            elif item["page_type"] == "product_detail":
                print("store detail page")
                product_detail_data.append(item)

    data_manager.store_product_listing_data(product_listing_data)
    data_manager.store_product_detail_data(product_detail_data)

    response = make_response(
        'Data stored successfully!',
        200
    )
    response.headers['Content-Type'] = "application/json"
    return response


@app.route("/parse-product-listing-data")
def parse_product_listing_data():
    # Fetch unparsed data
    unparsed_pages = data_manager.get_product_listing_data(parsed="N", batch_size=5)

    service = data_manager.connect()
    # Create table if it doesn't exist
    data_manager.create_listing_info_entity(service)

    for page in unparsed_pages:
        page['body'] = html.unescape(page['body'])
        try:
            # Extract relevant information
            extracted_info = data_parser.extract_zieng_product_listing(page['body'])
        except:
            print("something went wrong")
        else:
            # Store extracted info
            for item in extracted_info:
                item['product_category'] = page['product_category']
                data_manager.store_listing_info_item(item, service)
        finally:
            # Update product_listing with new status, attempts
            # TODO: data_manager.update_product_listing()
            pass

    data_manager.close(service)

    response = make_response(
        'Data parsed successfully!',
        200
    )
    response.headers['Content-Type'] = "application/json"
    return response


@app.route("/parse-product-detail-data")
def parse_product_detail_data():
    unparsed_pages = data_manager.get_product_detail_data(parsed="N", batch_size=5)

    for page in unparsed_pages:
        # todo: detail data parsen
        pass

    response = make_response(
        'Data parsed successfully!',
        200
    )
    response.headers['Content-Type'] = "application/json"
    return response


def link_product_info():
    """

    opmerkingen mbt linken van data:

        - ondanks dat het me niet gelukt is om bruikbare detail data te vinden ...
            ... zou ik de volgende aanpak hanteren als ik meer tijd zou hebben:

            - listing data parsen naar losse producten en opslaan met uniek id
            - detail data parsen en opslaan met uniek id
            - vervolgens door alle losse producten van de geparste listing data heenloopen
                - per product zoeken in de geparste detail data obv merk, type, (eventueel kleur etc)
                - indien er een match is:
                    - de id's geparste product detail tabel toevoegen aan de geparste product listing tabel


        - indexeren data

                ik zou een sql database gebruiken ipv noSQL:

                    - sql biedt mi. meer flexibiliteit mbt het zoeken op specifieke velden
                        bijvoorbeeld zoeken op categorie, kleur etc kan nu via een koppeltabel ...
                        ... ipv zoeken in grote stukken tekst


                    - noSQl zie ik dus meer als een optimalisatie slag voor specifieke doeleinden
                        ... die kan dan indien nodig (bijvoorbeeld tbv scaling) tegen de sql database aangebouwd worden
    """

    # TODO

    pass


@app.route("/get-product-info/<int:id>")
@auth.authenticate_user('gebruiker1', 'wachtwoord1')
def get_product_info(id):
    """
        opmerkingen mbt aanbieden van data aan gebruikers:

            - ben ik helaas nog niet aan toegekomen

            - Hier moet uiteraard gedacht worden aan de standaard zaken als:
                - authenticatie van gebruiker
                    - beschikt deze naast de juiste credentials ook over de juiste permissies voor de specifieke data

                - indien nodig ook rekening houden met data validatie om bijvoorbeeld sql injection te voorkomen
    """

    # TODO

    response = make_response(
        'Here is your data',
        200
    )
    response.headers['Content-Type'] = "application/json"
    return response


@app.route("/get-product-info-by-category/<string:category>")
@auth.authenticate_user('gebruiker2', 'wachtwoord2')
def get_product_info_by_category(category):

    # TODO

    response = make_response(
        'Here is your data',
        200
    )
    response.headers['Content-Type'] = "application/json"
    return response


if __name__ == "__main__":
    app.run(debug=True)