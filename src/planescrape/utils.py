def get_airlines(soup):
    airline = []
    airlines = soup.find_all("span", class_="codeshares-airline-names", string=True)

    for i in airlines:
        airline.append(i.text)
    return airline


def get_total_stops(soup):
    stops_list = []
    stops = soup.find_all("div", class_="section stops")

    for i in stops:
        for j in i.find_all("span", class_="stops-text"):
            stops_list.append(j.text)
    return stops_list


def get_price(soup):
    prices = []
    price = soup.find_all(
        "div", class_="Flights-Results-FlightPriceSection right-alignment sleek"
    )

    for i in price:
        for j in i.find_all("span", class_="price-text"):
            prices.append(j.text)
    return prices


def get_duration(soup):
    duration_list = []
    duration = soup.find_all("div", class_="section duration allow-multi-modal-icons")
    for i in duration:
        for j in i.find_all("div", class_="top"):
            duration_list.append(j.text)
    return duration_list
