#---------------------------------------------------------------
# Name:        Random Diffuse Colors
#
# Purpose:     Create random diffuse colors to selected objects
# Author:      Sakari Niittymaa
#
# Created:     27.4.2016
# Updated:     19.8.2024 (Updated to work with blender 4.2)
# Copyright:   Copyright(c) 2016 Sakari Niittymaa
#              http://www.niittymaa.com
#
# Licence:     The MIT License (MIT)
#---------------------------------------------------------------

import bpy
import random
import bpy.app

# Configuration options
useNodes = True  # Whether to use node-based materials
createNewMaterialSlot = False  # Whether to create a new material slot
replaceFirstMaterial = False  # Whether to replace the first material in the slot

# Version checking for backward compatibility
blender_version = bpy.app.version

# Function to handle material assignment
def assign_material(ob, mat, mat_len):
    if blender_version >= (2, 8, 0):
        # Blender 2.8 and newer
        ob.active_material_index = 0
        if mat_len > 0 and not createNewMaterialSlot:
            ob.data.materials[0] = mat
        else:
            ob.data.materials.append(mat)
            ob.active_material_index = len(ob.data.materials) - 1
    else:
        # Blender 2.7 and older
        ob.active_material_index = 0
        if mat_len > 0 and not createNewMaterialSlot:
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.material_slot_assign()
            bpy.ops.object.mode_set(mode='OBJECT')
            ob.data.materials[0] = mat
        else:
            ob.data.materials.append(mat)
            ob.active_material_index = len(ob.data.materials) - 1
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.material_slot_assign()
            bpy.ops.object.mode_set(mode='OBJECT')

# Loop through all selected objects
for ob in bpy.context.selected_objects:

    # Set the object as active
    if blender_version >= (2, 8, 0):
        bpy.context.view_layer.objects.active = ob
    else:
        bpy.context.scene.objects.active = ob
    
    # Get the number of materials the object has
    mat_len = len(ob.data.materials)
    
    # Generate random color values
    r = random.random()
    g = random.random()
    b = random.random()
    
    # Create a color name using HEX format
    hex_name = '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))
    
    # Handle material assignment based on user settings
    if mat_len > 0 and replaceFirstMaterial and not createNewMaterialSlot:
        # Replace the material in the first slot
        ob.active_material_index = 0
        mat = ob.active_material
        mat.name = hex_name
    else:
        # Create a new material with the HEX name
        mat = bpy.data.materials.new(name=hex_name)

    # Set the material to use nodes if required
    if useNodes:
        if blender_version >= (2, 8, 0):
            # Blender 2.8 and newer
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf is None:
                bsdf = mat.node_tree.nodes.new(type="ShaderNodeBsdfPrincipled")
                mat.node_tree.links.new(bsdf.outputs['BSDF'], mat.node_tree.nodes['Material Output'].inputs['Surface'])
            bsdf.inputs['Base Color'].default_value = (r, g, b, 1)  # RGBA
        else:
            # Blender 2.7 and older
            mat.use_nodes = True
            mat.diffuse_color = (r, g, b)  # RGB only in older versions
    else:
        if blender_version >= (2, 8, 0):
            # For materials without nodes in newer versions
            mat.diffuse_color = (r, g, b, 1)  # RGBA
        else:
            # For materials without nodes in older versions
            mat.diffuse_color = (r, g, b)  # RGB

    # Assign material using the correct method for the Blender version
    assign_material(ob, mat, mat_len)
