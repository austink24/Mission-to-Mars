# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager import chrome 

def scrape_all():
    # Initiate headless driver for deployment
    #from webdriver_manager import chrome 
    executable_path = {'executable_path': chrome.ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        #"weather_tweet": weather_table(browser),
        "Hemisphere": scrape_hemisphere()
        }
    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    #featured_image = img_url
    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    mars_facts = df.to_html(classes="table table-striped")
    return mars_facts



def weather_table (browser):
    # Visit the weather website
    url = 'https://mars.nasa.gov/insight/weather/'
    browser.visit(url)


    # %%
    # Parse the data
    html = browser.html
    weather_soup = soup(html, 'html.parser')


    # %%
    # Scrape the Daily Weather Report table
    weather_table = weather_soup.find('table', class_='mb_table')
    #print(weather_table.prettify())
    return weather_table

def scrape_hemisphere():

    executable_path = {'executable_path': chrome.ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)  # %%
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)


    # %%
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    image_html = browser.html
    hemi_soup = soup( image_html, 'html.parser')

    items = hemi_soup.find_all('div', class_='item')

    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    for item in items: 
    
        title = item.find('h3').text
        
        image_url = item.find('a', class_='itemLink product-item')['href']
        #print(image_url)
        browser.visit(hemispheres_main_url + image_url)

        image_html = browser.html

        hemi_soup = soup(image_html, 'html.parser')

        images_url = hemispheres_main_url + hemi_soup.find('img', class_='wide-image')['src']

        hemisphere_image_urls.append({"Title" : title, "Image_URL" : images_url})


    # %%
    # 4. Print the list that holds the dictionary of each image url and title.
    hemisphere_image_urls
    return (hemisphere_image_urls)
   

    # %%
    # 5. Quit the browser
    browser.quit()
if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

#from splinter import Browser
#from bs4 import BeautifulSoup as soup
#import pandas as pd


# %%
# Set the executable path and initialize the chrome browser in splinter
#from webdriver_manager import chrome 
def scrape_hemisphere():

    executable_path = {'executable_path': chrome.ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)



    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


    # %%
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('ul.item_list li.slide')


    # %%
    slide_elem.find("div", class_='content_title')


    # %%
    # Use the parent element to find the first `a` tag and save it as `news_title`
    news_title = slide_elem.find("div", class_='content_title').get_text()
    news_title


    # %%
    # Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    news_p


    # %%
    ### Featured Images


    # %%
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)


    # %%
    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()


    # %%
    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()


    # %%
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')


    # %%
    # Find the relative image url
    img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    img_url_rel


    # %%
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    img_url


    # %%
    df = pd.read_html('http://space-facts.com/mars/')[0]
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    df


    # %%
    df.to_html()


    # %%
    # Visit the weather website
    url = 'https://mars.nasa.gov/insight/weather/'
    browser.visit(url)


    # %%
    # Parse the data
    html = browser.html
    weather_soup = soup(html, 'html.parser')


    # %%
    # Scrape the Daily Weather Report table
    weather_table = weather_soup.find('table', class_='mb_table')
    #print(weather_table.prettify())


    # %%
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)


    # %%
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    image_html = browser.html
    hemi_soup = soup( image_html, 'html.parser')

    items = hemi_soup.find_all('div', class_='item')

    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    for item in items: 
    
        title = item.find('h3').text
        
        image_url = item.find('a', class_='itemLink product-item')['href']
        #print(image_url)
        browser.visit(hemispheres_main_url + image_url)

        image_html = browser.html

        hemi_soup = soup(image_html, 'html.parser')

        images_url = hemispheres_main_url + hemi_soup.find('img', class_='wide-image')['src']

        hemisphere_image_urls.append({"Title" : title, "Image_URL" : images_url})


    # %%
    # 4. Print the list that holds the dictionary of each image url and title.
    hemisphere_image_urls
    return (hemisphere_image_urls)
    

    # %%
    # 5. Quit the browser
    #browser.quit()
