#---------------------------------------------------------------
# Name:        Random Diffuse Colors
#
# Purpose:     Create random diffuse colors to selected objects
# Author:      Sakari Niittymaa
#
# Created:     27.4.2016
# Copyright:   Copyright(c) 2016 Sakari Niittymaa
#              http://www.niittymaa.com
#
# Licence:     The MIT License (MIT)
#---------------------------------------------------------------

import bpy,random

# Change if needed
useNodes = True
createNewMaterialSlot = False
replaceFirstMaterial = False

# Loop all selected objects
for ob in bpy.context.selected_objects:
    
    # Activate current object to assign material
    bpy.context.scene.objects.active = ob
    
    # Get object material length
    matLen = len(ob.data.materials)
    
    # Generate random color values
    # Tip: You can range channel values
    r = random.randint( 0, 255)
    g = random.randint( 0, 255)
    b = random.randint( 0, 255)
    
    # Color name from HEX value
    # Note: Value based to no gamma corrected value. 
    # See right value to setup "Color Management" > "Display Device" > "None"
    hexName = '#%02x%02x%02x' % (r,g,b)   
    
    # Replace material in first material slot
    if matLen and replaceFirstMaterial and not createNewMaterialSlot:
        ob.active_material_index = 0
        mat = ob.active_material
        mat.name = hexName
    
    # Create new material and name it by HEX code
    else:
        mat = bpy.data.materials.new(name=hexName)
    
    # Set diffuse to material
    mat.diffuse_color = (r/255,g/255,b/255)
    
    # Assign material to exist material in object
    if matLen and createNewMaterialSlot != True:
        ob.active_material_index = 0
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.material_slot_assign()
        bpy.ops.object.mode_set(mode='OBJECT')
        ob.data.materials[0] = mat
    
    # Append to new material slot and assign to object
    else:
        ob.data.materials.append(mat)
        ob.active_material_index = matLen   
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.material_slot_assign()
        bpy.ops.object.mode_set(mode='OBJECT')
        
    # Enable 'Use nodes' for material
    mat.use_nodes = useNodes