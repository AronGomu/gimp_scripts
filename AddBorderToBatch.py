#!/usr/bin/env python

from gimpfu import *
import glob
import os

pdb = gimp.pdb

def addBorderToBatch(loadfolder):

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
        gimp.message(outputfolder)
        if not os.path.exists(outputfolder):
            os.makedirs(outputfolder) # create the new folder if it doesn't exist yet
        filename = os.path.basename(filepath) # remove the path and only keep the actual filename with extension
        outputpath = outputfolder + filename

        # now the actual work

        # copy the selected layer
        layer_copy = pdb.gimp_layer_new_from_drawable(layer, image)

        # insert the layer_copy on top of the layers stack
        layer_position = 0
        pdb.gimp_image_insert_layer(image, layer_copy, None, layer_position)

        #Select Non Alpha
        pdb.gimp_selection_layer_alpha(layer_copy)

        # Select border with specified radius
        radius = 3
        pdb.gimp_selection_border(image, radius)

        # Fill with the border with foreground color
        fill_type = 0 # 0: FOREGROUND 
        pdb.gimp_drawable_edit_fill(layer, fill_type)

        # Merge layers to export the image as png
        image.merge_visible_layers(0)
        pdb.file_png_save_defaults(image, image.active_layer, outputpath, outputpath)
        
        ## Saving the project
        #outputpath = "%s.xcf" % outputpath
        #pdb.gimp_xcf_save(0, image, image.active_layer, outputpath, outputpath)


register(
    "addBorderToBatch",
	N_("Add border to a batch of images."),
	"Add border to all .png file in specified folder and save them in a output folder in the same folder.",
	"AronGomu",
	"@Copyright 2021",
	"2021",
	N_("addBorderToBatch"),
	"",
	[
    (PF_STRING, "loadfolder", "The location of your images.", "")
	],
	[],
	addBorderToBatch,
	menu="<Toolbox>/Scripts/",
	domain=("gimp20-python", gimp.locale_directory)
)

main()