import mathutils as mt
import numpy as np
import MatlabBlenderIO as mlb
import os, bpy, time


def obj2csv(filepath, obj, *args, **kwargs):
    # Stores a BLender-object as a .csv-file.
    address  = kwargs.get('address',  None)
    if address == None:
        address = obj.name


    with open(filepath, 'a') as file:
        bpy.ops.object.select_all(action='DESELECT')
        obj.rotation_mode = 'QUATERNION'
        position = np.array(obj.location)
        attitude = obj.rotation_quaternion.to_matrix()
        attitude.transpose()
        attitude = np.array(attitude)
        file.write(address+",,,,,,\n")
        file.write(address+".position,,,,,\n")
        file.write(mlb.matrix2csvtext(position)+",,,,,,\n")
        file.write(address+".attitude,,,,,\n")
        file.write(mlb.matrix2csvtext(attitude)+",,,,,,\n")

        if obj.type == 'MESH':
            file.write(address +'.mesh,,,,,\n')
            file.write(obj.name+'.stl,,,,,,\n')
            
            
            stl_filename       = obj.name+".stl"
            csv_filename       = filepath   .split('\\')[-1]
            stl_filepath       = filepath.replace(csv_filename, stl_filename)
            
            has_parent = not obj.parent == None
            
            # Un-parenting and saving logic
            if has_parent:
                parent     = obj.parent
                obj.parent = None

            obj.rotation_mode            = 'QUATERNION'
            original_rotation_quaternion = obj.rotation_quaternion.copy()
            original_location            = obj.location.copy()
            obj.rotation_quaternion      = mt.Quaternion((1,0,0,0))
            obj.location                 = mt.Vector    ((0,0,0))
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            bpy.ops.export_mesh.stl(filepath=stl_filepath, use_selection=True, global_scale = 1)
            obj.select_set(False)
            obj.rotation_mode       = 'QUATERNION'
            obj.rotation_quaternion = original_rotation_quaternion
            obj.location            = original_location

            if has_parent:
                obj.parent              = parent

        
    for child in obj.children:
        mlb.obj2csv(filepath, child, address = address + '.' + child.name)
            