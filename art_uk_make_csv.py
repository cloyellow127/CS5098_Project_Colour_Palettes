from art_uk_object import *
from art_uk_object import art_uk_object
import functions as fn
def main():
    if len(sys.argv) != 4:
        print("Usage: python art_uk_viewer.py <number of images> <name of csv> <URL>")
        sys.exit()

    file_name = sys.argv[2]
    url = sys.argv[3]

    art_uk = art_uk_object()
    art_uk.set_URL(url)

    if sys.argv[1].isnumeric():
        num_img = int(sys.argv[1])
        art_uk.set_number_images(num_img)

    elif sys.argv[1] == "all":
        art_uk.set_all_images()
    
    else:
        print("Usage: python art_uk_viewer.py <number of images> <name of csv> <URL>")
        sys.exit()

    art_uk.create_artuk_df()
    # art_uk.download(file_name)
    # art_uk.get_colours(file_name)
    art_uk.export(file_name)

if __name__ == "__main__":
    main()
    # print(os.path.isdir("/MSc-CS-Project---ColourPaletteExtractor-master/"))
    # timer = time.process_time()
    # print(time.process_time() - timer)
    # pip freeze > requirements.txt