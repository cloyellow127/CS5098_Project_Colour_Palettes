from imports import *
async def get_colors(path, n):
    savepath = Path(path)
    if savepath.is_file():
        # blockPrint()
        recoloured_image, colour_palette, relative_frequencies = model.generate_colour_palette_from_image(path)
        # enablePrint()
        await asyncio.sleep(1)
        return colour_palette, relative_frequencies, n
    else:
        return None, None, None

def get_all_imgs_element(contents):
    # param beautifulsoup contents: the html contents of the whole page 
    # return: html contents of hust the images
    all_images = [node for node in contents.findAll('li', {"class": "item artwork icons"})]
    return all_images

def num_ofimages_on_pg(url):
    # param str url: the URL of the Art UK search result page
    # return: number of images on the page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    page.close()
    nodes = [[node] for node in soup.findAll('li', {"class": "item artwork icons"})]
    return int(len(nodes))

def get_all_img_url(url):
    # param str url: the URL of the Art UK search result page
    # return: the str url of the current search result page at max pages, showing maxnumber of images
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    page.close()
    
    number_all_art = soup.find('span', {"class": "count"}).find('span', {"class": "num"}).contents[0]
    number_all_art = int(number_all_art.replace(',', ''))
    current_num_img = num_ofimages_on_pg(url)
    page_number = int(url.split("/")[-1])
    num_per_page = current_num_img / page_number
    
    max_page = int(number_all_art / num_per_page)
    return url[:-1] + str(max_page + 1)

def get_spec_img_url(url, number):
    # param str url: the URL of the Art UK search result page
    # return: the str url of the current search result page at X pages, showing specified number of images
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    page.close()
    
    number_all_art = soup.find('span', {"class": "count"}).find('span', {"class": "num"}).contents[0]
    number_all_art = int(number_all_art.replace(',', ''))
    current_num_img = num_ofimages_on_pg(url)
    page_number = int(url.split("/")[-1])
    num_per_page = current_num_img / page_number
    
    num = int(number / num_per_page)
    max_page = int(number_all_art / num_per_page)
    return url[:-1] + str(min((num + 1), (max_page + 1)))

def get_number_all_art(url):
    # param str url: the URL of the Art UK search result page
    # return int: number of total artwork on the page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    page.close()
    number_all_art = soup.find('span', {"class": "count"}).find('span', {"class": "num"}).contents[0]
    return int(number_all_art.replace(',', ''))

def add_page_to_url(url):
    # param str url: the URL of the Art UK search result page
    # return str: URL with /page/1 added onto it.
    return url + "/page/1"

def remove_weird_chars(string):
    # param str string: a string
    # return str: a string with all \n and \t removed
    clean_string = string.replace('\n', '')
    clean_string = clean_string.replace('\t', '')
    return clean_string.strip()

def split_name_year(string):
    # param str string: a string that is formated as follows: Joe Mama (1998 - 2012)
    # return str: a string a list that is split by '(' as follows: ["Joe MaMa", "(1998 - 2012)"]
    if '(' not in string: 
        return [string.strip()]
    split_string = string.split('(')
    split_string[0] = split_string[0].strip()
    split_string[1] = ('(' + split_string[1]).strip()
    return split_string

def dimension_text_to_num(string):
    # param str string: string
    # return str: a string with out 'cm', 'H', 'W', '(E)', 'x'
    clean_string = string.replace('cm', 'x')
    clean_string = clean_string.replace('H', '')
    clean_string = clean_string.replace('W', '')
    clean_string = clean_string.replace(';', '')
    clean_string = clean_string.replace('(E)', '')
    clean_string = clean_string.split('x')

    h = 0.0
    for n in range(0, len(clean_string), 2):
        if clean_string[n].strip() != '':
            h += float(clean_string[n].strip())

    w = 0.0
    for n in range(1, len(clean_string), 2):
        if clean_string[n].strip() != '':
            w += float(clean_string[n].strip())
    
    return [h, w]

