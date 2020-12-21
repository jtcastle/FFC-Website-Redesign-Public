# FFC-Website-Redesign-Public
Files for automatically restyling disc webpages

Created a script to scrape the data off of any current fresnoflightcenter.com disc webpage (name, description, flight numbers, inventory images, PayPal buttons, etc.) and reformat it into an updated html file.

How the update_styling_script works:

1) The most current information for a disc is pulled straight from the live webpage using the python requests library.

2) Information from within the webpage such as the name, description, flight numbers, inventory images, PayPal buttons, etc. is parsed using BeautifulSoup and saved. 

3) The parsed information from step 2 is then inserted into a local new_style_template.html file and reformmatted.

4) A new file is created and exported with the new html structure and an embedded link to the new discstyles.css style sheet.

5) This new file is ready to be simply uploaded to the site.


Before and After Examples can be viewed at the links below.

Before: https://www.fresnoflightcenter.com/boss.html

After: https://www.fresnoflightcenter.com/boss%20copy.html
