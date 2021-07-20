from model.model import generate_colour_palette_from_image


file_name = "/Users/tim/OneDrive - University of St Andrews/University/MScProject/ColourPaletteExtractor/colourpaletteextractor/data/sampleImages/annunciation-1434.jpg"

recoloured_image, colour_palette, relative_frequencies = generate_colour_palette_from_image(file_name)