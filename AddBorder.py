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

	#change active layer to copy
	#pdb.gimp_image_set_active_layer(image, layer_copy)

	#Select Non Alpha
	pdb.gimp_selection_layer_alpha(layer_copy)

	# Select border with specified radius
	radius = 3
	pdb.gimp_selection_border(image, radius)

	## COPIER COLLER
	#pdb.gimp_image_undo_group_start(image)
	#prev_layer = image.active_layer

	# Create new layer (empty but same size)
	#pdb.gimp_edit_copy(image.active_layer)
	#fsel = pdb.gimp_edit_paste(drawable)

	#new_layer = pdb.gimp_layer_new_from_drawable(image.active_layer, image)
	

	# Fill with the border with foreground color
	fill_type = 0 # 0: FOREGROUND 
	pdb.gimp_drawable_edit_fill(drawable, fill_type)

	#pdb.gimp_floating_sel_to_layer(fsel)
	#image.active_layer.name = layer_name
	#pdb.plug_in_autocrop_layer(image, image.active_layer)
	#image.active_layer = prev_layer

	#pdb.gimp_image_undo_group_end(image)
	
	
	# Save image
	new_image = pdb.gimp_image_duplicate(image)
	layer = pdb.gimp_image_merge_visible_layers(new_image, CLIP_TO_IMAGE)
	pdb.gimp_file_save(new_image, layer, 'D:\\Logiciel\\renpy-7.4.6-sdk\\projects\\Eternal Bonds\\game\\images\\character sets\\nivi\\test.png', '?')
	pdb.gimp_image_delete(new_image)
	#pdb.gimp_file_save(new_image, layer, 'D:\Logiciel\renpy-7.4.6-sdk\projects\R City\game\images\character sets\nivi\nivi.png', '?')

	return

def listAllVisible(parent, outputList):
	for layer in parent.layers:
		if pdb.gimp_layer_get_visible(layer):
			outputList.append(layer)
			if pdb.gimp_item_is_group(layer):
				listAllVisible(layer, outputList)

register(
	"addBorder",
	N_("Add border to image"),
	"Add border to the image and save it to the folder specified in the script",
	"AronGomu",
	"@Copyright 2021",
	"2021",
	N_("addBorder"),
	"",
	[
		#(PF_INT32, "radius", "Radius Border Pixel:", 2) # Possibility of choosing radius size
	],
	[],
	addBorder,
	menu="<Toolbox>/Scripts/",
	domain=("gimp20-python", gimp.locale_directory))

main()