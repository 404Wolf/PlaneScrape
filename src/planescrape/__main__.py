from time import sleep

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm

from planescrape.utils import get_airlines, get_duration, get_price, get_total_stops


def main():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    sources = []
    destinations = []
    print("Please enter -1 when done.")
    print("-" * 10)
    while True:
        sources.append(input("From which city?\n"))
        if "-1" in sources:
            sources.pop(-1)
            break
        destinations.append(input("Where to?\n"))
        if "-1" in destinations:
            sources.pop(-1)
            destinations.pop(-1)
            break
        print("-" * 10)

    print("\nRoutes:")
    for i in range(len(sources)):
        print(f"{sources[i]} => {destinations[i]}")

    # get user input for period (start and end date)
    # start_date = np.datetime64(input('Start Date, Please use YYYY-MM-DD format only '))
    # end_date = np.datetime64(input('End Date, Please use YYYY-MM-DD format only '))
    # days = end_date - start_date
    # num_days = days.item().days

    start_date = np.datetime64("2024-08-24")
    end_date = np.datetime64("2024-08-25")
    days = end_date - start_date
    num_days = days.item().days

    for i in range(len(sources)):
        column_names = [
            "Airline",
            "Source",
            "Destination",
            "Duration",
            "Total stops",
            "Price",
            "Date",
        ]
        df = pd.DataFrame(columns=column_names)
        for j in tqdm(range(num_days + 1)):

            # close and open driver every 10 days to avoid captcha
            if j % 10 == 0:
                driver.quit()
                driver = webdriver.Chrome()

            url = f"https://www.kayak.com/flights/{sources[i]}-{destinations[i]}/{start_date+j}"
            driver.get(url)
            sleep(15)

            # click show more button to get all flights
            try:
                show_more_button = driver.find_element_by_xpath(
                    '//a[@class = "moreButton"]'
                )
            except:
                # in case a captcha appears, require input from user so that the for loop pauses and the user can continue the
                # loop after solving the captcha
                input(
                    "Please solve the captcha then enter anything here to resume scraping."
                )

            while True:
                try:
                    show_more_button.click()
                    driver.implicitly_wait(10)
                except:
                    break

            soup = BeautifulSoup(driver.page_source, "html.parser")
            airlines = get_airlines(soup)
            print(airlines)
            total_stops = get_total_stops(soup)
            prices = get_price(soup)
            print(prices)
            duration = get_duration(soup)
            new_data = pd.DataFrame(
                {
                    "Airline": airlines,
                    "Duration": duration,
                    "Total stops": total_stops,
                    "Price": prices,
                    "Date": start_date + j,
                }
            )

            # Concatenating the new data with the existing DataFrame
        df = pd.concat([df, new_data], ignore_index=True)

        # Assuming 'i' is defined somewhere in your code
        df["Source"] = sources[i]
        df["Destination"] = destinations[i]

        # Replacing newlines with empty strings
        df = df.replace("\n", "", regex=True)

        # Resetting the index

        df = df.reset_index(drop=True)

        # save data as csv file for each route
        df.to_csv(f"{sources[i]}_{destinations[i]}.csv", index=False)
        print(
            f"Succesfully saved {sources[i]} => {destinations[i]} route as {sources[i]}_{destinations[i]}.csv "
        )

    driver.quit()


if __name__ == "__main__":
    main()
