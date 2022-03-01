from typing import List

from area import Area
from data import parse_csv_lines
from services import get_countries_from_github, upload_to_github


def main():
    countries: dict = get_countries_from_github(
        "https://raw.githubusercontent.com/MatisseBE/VATSIMareas/main/Countries.txt")
    with open("areas.csv", "r") as file:
        text: str = file.read()
        areas: List[Area] = parse_csv_lines(text)

    for country in countries:
        this_country_areas: str = ""
        for area in areas:
            if countries[country]["Code"] == area.country_ident:
                this_country_areas += str(area) + "\n"

        upload_to_github(this_country_areas, f"Datafiles/{country}.txt")


if __name__ == '__main__':
    main()
