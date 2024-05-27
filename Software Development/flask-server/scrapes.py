from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from flask_cors import CORS
import yfinance as yf
import plotly.graph_objects as grapher
import plotly.graph_objs as grapher

import json
from flask import Flask, jsonify
from flask import json
import plotly

class stock:
    """
    q represents the ticker name of the stock
    name represents the name of the stock
    """
    q: str

    def __init__(self, q: str) -> None:
        self.q = q

    def scrape(self):
        """
        Return -1 if error arises
        Otherwise return:
        [stock name (str), stock closing price (float), current stock price (float), percentage growth (float), News Titles (list[str]), News Descriptions (list[str]), Image sources (list[str]), Link sources (list[str])]
        """
        # Set up the Chrome driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        
        try:
            # Navigate to the Yahoo Finance page for the given stock symbol
            url = 'https://ca.finance.yahoo.com/quote/' + self.q
            driver.get(url)
            
            
            # Locate the element using XPath with only the data-test attribute
            stockName = '//h1[@class="D(ib) Fz(18px)"]'
            stockPrice = '//fin-streamer[@data-test="qsp-price"]'
            stockClose = '//td[@class="Ta(end) Fw(600) Lh(14px)"]'
            newsTitle = '//a[@data-wf-caas-prefetch="1"]'
            newsDescription = '//p[@class="Fz(14px) Lh(19px) Fz(13px)--sm1024 Lh(17px)--sm1024 LineClamp(2,38px) LineClamp(2,34px)--sm1024 M(0)"]'
            image_xpath = '//div[@class="Fl(start) Pos(r) Mt(2px) W(26.5%) Maw(220px)"]//img'
            link_xpath = '//a[contains(@class, "mega-item-header-link")]'

            # Scrape the data
            try:
                stockName = driver.find_element(By.XPATH, stockName)
            except:
                return -1
            
            try:
                current_stock_price = driver.find_element(By.XPATH, stockPrice)
            except:
                return -1
            
            try:
                stock_close_price = driver.find_element(By.XPATH, stockClose)
            except:
                return -1

            try:
                stock_Newstitle = driver.find_elements(By.XPATH, newsTitle)
            except:
                return -1

            try:
                stock_NewsDescription = driver.find_elements(By.XPATH, newsDescription)
            except:
                return -1
            
            try:
                image_src = driver.find_elements(By.XPATH, image_xpath)
            except:
                return -1
            
            try:
                link_elements = driver.find_elements(By.XPATH, link_xpath)
            except:
                return -1

            current_stock_price = float(current_stock_price.get_attribute('value'))
            percentage_growth = (current_stock_price - float(stock_close_price.text)) / float(stock_close_price.text)
            ret = []
            ret.append(stockName.text)
            ret.append(float(stock_close_price.text))
            ret.append(current_stock_price)
            ret.append(float(percentage_growth))
            ret.append([])
            for title in stock_Newstitle:
                ret[4].append(title.text)
            ret.append([])
            for description in stock_NewsDescription:
                ret[5].append(description.text)
            ret.append([])
            for image in image_src:
                ret[6].append(image.get_attribute('src'))
            ret.append([])
            for link in link_elements:
                ret[7].append(link.get_attribute('href'))
            return ret

        
        finally:
            # Quit the driver
            driver.quit()


    def generate_graph(self):
        nw = yf.Ticker(self.q)
        hist = nw.history(period='1mo')

        figure = grapher.Figure(data=grapher.Scatter(x=hist.index, y=hist['Close'], mode='lines'))

        # Convert the figure to JSON using to_json method
        graph_json = figure.to_json()
        return graph_json

