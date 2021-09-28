#! /usr/bin/env python2

from gimpfu import *

def addBorder(image, drawable):

	# get active layer
	layer = pdb.gimp_image_get_active_layer(image)

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

	# set foreground color
	pure_black_color = (0.0, 0.0, 0.0, 1.0)
	foreground = pure_black_color
	pdb.gimp_context_set_foreground(foreground)

	# Fill with the border with foreground color
	fill_type = 0 # 0: FOREGROUND 
	pdb.gimp_drawable_edit_fill(drawable, fill_type)
	
	# Save image
	new_image = pdb.gimp_image_duplicate(image)
	layer = pdb.gimp_image_merge_visible_layers(new_image, CLIP_TO_IMAGE)
	pdb.gimp_file_save(new_image, layer, 'D:\\Logiciel\\renpy-7.4.6-sdk\\projects\\Eternal Bonds\\game\\images\\character sets\\nivi\\test.png', '?')
	pdb.gimp_image_delete(new_image) # Delete old file after been moved

	return

"""
def listAllVisible(parent, outputList):
	for layer in parent.layers:
		if pdb.gimp_layer_get_visible(layer):
			outputList.append(layer)
			if pdb.gimp_item_is_group(layer):
				listAllVisible(layer, outputList)
"""

register(
    "python_fu_test_hello_world",
    "Hello world",
    "Display a 'hello world' message",
    "JFM",
    "Open source (BSD 3-clause license)",
    "2013",
    "<Image>/Filters/AddBorder",
    "*",
    [],
    [],
    addBorder)

main()