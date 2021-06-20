"""
https://stackoverflow.com/questions/50207292/how-to-convert-geotiff-to-jpg-in-python-or-java
ve code simply create a jpg file with band 1 scaled into byte range. You could add more bands by adding, '-b 2' etc. Also notice that scale automatically wraps the entire range into byte range. If you like something else you could use '-scale min_val max_val' in order to specify the range you like, since often you have no need of either the lowest or highest values available.
The above worked well for me except the JPEG resolution wasn't great. Swapping JPEG to PNG worked better.

https://gdal.org/programs/gdal_translate.html
https://gdal.org/programs/gdal_translate.html
"""
import gc
import os
import pprint as pp
import time
from datetime import datetime
from os import listdir
from os.path import join, isfile

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import rasterio
import rasterio.mask
import wordninja
from cleantext import clean
from natsort import natsorted
from tqdm import tqdm

tif_dir_path = str(input("Enter path to folder with geotiff files -->"))
# -----------------------------------------------------------------
output_folder_name = "full_color_PNGs_geotiff2png"
if not os.path.isdir(join(tif_dir_path, output_folder_name)):
    os.mkdir(join(tif_dir_path, output_folder_name))
    # make a place to store outputs if one does not exist
output_path_full = os.path.join(tif_dir_path, output_folder_name)
print("outputs will be in: \n", output_path_full)


# ----------------------------------------------------------------------------

def cleantxt_wrap(ugly_text):
    # a wrapper for clean text with options different than default

    # https://pypi.org/project/clean-text/
    cleaned_text = clean(ugly_text,
                         fix_unicode=True,  # fix various unicode errors
                         to_ascii=True,  # transliterate to closest ASCII representation
                         lower=True,  # lowercase text
                         no_line_breaks=True,  # fully strip line breaks as opposed to only normalizing them
                         no_urls=True,  # replace all URLs with a special token
                         no_emails=True,  # replace all email addresses with a special token
                         no_phone_numbers=True,  # replace all phone numbers with a special token
                         no_numbers=False,  # replace all numbers with a special token
                         no_digits=False,  # replace all digits with a special token
                         no_currency_symbols=True,  # replace all currency symbols with a special token
                         no_punct=True,  # remove punctuations
                         replace_with_punct="",  # instead of removing punctuations you may replace them
                         replace_with_url="<URL>",
                         replace_with_email="<EMAIL>",
                         replace_with_phone_number="<PHONE>",
                         replace_with_number="<NUM>",
                         replace_with_digit="0",
                         replace_with_currency_symbol="<CUR>",
                         lang="en"  # set to 'de' for German special handling
                         )

    return cleaned_text


def beautify_filename(filename, num_words=20, start_reverse=False,
                      word_separator="_"):
    # takes a filename stored as text, removes extension, separates into X words ...
    # and returns a nice filename with the words separateed by
    # useful for when you are reading files, doing things to them, and making new files

    filename = str(filename)
    index_file_Ext = filename.rfind('.')
    current_name = str(filename)[:index_file_Ext]  # get rid of extension
    clean_name = cleantxt_wrap(current_name)  # wrapper with custom defs
    file_words = wordninja.split(clean_name)
    # splits concatenated text into a list of words based on common word freq
    if len(file_words) <= num_words:
        num_words = len(file_words)

    if start_reverse:
        t_file_words = file_words[-num_words:]
    else:
        t_file_words = file_words[:num_words]

    pretty_name = word_separator.join(t_file_words)  # see function argument

    # NOTE IT DOES NOT RETURN THE EXTENSION
    return pretty_name[: (len(pretty_name) - 1)]  # there is a space always at the end, so -1


# ----------------------------------------------------------------------------

def load_landsat_image_single(imgpath):
    # ONLY USEFUL IF BANDS ARE IN DIFFERENT FILE
    image = {}
    datboi = rasterio.open(imgpath)
    bands = datboi.indexes
    for band in bands:
        # considering the landsat images end with *_SR_B#.TIF, we will use it to locate the correct file
        this_label = "B" + str(band)
        image.update({this_label: datboi.read(band)})

    return image


def convert_tif_to_png_v2(full_input_path, output_folder, download_pic=False):
    img = load_landsat_image_single(full_input_path)
    basename = beautify_filename(os.path.basename(full_input_path))

    # stack the layers to create a cube
    rgb = np.stack([img['B4'], img['B3'], img['B2']], axis=-1)

    # normalize the values
    rgb = rgb / rgb.max() * 2

    # display the image with a slightly increased figure size
    plt.figure(figsize=(10, 10), tight_layout=True, clear=True)
    plt.imshow(rgb, norm=matplotlib.colors.Normalize(), interpolation="lanczos")

    plt.title(os.path.basename(full_input_path))
    outname = "[conv to pretty image]" + basename + ".png"
    plt.savefig(join(output_folder, outname), dpi=300, facecolor='w', edgecolor='w',
                transparent=True, bbox_inches="tight")
    plt.close()


# ----------------------------------------------------------------------------


# load files
files_to_munch = natsorted([f for f in listdir(tif_dir_path) if isfile(os.path.join(tif_dir_path, f))])
total_files_1 = len(files_to_munch)
removed_count_1 = 0
approved_files = []
# remove non-tif_image files
for prefile in files_to_munch:
    if prefile.endswith(".tif"):
        approved_files.append(prefile)
    else:
        files_to_munch.remove(prefile)
        removed_count_1 += 1

print("out of {0:3d} file(s) originally in the folder, ".format(total_files_1),
      "{0:3d} non-tif_image files were removed".format(removed_count_1))
print('\n {0:3d} tif_image file(s) in folder will be transcribed.'.format(len(approved_files)))
pp.pprint(approved_files[:10])
print("...\n")
# loop
st = time.time()
verbose = False
for tif_file in tqdm(approved_files, total=len(approved_files),
                     desc="Resizing tif_images"):
    index_pos = approved_files.index(tif_file)

    try:
        convert_tif_to_png_v2(join(tif_dir_path, tif_file), output_path_full)
    except:
        print("was unable to process the file {}. moving to next one".format(tif_file))

    if index_pos % 5 == 0:
        gc.collect()

rt = round((time.time() - st) / 60, 2)
print("\n\nfinished converting all tif_images - ", datetime.now())
print("Converted {} tif_images in {} minutes".format(len(approved_files), rt))
print("they are located in: \n", output_path_full)
print("they are located in: \n", output_path_full)
