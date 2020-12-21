from bs4 import BeautifulSoup
import requests

"""
PART 1 FOR SCRAPING HTML OFF AN EXISTING PAGE
"""

url = "https://www.fresnoflightcenter.com/Teebird3.html"

webpage = requests.get(url)

soup = BeautifulSoup (webpage.content, "html.parser")


"""
Function for scraping each paypal html form and placing into a list.
First paramenter is starting_num (the desired starting index value of the list)
Second parameter is ending_num (the desired ending index value of the list)
To return the complete list enter 0, None as arguments
"""

def get_form(starting_num, ending_num):
    cell_contents = soup.find_all("form")

    content = []
    for cell in cell_contents:
      content.append(cell)

    return content[starting_num:ending_num]


"""
Functions for scraping disc name, disc description, and disc availiability
Call get_name function to return the string containing the name of the disc
Call get_description function to return the string containing the description of the disc
Call get_flight_numbers function to return the string containing the flight numbers of the disc
Call get_avail function to return the string containing the availability of the disc
Call get_link function to return the external link for more info from the mfg 
"""

def get_name():
    cell_contents = soup.find_all("td")

    content = []
    for cell in cell_contents:
        content.append(cell.get_text(strip=True))

    return content[7]

def get_description():
    cell_contents = soup.find_all("td")

    content = []
    for cell in cell_contents:
        content.append(cell.get_text())

    description = content[2]
    split_description = description.split(".")
    joined_description = ".".join(split_description[:-1]) + "."

    return joined_description

def get_flight_numbers():
    cell_contents = soup.find_all("td")

    content = []
    for cell in cell_contents:
        content.append(cell.get_text())

    description = content[2]
    split_description = description.split(".")
    flight_numbers = split_description[-1]
    stripped_flight_numbers = flight_numbers.strip()

    return stripped_flight_numbers

def get_avail():
    cell_contents = soup.find_all("td")

    content = []
    for cell in cell_contents:
        content.append(cell.get_text())

    return content[6]

def get_link():
    cell_contents = soup.find_all("a")

    return cell_contents[0]



"""
Functions for scraping disc images
Call get_main_img function to return the bs4 element tag for the html of the main image
Call get_imgs function to return a list of bs4 elements of the available disc images
"""

def get_main_img():
    cell_contents = soup.find_all(height="350")

    content = []
    for cell in cell_contents:
        del cell["height"]
        del cell["width"]
        cell["width"] = "100%"
        content.append(cell)

    return content[0]

def get_imgs():
    cell_contents = soup.find_all(height="250")

    content = []
    for cell in cell_contents:
        del cell["height"]
        del cell["width"]
        cell["width"] = "250px"
        cell["height"] = "250px"
        content.append(cell)

    return content

"""
Checker function
Since some pages contain images of already sold items, the amount
of paypal forms on a page does not match the amount of images.

This function checks for this mismatch and removes images without
corresponding paypal forms by creating a list of all image names
and a list of all form labels. Each index of the image list is
checked for a coresponding value in the form list. If no corresponding
value exists, the image is deleted.
"""

### Checker function

print("Number of forms on page: " + str(len(get_form(0, None))))

def checker():
    images = (get_imgs())
    disc_name = get_name()
    disc_lower = disc_name.lower()
    all_forms = get_form(0, None)

    image_list = []

    for image in images:
        src = image["src"]
        src_split = (src.split("/"))
        src_split_img_name = src_split[-1]
        src_split_name = (src_split_img_name.split(".")[0])
        src_split_num = src_split_name.split(disc_lower)
        disc_cap = disc_lower.capitalize()
        src_join = (disc_cap + " " + src_split_num[1])
        image_list.append(src_join)

    num_of_images = (len(images))

    list1 = []
    values = []
    skip_counter = 0

    for form in range(len(all_forms)):
        find_table = all_forms[form].find("table")
        find_td = find_table.find("td")
        form_input = find_td.find("input")
        value = form_input['value']
        values.append(value)

    for image in image_list:
        if image not in values:
            list1.append(image_list.index(image))


    print("Disc images deleted: " + str(list1))

    if len(list1) != 0:
        for i in list1:
            del images[i]

    return images


"""
PART 2 FOR INSERTING HTML INTO NEW STYLING
"""

url2 = "https://fresnoflightcenter.com/Luna%20Example/sample_disc_copy_trial.html"

webpage2 = requests.get(url2)

soup_out = BeautifulSoup (webpage2.content, "html.parser")


def replace_name():
    
    name = soup_out.h2

    new_name = soup_out.new_tag("h2")
    new_name.string = (get_name())
    name.replace_with(new_name)

def replace_main_img():

    main_img = soup_out.find("div", {"class": "description-container"})
    disc_img = main_img.img
    disc_img.replace_with(get_main_img())


def replace_description():
    
    description = soup_out.p

    new_description = soup_out.new_tag("p")
    new_description.string = (get_description())
    description.replace_with(new_description)

def replace_flight_numbers():

    flight_numbers = soup_out.find_all("p")[1]

    new_flight_numbers = soup_out.new_tag("p")
    new_flight_numbers.string = get_flight_numbers()
    flight_numbers.replace_with(new_flight_numbers)


def replace_link():
    
    link_in = get_link()
    href = link_in["href"]

    link_out = soup_out.find("a")
    del link_out["href"]
    link_out["href"] = href


###Code that will become the replace discs function

def replace_discs():

    #Start by clearing template placeholders (do this once)
    disc_container_div = soup_out.find(class_="disc-container")
    disc_container_div.clear()

    #Fill out the discs here
      
    ims = checker()
    fms = get_form(0, None)


    for i in (range(0, len(fms))):

        column25div = soup_out.new_tag("div")
        column25div['class'] = "column25"
        disc_container_div.insert(i, column25div)

        column25div.insert(0, (ims[i]))
        column25div.insert(1, (fms[i]))


replace_name()
replace_main_img()
replace_description()
replace_flight_numbers()
replace_link()
replace_discs()


print(soup_out.prettify())

#for loop that only works for sequential discs
'''
    list1 = []

    skip_counter = 0

    for i in (range(1, num_of_images)):
        form = all_forms[i-1]
        value = form.find_all(value=(disc_name + " " + str(i + skip_counter)))
        if len(value) != 1:
            list1.append(i-1)
            skip_counter += 1

    print(list1)
'''


url_split = url.split("/")
output_filename = url_split[-1]

'''
# Outputs the file
with open(output_filename, "wb") as f_output:
    f_output.write(soup_out.prettify("utf-8"))

print("File Updated")
'''


