# bs4-scrapping-project

This project uses beautiful soupe to scrape search engines for fake PC Matic support sites offering phone support.

The program first sends the request to  a docker splash image to render the javascript on the page then scraps the link and text from the seach results, then saves the data in pandas dataframe. The data frame is then processed an given a shady score, and then from there filtered into a csv file after.

