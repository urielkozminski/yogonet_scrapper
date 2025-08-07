from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
import logging

chromedriver_autoinstaller.install()

def scrape_yogonet():
    """
    Realiza scraping de articulos desde la web de Yogonet.
    Retorna una lista de diccionarios con los datos obtenidos.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.yogonet.com/international/")
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        articles = []
        for module in soup.find_all("div", class_="contenedor_dato_modulo"):
            kicker_tag = module.find("div", class_="volanta")
            kicker = kicker_tag.get_text(strip=True) if kicker_tag else ""

            title_tag = module.find("h2")
            a_tag = title_tag.find("a") if title_tag else None
            title = a_tag.get_text(strip=True) if a_tag else ""
            link = a_tag.get("href") if a_tag else ""

            image_tag = module.find("div", class_="imagen")
            img = image_tag.find("img") if image_tag else None
            image_url = img.get("src") if img else ""

            articles.append({
                "kicker": kicker,
                "title": title,
                "link": link,
                "image": image_url,
            })

        return articles

    except WebDriverException as e:
        logging.error(f"Error con Selenium WebDriver: {e}", exc_info=True)
        return []

    finally:
        if driver:
            driver.quit()