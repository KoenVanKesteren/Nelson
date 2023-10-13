"""


    Opmerkingen bij Opslaan data:

        - ik ben een fan losse koppeling ...
            ... dus ik heb ervoor gekozen om iets van een generieke interface voor dataservices op te zetten, ...
            ... maar die is omwille van tijd wel wat specifiek voor sqlite geworden

        - mbt type database zou ik bij grotere applicaties eerder voor een structured model gaan.
            - No-SQL vervult naar mijn idee vooral een rol bij het aanbieden van data voor specifieke toepassingen

        - veel kolommen hebben hier overigens nog niet het juiste data type

    Opmerkingen bij uitlezen database:

        - ik heb hier geen gebruik gemaakt van de ingebouwde generator functionaliteit van sqlite, ...
			... ik vind het fijner om kleine batches op te halen ...
			... en dan lijken me de voordelen van een generator niet vanzelfsprekend.

"""

from data_service import sqlite_service


def connect(service=sqlite_service.SqliteService({})):
    service.connect()

    return service


def close(service):
    service.close_connection()


def store_product_listing_data(data, service=sqlite_service.SqliteService({})):
    service.connect()

    # create table if it doesn't exist
    create_product_listing_entity(service)

    # insert data
    for item in data:
        service.create_item("product_listing", item)

    service.close_connection()


def store_product_detail_data(data, service=sqlite_service.SqliteService({})):
    service.connect()

    # create table if it doesn't exist
    create_product_detail_entity(service)

    # insert data
    for item in data:
        service.create_item("product_detail", item)

    service.close_connection()


def store_listing_info_item(item, service):
    service.create_item("listing_info", item)


def create_product_listing_entity(service):
    service.create_entity(
        "product_listing",
        [
            {"name": "page_type", "type": "TEXT"},
            {"name": "page_url", "type": "TEXT"},
            {"name": "page_number", "type": "INTEGER"},
            {"name": "crawled_at", "type": "TEXT"},
            {"name": "product_category", "type": "TEXT"},
            {"name": "ordering", "type": "TEXT"},
            {"name": "body", "type": "TEXT"},
            {"name": "parsed_at", "type": "TEXT"},
            {"name": "status", "type": "TEXT"},
            {"name": "attempts", "type": "INTEGER"},
        ]
    )


def create_product_detail_entity(service):
    service.create_entity(
        "product_detail",
        [
            {"name": "page_type", "type": "TEXT"},
            {"name": "page_url", "type": "TEXT"},
            {"name": "crawled_at", "type": "TEXT"},
            {"name": "body", "type": "TEXT"},
            {"name": "parsed_at", "type": "TEXT"},
            {"name": "status", "type": "TEXT"},
            {"name": "attempts", "type": "INTEGER"},
        ]
    )


def create_listing_info_entity(service):
    service.create_entity(
        "listing_info",
        [
            {"name": "brand_name", "type": "TEXT"},
            {"name": "product_name", "type": "TEXT"},
            {"name": "price", "type": "REAL"},
            {"name": "currency", "type": "TEXT"},
            {"name": "product_category", "type": "TEXT"},
        ]
    )


def get_product_listing_data(parsed: str, batch_size=5, service=sqlite_service.SqliteService({})) -> list:
    service.connect()

    if parsed == "N":
        result = service.list("product_listing", where="parsed_at IS NULL", limit=batch_size)
    elif parsed == "Y":
        result = service.list("product_listing", where="parsed_at IS NOT NULL", limit=batch_size)
    else:
        result = service.list("product_listing", limit=batch_size)

    service.close_connection()

    return result


def get_product_detail_data(parsed: str, batch_size=5, service=sqlite_service.SqliteService({})) -> list:
    service.connect()

    if parsed == "N":
        result = service.list("product_detail", where="parsed_at IS NULL", limit=batch_size)
    elif parsed == "Y":
        result = service.list("product_detail", where="parsed_at IS NOT NULL", limit=batch_size)
    else:
        result = service.list("product_detail", limit=batch_size)

    service.close_connection()

    return result


def get_listing_info_data(service=sqlite_service.SqliteService({})) -> list:
    service.connect()

    result = service.list("listing_info")

    service.close_connection()

    return result

