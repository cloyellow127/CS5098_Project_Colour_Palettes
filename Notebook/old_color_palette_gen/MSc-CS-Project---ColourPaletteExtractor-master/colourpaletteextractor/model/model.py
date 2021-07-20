# TODO: add ability to run the model by itself, without the GUI using __main__
import errno
import os
from sys import argv

from colourpaletteextractor.model import imagedata
from colourpaletteextractor.model.algorithms import nieves2020


def generate_colour_palette_from_image(path_to_file: str) -> list:

    model = ColourPaletteExtractorModel()

    if os.path.isfile(path_to_file) is False:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), path_to_file)
        # TODO: explain why the file is invalid (ie make sure that there are no spaces in the names of folders etc)
        # Put it in quotes
    else:
        image_data_id, image_data = model.add_image(path_to_file)

    print("Added image!")

    # Get colour palette of the image (image 0 in list)
    model.generate_palette(image_data_id, "Tab_0", None)

    print("\n---------------")
    print("Colour Palette:")
    for colour in image_data.colour_palette:
        print(colour)
    print("---------------")

    return image_data.colour_palette


class ColourPaletteExtractorModel:
    ERROR_MSG = "Error! :'("
    supported_image_types = {"png", "jpg", "jpeg"}

    def __init__(self, algorithm_name=None):

        self._image_data_id_counter = 0
        self._image_data_id_dictionary = {}

        # self._images = []
        if algorithm_name is None:
            # self._algorithm = nieves2020.Nieves2020()  # Default algorithm
            self._algorithm = "nieves_2020"  # Default algorithm
        else:
            print("Algorithm not None")  # TODO: add new algorithm

    def evaluate_expression(self, expression):
        """slot function.
        :param expression:
        :return:
        """

        try:
            result = str(eval(expression, {}, {}))
        except Exception:
            result = ColourPaletteExtractorModel.ERROR_MSG

        return result

    def _get_algorithm(self):

        if self._algorithm == "nieves_2020":
            print("Nieves")
            return nieves2020.Nieves2020()

        else:
            print("Not a valid algorithm")
            # TODO: Throw exception

    # def set_algorithm(self, algorithm_name="nieves_2020"):
    #     """Set the algorithm use to extract the colour palette of an image."""
    #
    #     if algorithm_name == "nieves_2020":
    #         print("Nieves")
    #         self._algorithm = nieves2020.Nieves2020()
    #
    #     else:
    #         print("Not a valid algorithm")
    #         # TODO: Throw exception

    def add_image(self, file_name_and_path: str):
        """From the path to an image, create a new image_data object and add it to the
         dictionary of image_data objects with a new ID number."""

        # Create new ImageData object to hold image (and later the colour palette)
        new_image_data = imagedata.ImageData(file_name_and_path)

        # Add to image dictionary
        new_image_data_id = ("Tab_" + str(self._image_data_id_counter))
        self._image_data_id_counter += 1
        self._image_data_id_dictionary[new_image_data_id] = new_image_data
        # TODO: Add checks to make sure new key doesn't overwrite a current key

        return new_image_data_id, new_image_data

    def remove_image_data(self, image_data_id):
        """Remove image from list of images by its index."""
        # self._images.pop(i)
        self._image_data_id_dictionary.pop(image_data_id)
        # TODO: add checks if not found

    def _get_image_copy(self, image_data_id):
        print("Retrieving image...")
        # image_data = self._images[index]
        image_data = self._image_data_id_dictionary.get(image_data_id)

        return image_data.image.copy()
        # TODO: Add checks for the index in case it is out of range

    def get_image_data(self, image_data_id):
        return self._image_data_id_dictionary.get(image_data_id)

    @property
    def image_data_id_dictionary(self):
        return self._image_data_id_dictionary

    def generate_palette(self, image_data_id, tab, progress_callback=None):
        print("Generating colour palette for image:", image_data_id)

        image_data = self._get_image_copy(image_data_id)

        # Get algorithm and process image with it
        algorithm = self._get_algorithm()
        if progress_callback is not None:
            algorithm.set_progress_callback(progress_callback, tab)
        recoloured_image, colour_palette = algorithm.generate_colour_palette(image_data)

        self._image_data_id_dictionary[image_data_id].recoloured_image = recoloured_image
        self._image_data_id_dictionary[image_data_id].colour_palette = colour_palette

        print(recoloured_image.shape, len(colour_palette))


if __name__ == "__main__":

    # data_dir = "data"
    # print(__file__)
    # os.getcwd() - where script executed from!
    # print(argv[0])  # Gives you absolute path to the file that was run - this could be useful later on

    file_name = argv[1]

    if len(argv) == 3:
        model_type = argv[2]

    colour_palette = generate_colour_palette_from_image(file_name)

    # print(os.path.isfile(file_name))

    # # Check if file is an image
    # found = False
    # for file_type in model.supported_image_types:
    #     file_type = "." + file_type
    #     if search(file_type, file_name):
    #         found = True
    #         # model.add_image()
    #         break
    # Check if file can be found
    #
    #
    # # Check if file is a path
    # if os.path.isdir(file_name):
    #     print("Found directory")

    # TODO Check inputs
    # If provided with a directory, apply to all valid files inside
    # Else if just a file - just do that one
    # If provided with a second argument - this is used to control the algorithm used to extract

    # model.add_image()