#dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    #setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = False)

    #----------------------------------
    #LATEST NEWS
    #----------------------------------
    task = 'LATEST NEWS'
    print(f"Scraping {task}...")

    #setup url
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    #retrieve latest news title paragraph
    news_title = soup.find_all('div', class_ = 'content_title')[0].text
    news_p = soup.find_all('div', class_ = 'article_teaser_body')[0].text

    print(f"{task} completed.")

    #----------------------------------
    #FEATURED IMAGE
    #----------------------------------
    task = 'FEATURED IMAGE'
    print(f"Scraping {task}...")

    #setup url
    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    #retrieve featured image
    partial_url = soup.find('a', class_ = 'showimg fancybox-thumbs')['href']
    featured_image_url = image_url + partial_url

    print(f"{task} completed.")

    #----------------------------------
    #FACTS
    #----------------------------------
    task = 'FACTS'
    print(f"Scraping {task}...")

    #url scraping w pandas
    facts_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(facts_url)
    df = tables[1]
    df.to_html('facts_mars.html', index = False)    

    #setup url
    facts_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(facts_url)
    df = tables[1]
    # df.to_html('facts_mars.html', index = False)
    html_table = df.to_html(index = False)

    print(f"{task} completed.")

    #----------------------------------
    #HEMISPHERES
    #----------------------------------
    task = 'HEMISPHERES'
    print(f"Scraping {task}...")

    #setup url
    hemi_base_url = 'https://marshemispheres.com/'
    browser.visit(hemi_base_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    #grabbing image containers
    hemi_data = soup.find_all('div', class_ = 'item')

    #empty list to store data
    hemi_ls_of_dicts = []
    #loop through item to pull data
    for i in range(len(hemi_data)):
        #setting up new html
        html = browser.html
        soup = bs(html, 'html.parser')

        #splinter click into each link
        hemi_text = soup.find_all('h3')[i].text
        browser.click_link_by_partial_text(hemi_text)

        #finding specific url
        subhtml = browser.html
        subsoup = bs(subhtml, 'html.parser')
        hemi_partial_url = subsoup.find('div', class_ = 'downloads').find('a')['href']

        #appending info
        temp_dict = {}
        temp_dict['title'] = hemi_text
        temp_dict['img_url'] = hemi_base_url + hemi_partial_url
        hemi_ls_of_dicts.append(temp_dict)

        #back to home page
        browser.back()

    print(f"{task} completed.")

    #----------------------------------
    #FINAL DICTIONARY
    #----------------------------------
    task = 'FINAL DICTIONARY'
    print(f"Doing {task}...")

    final_dict = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'html_table': html_table, 
        'hemi_ls_of_dicts': hemi_ls_of_dicts
    }

    print(f"{task} completed.")

    browser.quit()
    
    return final_dict