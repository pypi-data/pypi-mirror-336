import numpy as np
import mathutils as mt
import MatlabBlenderIO as mlb
import csv, bpy


def csv2obj(filepath, *args, **kwargs):
    # Takes in the filepath to an object stored as a .csv file, and imports it into Blender.
    replace = kwargs.get('replace', None)
    if replace == None: replace = True

    with open(filepath, mode='r') as file:
        data = file.read()
    
    data = data.replace("\n", "")
    data = data.replace("\n", "")
    data = data.split(",,,,,,")
    data = list(map(lambda element: element.split(",,,,,"), data))
    data = [list(filter(lambda item: item != '', element )) for element in data if type(element) is list]
    data = data[:-1]
    
    
    # Loop through and create all the bodies:
    for element in data:
        is_body = len(element)==1
        if not is_body:
            is_mesh = "mesh" == element[0].split(".")[-1]
        else:
            is_mesh = False

        if is_body:
            body_name      = element[0].split(".")[-1]

            if body_name not in bpy.data.objects.keys():
                bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
                body           = bpy.data.objects['Empty']
                body.name      = body_name

        if is_mesh:
            mesh_name   = element[0].split(".")[-2]
            if mesh_name not in bpy.data.objects.keys():
                new_mesh = True
            elif bpy.data.objects[mesh_name].type == 'EMPTY':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects[mesh_name].select_set(True)
                bpy.ops.object.delete()
                bpy.ops.object.select_all(action='DESELECT')
                new_mesh = True
            else:
                new_mesh = False

            if new_mesh:
                stl_filename        = element[1].split('\\')[-1]
                csv_filename        = filepath  .split('\\')[-1]
                stl_filepath        = filepath  .replace(csv_filename, stl_filename)
                import_name         = stl_filename.replace(".stl", "")
                update_original     = False

                if import_name in bpy.data.objects.keys():
                    update_original = True
                    original        = bpy.data.objects[import_name]
                    original.name   = "Temp__"

                bpy.ops.import_mesh.stl(filepath = stl_filepath)
                bpy.data.objects[import_name].name = mesh_name 
                bpy.ops.object.select_all(action='DESELECT')

                if update_original:
                    original.name = import_name
    
    
    # Loop through and assign all the parent-relationships:
    for element in data:
        is_body = len(element)==1
        
        if is_body:
            address    = element[0].split(".")
            has_parent = len(address)>1
            body_name  = address[-1]
            
            if has_parent:
                parent_name = address[-2]
                bpy.data.objects[body_name].parent = bpy.data.objects[parent_name]

    
    # Loop through and assign position, rotation and mesh:
    for element in data:
        has_properties = len(element)>1
        if has_properties:
            body_name     = element[0].split(".")[-2]
            property_name = element[0].split(".")[-1]
            body          = bpy.data.objects[body_name]

            if property_name == "position":
 
                positions, position_dimensions = mlb.csvtext2matrix(element[1])

                if len(position_dimensions) > 2:
                    number_of_keyframes = positions.shape[2]
                    for keyframe in range(1,number_of_keyframes):
                        position = mt.Vector(positions[:,:,keyframe])
                        body.keyframe_insert('location', frame = keyframe)
                        body.location = position
                else:
                    position = mt.Vector(positions)
                    body.location = position
            
            if property_name == "attitude":
                body.rotation_mode = 'QUATERNION'
                attitudes, attitude_dimensions = mlb.csvtext2matrix(element[1])

                if len(attitude_dimensions) > 2:
                    number_of_keyframes = attitudes.shape[2]
                    for keyframe in range(1,number_of_keyframes):
                        attitude = attitudes[:,:,keyframe]
                        attitude_quaternion = mt.Matrix(attitude).to_quaternion()
                        body.keyframe_insert('rotation_quaternion', frame = keyframe)
                        body.rotation_quaternion = attitude_quaternion
                else:
                    attitude_quaternion = mt.Matrix(attitudes).to_quaternion()
                    body.rotation_quaternion = attitude_quaternion
                    