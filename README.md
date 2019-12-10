# New York City Bar list 
This is the repo for my SI 507 final project. 

## Description
In the project, I used BeautifulSoup4 and python systematically scraped over 130 pages which includes a list of bars in the New York City and bar details. This is the [original source page](https://www.theinfatuation.com/new-york/guides/the-manhattan-bar-directory).

- The Cache file and csvs are included. However, you could download and use the final_proj.py file to recreate the cache. It would take a few minutes to scrape all the webpages though.

- It takes around 25 seconds to run the final_proj_test.py file because of the scraping loop. I haven't found a way to reduce the time yet. 

## Set up
- To run the program, run the final_proj.py file,then the app.py file to see the visual representations. 
- The requirements.txt is shown in the front page.

## Code Structure 
I started by scraping the page with cache system, creating a list of bars utilizing the Bar class. Then created a list of neighborhoods name with ability to catch the bars that don't associate with a neighborhood.

## User Guide 



