# New York City Bar list 

## Description
In the project, I scraped over 130 pages which includes a list of bars in the New York City and the bar details such as open hours, addresses and websites. This is the [original source page](https://www.theinfatuation.com/new-york/guides/the-manhattan-bar-directory).

- The Cache file and csvs are included. However, you could download and use the final_proj.py file to recreate the cache. It would take a few minutes to scrape all the webpages though.

- It takes around 25 seconds to run the final_proj_test.py file because of the scraping loop. I haven't found a way to reduce the time yet. 

## Set up
- To run the program, run the final_proj.py file,then the app.py file to see the visual representations. 
- The requirements.txt is shown in the front page.

## Code Structure 

- final_proj.py

I started by scraping the page with cache system, creating a list of bars utilizing the Bar class. 
Then created a list of neighborhoods name with ability to catch the bars that don't associate with a neighborhood.
I then saved the bars into the bars_info.csv file, and the neighborhoods in a neighborhoods.csv file.
By creating the Bars and Neighborhood tables in the nycbars.db database, I populated the table with the information in csv file through init_db(), insert_data(). Then I calculated average price ratings in each neighborhood and count the number of bars in each neighborhood using the insert_calc_neigh(), and updating the information into the neighborhoods.csv through update_neigh_csv().

- model.py

init_neighbors() creates the table for the list of neighbors from the associated csv file. 
get_neighbors() updates the table content based on the sorting requirement input by the user. 
get_filtered_bars() calls the databse and updates the list of bars based on the neighborhood id of interest. 


## User Guide 
- Start with click on either "explore neighborhood" or "explore bar list"
- On Neighborhood page, you can sort the neighborhoods based on the average price rating of the bars in the neighborhood, or you can sort based on the number of bars in the neighborhood. 
- When you have a neighborhood in mind that you would like to browse, click on the "let's go" to go to the bar list view. 

- On Bars page, by default, it shows all the bars in the database with selected bar information. 
- You can input the id of the neighborhood that you earlier wanted to explore more, then the page would refresh and only show the bar in the designated neighborhood. The title of the page would also update with the neighborhood name that you are exploring. 
- If you forget the neighborhood id, you can click on the "click here" to view the neighborhood information.