def year_to_estimate(creation_year):
    # param str string:  year that can be in follwing formats: 
    # 1800 - 1900, 18th C, etc
    # return str: 18th C -> 1800, years with range becomes average
    if creation_year is np.nan:
        return np.nan
    
    elif any(x in creation_year for x in ["-", "–"]):
        split_string = creation_year.split('–')

        if len(split_string) == 1:
            numeric_filter = filter(str.isdigit, creation_year)
            numeric_string = "".join(numeric_filter)
            return numeric_string.strip()
        else:        
            start_filter = filter(str.isdigit, split_string[0])
            start = "".join(start_filter)
            
            end_filter = filter(str.isdigit, split_string[1])
            end = "".join(end_filter)
            
            start = start.strip()
            end = end.strip()
            avg = int(start) + int(end)
            avg = round(avg / 2)

            if len(str(avg)) == 2:
                return str(avg) + "00"
            else:
                return str(avg)
        
    
    elif any(x in creation_year for x in ["th", "C"]):
        numeric_filter = filter(str.isdigit, creation_year)
        numeric_string = "".join(numeric_filter) + "00"
        return numeric_string.strip()
    
    else:
        numeric_filter = filter(str.isdigit, creation_year)
        numeric_string = "".join(numeric_filter)
        return numeric_string.strip()

async def get_all_other(session, art_uk_df, n):
    # param session: aiohttp Client Session
    # param pd.dataframe: dataframe
    # param int n: index of self.img_elements
    # return list: [medium, height, width, accession_number, enlarged_img]
    # get_all_other & set_all_other sets: the enlarged imaged url, height and width, Accession number, medium
    # as they are all in the embedded url, getting them all at once to increase speed
    async with session.get(art_uk_df['url'][n]) as response:
        page = await response.text()
        embeded_page = BeautifulSoup(page, 'html.parser')
        
        all_info = embeded_page.find('div', {'class' : 'masonry_details'})
        items = all_info.findAll('div', {'class' : 'masonry-item'})

        medium = np.nan
        height = np.nan
        width = np.nan
        accession_number = np.nan

        # Title
        title = str(art_uk_df['Title'][n])
        if "(" in title:
            title = str(title.split("(")[0])
        else:
            title = str(title.split(" ")[0])

        for tag in items:
            # Medium
            if tag.findNext('h5').text == "Medium":
                medium = tag.findNext('h5').findNext('p').text
                
            # Height and Width
            elif tag.findNext('h5').text == "Measurements":
                height = dimension_text_to_num(tag.findNext('h5').findNext('p').text)[0]
                width = dimension_text_to_num(tag.findNext('h5').findNext('p').text)[1]
                
            # Accession Number
            elif tag.findNext('h5').text == "Accession number":
                accession_number = tag.findNext('h5').findNext('p').text.replace('/', '_').replace(':', '_')
            

        # image_url
        if embeded_page.find('img', alt=re.compile(title)) is None:
            try:
                enlarged_img = embeded_page.find('img', {"alt": "Untitled"})
                enlarged_img = enlarged_img['src']
            except:
                enlarged_img = np.nan
 
        else:
            try:
                enlarged_img = embeded_page.find('img', alt=re.compile(title))
                enlarged_img = enlarged_img['src']
            except:
                enlarged_img = np.nan
            

        return [medium, height, width, accession_number, enlarged_img]

async def set_all_other(img_elements, art_uk_df, num_of_img):

     async with aiohttp.ClientSession() as session:
        tasks = []
        
        for number in range(num_of_img):
            tasks.append(asyncio.ensure_future(get_all_other(session, art_uk_df, number)))
                
        tasks = await asyncio.gather(*tasks)
        
        # image_url
        art_uk_df['Medium'] = [tasks[n][0] for n in range(num_of_img)]
        art_uk_df['height_cm'] = [tasks[n][1] for n in range(num_of_img)]
        art_uk_df['width_cm'] = [tasks[n][2] for n in range(num_of_img)]
        art_uk_df['Accession_number'] = [tasks[n][3] for n in range(num_of_img)]
        art_uk_df['img_URL'] = [tasks[n][4] for n in range(num_of_img)]

async def get_img(imgageURL, path):
    if not path.is_file():
        urllib.request.urlretrieve(imgageURL, path)
    await asyncio.sleep(1)
    
async def download_All(img_elements, folder_name, art_uk_df, num_of_img):
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    tasks = []

    for number in range(num_of_img):
        savepath = Path(folder_name + "/" + str(art_uk_df["Accession_number"][number]) + ".jpg")
        if art_uk_df["img_URL"][number] is not np.nan:
            tasks.append(asyncio.ensure_future(get_img(art_uk_df["img_URL"][number], savepath)))
    
    await asyncio.gather(*tasks)

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__
