import pandas as pd
import numpy as np
import requests
import json
from pandas.io.json import json_normalize
from PIL import Image
from os import path
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlopen
import re
import time
import aiohttp
import asyncio
from pathlib import Path
import asyncio
import sys, os
import csv
from tabulate import tabulate
import csvkit
import tabloo
import git

if not os.path.isdir("MSc-CS-Project---ColourPaletteExtractor-master/"):
    cwd = os.getcwd()
    git.Repo.clone_from("https://github.com/PurpleCrumpets/MSc-CS-Project---ColourPaletteExtractor.git", cwd + "/MSc-CS-Project---ColourPaletteExtractor-master/")

sys.path.append(path.abspath('MSc-CS-Project---ColourPaletteExtractor-master/'))
from colourpaletteextractor.model import model