from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
   
    # MARS NEWS
    # Visit mars website
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(3)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Scrape data and view it
    news = soup.find("li", class_="slide")

    # Get the title and description of the latest news
    news_title = news.find("div", class_="content_title").text
    news_p = news.find("div", class_="article_teaser_body").text

    # MARS IMAGE
    # Visit the image url
    image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image)

    time.sleep(3)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    # find article for featured image and print
    img_info = soup.find("li",class_="slide").a["data-fancybox-href"]
    base_url = "https://www.jpl.nasa.gov"
    featured_image_url = base_url + img_info
   
    # MARS FACTS
    # Visit the facts url
    spacefacts = 'https://space-facts.com/mars/'
    df = pd.read_html(spacefacts)
    mars_df = df[0]
    mars_df = mars_df.rename({0: "", 1: "Mars Statistics"}, axis =1).set_index("")
    mars_df.to_html("mars_facts.html")
    
    # MARS HEMISPHERES
    # Visit the hemisphers url
    hem = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hem)

    time.sleep(3)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser") 
    
    # Find the image urls
    img_links= soup.find_all("div", class_="item")
    hemisphere_image_urls = []
    
    for img in img_links:
        # Get title
        title = img.find("h3").text
        # Click onto image url to get better image
        extra = img.find("a")["href"]
        base = "https://astrogeology.usgs.gov"
        get_url = base + extra
        response = requests.get(get_url)
        # Soup it up
        soup = bs(response.text, "html.parser") 
        # Get full res image
        full_res_img = soup.find("img", class_="wide-image")["src"]
        img_url = base + full_res_img
        hemisphere_image_urls.append({"title": title, "img_url": img_url})

    #STORING DATA
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts" : mars_facts,
        "hemisphere_image_urls" : hemisphere_image_urls
        }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
