#!/usr/bin/env python

from gimpfu import *
import glob
import os

pdb = gimp.pdb

def resizePercentageBatch(scale, loadfolder):

# correct loadfolder: add (back-)slash if needed
    if not loadfolder.endswith(("/", "\\")):
        if os.name == "nt": # we need backslashes on windows, but slashes on linux/mac
            loadfolder = loadfolder + "\\"
        else:
            loadfolder = loadfolder + "/"

# prepare the file pattern
    filepattern = loadfolder + "*.png" # Don't forget the star
    filelist = glob.glob(filepattern)
    filelist.sort()
    # gimp.message(" ".join(filelist) # for debugging

# loop once for every file
    for filepath in filelist:
    # load image
        image = pdb.file_png_load(filepath, filepath)
        layer = image.active_layer
    # prepare filename
        if os.name == "nt": # we need backslashes on windows, but slashes on linux/mac
            outputfolder = "%soutput\\" % loadfolder # add the name of a new folder
        else:
            outputfolder = "%soutput//" % loadfolder # add the name of a new folder
        #gimp.message(outputfolder)
        if not os.path.exists(outputfolder):
            os.makedirs(outputfolder) # create the new folder if it doesn't exist yet
        filename = os.path.basename(filepath) # remove the path and only keep the actual filename with extension
        outputpath = outputfolder + filename

        # Get image width and height
        width_image = pdb.gimp_image_width(image)
        height_image = pdb.gimp_image_height(image)

        # Crop the 4 first lines because of koikatsu studio artefacts
        new_width = int(width_image * scale)
        new_height = int(height_image * scale)
        #offx = 0
        #offy = 0
        #pdb.gimp_image_resize(image, new_width, new_height, offx, offy)
        pdb.gimp_image_scale(image, new_width, new_height)
        # Crop to content
        drawable = layer
        pdb.plug_in_autocrop(image, drawable)

        # Merge layers to export the image as png
        image.merge_visible_layers(0)
        pdb.file_png_save_defaults(image, image.active_layer, outputpath, outputpath)
        
        ## Saving the project
        #outputpath = "%s.xcf" % outputpath
        #pdb.gimp_xcf_save(0, image, image.active_layer, outputpath, outputpath)


register(
    "resizePercentageBatch",
	N_("Resize a batch of image with a given percentage"),
	"Resize a batch of image with a given percentage",
	"AronGomu",
	"@Copyright 2021",
	"2021",
	N_("resizePercentageBatch"),
	"",
	[
    (PF_FLOAT, "scale", "The scaling of resizing, number to multiply to the height and width.", ""),
    (PF_STRING, "loadfolder", "The location of your images.", "")
	],
	[],
	resizePercentageBatch,
	menu="<Toolbox>/Filters/",
	domain=("gimp20-python", gimp.locale_directory)
)

main()