from imports import *
import functions as fn

class art_uk_object:
    def __init__(self):
        self.url = None
        self.contents = None
        self.img_elements = None
        self.num_of_img = 0
        self.art_uk_df = pd.DataFrame(columns = ['Title', 'Artist', 'Creation_Date', 'estimate_year', 'url', 
                                        'img_URL', 'Medium', 'height_cm', 'width_cm', 'Accession_number'])                                       
        self.color_palette_df = pd.DataFrame(columns = ['R', 'G', 'B', 'freqency', 'id'])

    def __load_URL(self, url):
        self.url = url
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        page.close()

        self.contents = soup

        self.img_elements = fn.get_all_imgs_element(self.contents)
    
    def __get_title(self, n):
        # param int n: index of self.img_elements
        # return str: a string with all \n and \t removed
        title = self.img_elements[n].find('span', {"class": "title"})
        cleaned_title = fn.remove_weird_chars(title.contents[0])
        if cleaned_title == 'Untitled':
            return np.nan
        return cleaned_title
    
    def __get_URL(self, n):
        # param int n: index of self.img_elements
        # return str: embeded URL
        embeded_url = self.img_elements[n].find('a', {"class": ""})
        embeded_url = embeded_url.attrs['href']
        return embeded_url
    
    def __get_artist_name(self, n):
        # param int n: index of self.img_elements
        # return str: artist name or empty value
        tag = self.img_elements[n].find('span', {"class": "artist"})
        tag = fn.remove_weird_chars(tag.contents[0])
        
        
        if tag == "unknown artist":
            return np.nan

        artist_name_and_date = fn.split_name_year(tag)
        artist_name = artist_name_and_date[0]
        return artist_name
    
    def __get_art_year(self, n):
        # param int n: index of self.img_elements
        # return str: year or empty value
        tag = self.img_elements[n].find('span', {"class": "date"})
        if tag is None:
            return np.nan
        tag = fn.remove_weird_chars(tag.contents[0])
        return str(tag)
    
    def create_artuk_df(self): 
        # Title
        self.art_uk_df['Title'] = pd.Series([self.__get_title(n) for n in range(self.num_of_img)])
        
        # embedded url
        self.art_uk_df['url'] = pd.Series([self.__get_URL(n) for n in range(self.num_of_img)])
        
        # Artist Name
        self.art_uk_df['Artist'] = pd.Series([self.__get_artist_name(n) for n in range(self.num_of_img)])
        
        # Art Creation Date
        self.art_uk_df['Creation_Date'] = pd.Series([self.__get_art_year(n) for n in range(self.num_of_img)])
        
        self.art_uk_df['estimate_year'] = pd.Series([fn.year_to_estimate(self.art_uk_df['Creation_Date'][n]) for n in range(self.num_of_img)])


        loop = asyncio.get_event_loop()
        loop.run_until_complete(fn.set_all_other(self.img_elements, self.art_uk_df, self.num_of_img))
    
    def get_colours(self, filename):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__set_all_colors(filename))

    async def __set_all_colors(self, filename):
        tasks = []
        for number in range(self.num_of_img):
            filepath = filename + "/" + self.art_uk_df["Accession_number"][number] + ".jpg"
            if Path(filepath).is_file():
                tasks.append(asyncio.ensure_future(fn.get_colors(filepath, number)))

        await asyncio.gather(*tasks)
        
        for n in range(len(tasks)):
            temp_df = pd.DataFrame(columns = ['R', 'G', 'B', 'freqency', 'id'])
            temp_df['R'] = pd.Series([tasks[n].result()[0][x][0] for x in range(len(tasks[n].result()[0]))])
            temp_df['G'] = pd.Series([tasks[n].result()[0][x][1] for x in range(len(tasks[n].result()[0]))])
            temp_df['B'] = pd.Series([tasks[n].result()[0][x][2] for x in range(len(tasks[n].result()[0]))])
            temp_df['freqency'] = pd.Series([tasks[n].result()[1][x] for x in range(len(tasks[n].result()[1]))])
            temp_df['id'] = pd.Series([tasks[n].result()[2] for x in range(len(tasks[n].result()[0]))])
            self.color_palette_df = self.color_palette_df.append(temp_df, ignore_index=True)
    
    def export(self, filename):
        path = filename + '.csv'
        self.art_uk_df.to_csv(Path(path), index = False)

        color_path = filename + '_colours.csv'
        self.color_palette_df.to_csv(Path(color_path), index = False)
    
    def download(self, foldername):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(fn.download_All(self.img_elements, foldername, self.art_uk_df, self.num_of_img))

    def set_URL(self, url):
        self.url = fn.add_page_to_url(url)

    def set_all_images(self):
        self.num_of_img = fn.get_number_all_art(self.url)
        self.__load_URL(fn.get_all_img_url(self.url))
    
    def set_number_images(self, number):
        self.num_of_img = number
        self.__load_URL(fn.get_spec_img_url(self.url, number))
    
    def get_num_of_img(self):
        # return int: the number of images the user wants
        return self.num_of_img
    
    def get_contents(self):
        return self.contents