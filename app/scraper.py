from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
from utils.ai_helper import AIPredictor
import chromedriver_autoinstaller
import logging

chromedriver_autoinstaller.install()

def scrape_yogonet():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = None
    predictor = AIPredictor()

    try:
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.yogonet.com/international/")
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        articles = []
        for module in soup.find_all("div", recursive=True):
            article_data = {"title": "", "kicker": "", "link": "", "image": ""}

            for tag in module.find_all(["a", "p", "h2", "div", "span"], recursive=False):
                prediction = predictor.predict_element_type(tag)

                if prediction == "title" and not article_data["title"]:
                    article_data["title"] = tag.get_text(strip=True)
                elif prediction == "kicker" and not article_data["kicker"]:
                    article_data["kicker"] = tag.get_text(strip=True)
                elif prediction == "link" and not article_data["link"]:
                    article_data["link"] = tag.get("href", "")
                elif prediction == "image" and not article_data["image"]:
                    img = tag.find("img")
                    if img and img.get("src"):
                        article_data["image"] = img["src"]

            if article_data["title"]:
                articles.append(article_data)

        return articles

    except WebDriverException as e:
        logging.error(f"Error con Selenium WebDriver: {e}", exc_info=True)
        return []

    finally:
        if driver:
            driver.quit()