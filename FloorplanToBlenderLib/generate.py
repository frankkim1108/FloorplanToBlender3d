import cv2
import numpy as np

from . import detect
from . import IO
from . import transform

# Path
path = "Data/"

def generate_all_files(imgpath, info):
    '''
    Generate all data files
    '''
    generate_floor_file(imgpath, info)
    generate_walls_file(imgpath, info)
    #generate_windows_file(imgpath, info)
    #generate_rooms_file(imgpath, info)

def generate_rooms_file(img_path, info):
    '''
     generate rooms
    '''
    # Read floorplan image
    img = cv2.imread(img_path)

    # grayscale image
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # create verts (points 3d), points to use in mesh creations
    verts = []
    # create faces for each plane, describe order to create mesh points
    faces = []

    # Height of waLL
    height = 1

    # Scale pixel value to 3d pos
    scale = 100

    gray = detect.wall_filter(gray)

    gray = ~gray

    rooms, colored_rooms = detect.find_rooms(gray.copy())

    gray_rooms =  cv2.cvtColor(colored_rooms,cv2.COLOR_BGR2GRAY)

    # get box positions for rooms
    boxes, gray_rooms = detect.detectPreciseBoxes(gray_rooms, blank_image)

    #Create verts
    verts = transform.scale_point_to_vector(boxes, scale, height)

    # create faces
    count = 0
    for box in verts:
        faces.extend([(count)])
        count += 1

    if(info):
        print("Number of rooms detected : ", count)

    IO.save_to_file(path+"rooms_verts", verts)
    IO.save_to_file(path+"rooms_faces", faces)

def generate_windows_file(img_path, info):
    '''
     generate doors
     generate windows
    '''
    # Read floorplan image
    img = cv2.imread(img_path)

    # grayscale image
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # create verts (points 3d), points to use in mesh creations
    verts = []
    # create faces for each plane, describe order to create mesh points
    faces = []

    # Height of waLL
    height = 1

    # Scale pixel value to 3d pos
    scale = 100

    gray = detect.wall_filter(gray)

    gray = ~gray

    rooms, colored_rooms = detect.find_details(gray.copy())

    gray_rooms =  cv2.cvtColor(colored_rooms,cv2.COLOR_BGR2GRAY)

    # get box positions for rooms
    boxes, gray_rooms = detect.detectPreciseBoxes(gray_rooms, blank_image)

    windows = []
    other = []
    #do a split here, objects next to outside ground are windows, rest are doors or extra space
    for box in boxes:
        for point in box:
            '''
            if close_to_bound(point):
                for x,y,x1,y1 in box:
                    windows.append([round((x+x1)/2),round((y+y1)/2)])
            '''
            pass

    '''
    Windows
    '''
    #Create verts for door
    verts, faces, window_amount = transform.create_nx4_verts_and_faces(img=windows, height=0.25, scale=scale) # create low piece
    verts, faces, window_amount = transform.create_nx4_verts_and_faces(img=windows, height=0.25, scale=scale, ground= 0.75) # create heigher piece

    if(info):
        print("Windows created : ", window_amount)

    IO.save_to_file(path+"windows_verts", verts)
    IO.save_to_file(path+"windows_faces", faces)

def generate_windows_file(img_path, info):
    '''
     generate doors
     generate windows
    '''
    # Read floorplan image
    img = cv2.imread(img_path)

    # grayscale image
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # create verts (points 3d), points to use in mesh creations
    verts = []
    # create faces for each plane, describe order to create mesh points
    faces = []

    # Height of waLL
    height = 1

    # Scale pixel value to 3d pos
    scale = 100

    gray = detect.wall_filter(gray)

    gray = ~gray

    rooms, colored_rooms = detect.find_details(gray.copy())

    gray_rooms =  cv2.cvtColor(colored_rooms,cv2.COLOR_BGR2GRAY)

    # get box positions for rooms
    boxes, gray_rooms = detect.detectPreciseBoxes(gray_rooms, blank_image)

    doors = []

    #do a split here, objects next to outside ground are windows, rest are doors or extra space
    for box in boxes:
        if shape_of_door(point):
            #change doors to actual 2 points instead of 4
            for x,y,x1,y1 in box:
                doors.append([round((x+x1)/2),round((y+y1)/2)])

    '''
    Doors
    '''
    #Create verts for door
    verts, faces, door_amount = transform.create_nx4_verts_and_faces(doors, height, scale)

    if(info):
        print("Doors created : ", door_amount)


    IO.save_to_file(path+"doors_verts", verts)
    IO.save_to_file(path+"doors_faces", faces)


def generate_floor_file(img_path, info):
    '''
    Receive image, convert
    '''
    # Read floorplan image
    img = cv2.imread(img_path)

    # grayscale image
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # detect outer Contours (simple floor or roof solution)
    contour, img = detect.detectOuterContours(gray)

    # create verts (points 3d), points to use in mesh creations
    verts = []
    # create faces for each plane, describe order to create mesh points
    faces = []

    # Height of waLL
    height = 1

    # Scale pixel value to 3d pos
    scale = 100

    #Create verts
    verts = transform.scale_point_to_vector(contour, scale, height)

    # create faces
    count = 0
    for box in verts:
        faces.extend([(count)])
        count += 1

    if(info):
        print("Approximated apartment size : ", "uncalculated at present time")
        # TODO: calculate size

    IO.save_to_file(path+"floor_verts", verts)
    IO.save_to_file(path+"floor_faces", faces)

def generate_walls_file(img_path, info):
    '''
    generate wall data file for floorplan
    @Param img_path, path to input file
    '''
    # Read floorplan image
    img = cv2.imread(img_path)

    # grayscale image
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # create wall image (filter out small objects from image)
    wall_img = detect.wall_filter(gray)

    # detect walls
    boxes, img = detect.detectPreciseBoxes(wall_img)

    # create verts (points 3d), points to use in mesh creations
    verts = []
    # create faces for each plane, describe order to create mesh points
    faces = []

    # Height of waLL
    wall_height = 1

    # Scale pixel value to 3d pos
    scale = 100

    # Convert boxes to verts and faces
    verts, faces, wall_amount = transform.create_nx4_verts_and_faces(boxes, wall_height, scale)

    if(info):
        print("Walls created : ", wall_amount)

    # One solution to get data to blender is to write and read from file.
    IO.save_to_file(path+"wall_verts", verts)
    IO.save_to_file(path+"wall_faces", faces)