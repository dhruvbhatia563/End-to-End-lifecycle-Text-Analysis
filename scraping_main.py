import numpy as np
import scrapy
import selenium
import time
import pandas as pd
import csv

from tqdm import tqdm
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

s=Service('C:/Users/HP/PycharmProjects/pythonProject/movie_reviews_selenium/chromedriver.exe')
driver = webdriver.Chrome(options=options,service=s)
url = 'https://www.imdb.com/title/tt6723592/reviews?ref_=tt_ov_rt' # tenet movie reviews url
driver.get(url)

print(driver.title)

response = Selector(text=driver.page_source) #HTML code of the page to Scrapy Selector
total_reviews = response.css('.lister .header span::text') #will have multiple Selectors of the given css
total_reviews = total_reviews.extract_first()
#print(total_reviews) #output: 5,512 Reviews
# as now need only number will split the string and will remove the ','
total_reviews = total_reviews.replace(',','').split(' ')[0] #extract only 5512
print(total_reviews)
print(type(total_reviews)) #extracted number is in string format

# before loading the next page the current page of URL has only 25 reviews therefore:

number_of_clicks = int(int(total_reviews)/1)

error_url_list=[]
error_msg_list=[]

reviewer_list = []
url_review = []
date = []
reviewer_rating = []
review_title_list = []
movie_review = []

for i in tqdm(range(number_of_clicks)):
    try:
        css_selector = 'load-more-trigger'
        driver.find_element(By.ID, css_selector).click()
    except:
        pass


containers_reviews = driver.find_elements(By.CSS_SELECTOR, 'div.review-container')

for each_container in tqdm(containers_reviews):
    try:
        sel2 = Selector(text=each_container.get_attribute('innerHTML'))
        try:
            reviewer = sel2.css('.display-name-link a::text').extract_first().strip()

        except:
            reviewer = np.NaN

        try:
            review_url = sel2.css('a.title::attr(href)').get()
            review_url = 'https://www.imdb.com' + review_url

        except:
            review_url= np.NaN

        try:
            review_date = sel2.css('.review-date::text').extract_first().strip()

        except:
            review_date = np.NaN

        try:
            rating = sel2.css('.rating-other-user-rating span::text').extract_first().strip()

        except:
            rating=np.NaN

        try:
            review_title = sel2.css('a.title::text').extract_first().strip()

        except:
            review_title = np.NaN

        #try:
            #review = sel2.css('.text.show-more__control::text').get()

        #except:
            #review=np.NaN

        reviewer_list.append(reviewer)
        url_review.append(review_url)
        date.append(review_date)
        reviewer_rating.append(rating)
        review_title_list.append(review_title)
        #movie_review.append(review)

    except Exception as e:
        error_url_list.append(url)
        error_msg_list.append(e)

df = pd.DataFrame({
    'author':reviewer_list,
    'url':url_review,
    'date':date,
    'rating':reviewer_rating,
    'review':review_title_list})
    #'review':movie_review

df.to_csv('tenet_movie_reviews.csv')

driver.quit()




