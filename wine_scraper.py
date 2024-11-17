import csv
import random
from playwright.sync_api import sync_playwright, TimeoutError

def scrape_vivino(max_pages=10):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Use a random user-agent to avoid detection
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        ]
        page.set_extra_http_headers({"User-Agent": random.choice(user_agents)})

        try:
            print("Accessing Vivino website...")
            page.goto("https://www.vivino.com/explore", timeout=60000)
            page.wait_for_timeout(8000)

            # Adjusting the price range slider
            print("Adjusting the price range slider...")
            min_price_handle = page.locator("div.rc-slider-handle.rc-slider-handle-1")
            max_price_handle = page.locator("div.rc-slider-handle.rc-slider-handle-2")

            # Move the minimum price handle to 0
            min_price_handle.hover()
            page.mouse.down()
            page.mouse.move(min_price_handle.bounding_box()["x"] - 1000, min_price_handle.bounding_box()["y"])
            page.mouse.up()
            page.wait_for_timeout(2000)

            # Move the maximum price handle to 10,000+
            max_price_handle.hover()
            page.mouse.down()
            page.mouse.move(max_price_handle.bounding_box()["x"] + 1000, max_price_handle.bounding_box()["y"])
            page.mouse.up()
            page.wait_for_timeout(2000)

            print("Price range set from $0 to $10,000+")

            # Select the "Any rating" filter
            print("Selecting the 'Any rating' filter...")
            any_rating_selector = "label:has-text('Any rating')"
            page.wait_for_selector(any_rating_selector, timeout=5000)
            page.locator(any_rating_selector).click()
            page.wait_for_timeout(5000)

            print("Filter 'Any rating' selected. Extracting wines...")

            with open("wines.csv", mode="w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Wine Name", "Rating", "Current Price"])

                seen_wines = set()
                current_page = 1

                while current_page <= max_pages:
                    print(f"Scraping page {current_page}...")

                    # Locate wine cards
                    wine_containers = page.locator("div[class*='wineCard']")
                    wine_count = wine_containers.count()
                    print(f"Found {wine_count} wine entries on page {current_page}.")

                    for i in range(wine_count):
                        wine_container = wine_containers.nth(i)
                        winery_element = wine_container.locator("div.wineInfoVintage__truncate--3QAtw").first
                        if winery_element.count() == 0:
                            continue
                        winery = winery_element.inner_text().strip()

                        vintage_element = wine_container.locator("div.wineInfoVintage__vintage--VvWlU.wineInfoVintage__truncate--3QAtw")
                        vintage = vintage_element.inner_text().strip() if vintage_element.count() > 0 else ""
                        wine_name = f"{winery} {vintage}".strip()

                        if wine_name in seen_wines:
                            continue
                        seen_wines.add(wine_name)

                        rating_element = wine_container.locator("div.vivinoRating_averageValue__uDdPM")
                        rating = rating_element.inner_text().strip() if rating_element.count() > 0 else "N/A"

                        price_element = wine_container.locator("div.addToCartButton__price--qJdh4 > div:nth-child(2)")
                        current_price = price_element.inner_text().strip() if price_element.count() > 0 else "N/A"

                        print(f"Wine Name: {wine_name}, Rating: {rating}, Current Price: {current_price}")
                        writer.writerow([wine_name, rating, current_price])

                    # Check for the link to the next page
                    next_page_number = current_page + 1
                    next_page_selector = f"a[aria-label='Go to page {next_page_number}']"
                    next_page_link = page.locator(next_page_selector)

                    print(f"Checking for link to page {next_page_number}...")
                    if next_page_link.count() > 0:
                        print(f"Navigating to page {next_page_number}...")
                        next_page_link.scroll_into_view_if_needed()
                        next_page_link.click()
                        page.wait_for_timeout(8000)
                        current_page += 1
                    else:
                        print("No more pages to scrape.")
                        break

        except TimeoutError as te:
            print(f"Timeout Error: {te}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    scrape_vivino(max_pages=5)
