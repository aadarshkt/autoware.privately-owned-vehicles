#! /usr/bin/env python3
import pathlib
from PIL import Image

# Create coarse semantic segmentation mask
# of combined classes
def createMask(colorMap):

    # Initializing and loading pixel data
    row, col = colorMap.size
    px = colorMap.load()
    coarseSegColorMap = Image.new(mode="RGB", size=(row, col))
    cx = coarseSegColorMap.load()

    # Colourmaps for classes
    sky_colour = (61, 184, 255)
    background_objects_colour = (61, 93, 255)
    vulnerable_living_colour = (255, 61, 61)
    small_mobile_vehicle_colour = (255, 190, 61)
    large_mobile_vehicle_colour = (255, 116, 61)
    road_edge_delimiter_colour = (216, 255, 61)
    road_colour = (0, 255, 220)

    # Extracting classes and assigning to colourmap
    for x in range(row):
        for y in range(col):

            # SKY
            if px[x, y] == 10:
                cx[x,y] = sky_colour
        
            # BACKGROUND OBJECTS
            # Building    
            elif px[x,y] == 2:
                cx[x,y] = background_objects_colour
            # Pole  
            elif px[x,y] == 5:
                cx[x,y] = background_objects_colour
            # Traffic Light
            elif px[x,y] == 6:
                cx[x,y] = background_objects_colour 
            # Traffic Sign
            elif px[x,y] == 7:
                cx[x,y] = background_objects_colour 
            # Vegetation
            elif px[x,y] == 8:
                cx[x,y] = background_objects_colour
            # Terrain
            elif px[x,y] == 9:
                cx[x,y] = background_objects_colour

            # VULNERABLE LIVING
            # Person
            elif px[x,y] == 11:
                cx[x,y] = vulnerable_living_colour

            # SMALL MOBILE VEHICLE
            # Rider
            elif px[x,y] == 12:
                cx[x,y] = small_mobile_vehicle_colour
            # Motorcylce
            elif px[x,y] == 17:
                cx[x,y] = small_mobile_vehicle_colour
            # Bicycle
            elif px[x,y] == 18:
                cx[x,y] = small_mobile_vehicle_colour

            # LARGE MOBILE VEHICLE
            # Car
            elif px[x,y] == 13:
                cx[x,y] = large_mobile_vehicle_colour
            # Truck
            elif px[x,y] == 14:
                cx[x,y] = large_mobile_vehicle_colour
            # Bus
            elif px[x,y] == 15:
                cx[x,y] = large_mobile_vehicle_colour
            # Train
            elif px[x,y] == 16:
                cx[x,y] = large_mobile_vehicle_colour
            
            # ROAD EDGE DELIMITER
            # Wall
            elif px[x,y] == 3:
                cx[x,y] = road_edge_delimiter_colour
            # Fence
            elif px[x,y] == 4:
                cx[x,y] = road_edge_delimiter_colour

            # ROAD
            elif px[x,y] == 0:
                cx[x,y] = road_colour

    return coarseSegColorMap

# Reading dataset labels and images and sorting returned list in alphabetical order
labels = sorted([f for f in pathlib.Path('/home/zain/Autoware/semantic_segmentation/training_data/BDD100K/ground_truth/labels/').glob("*.png")])
images = sorted([f for f in pathlib.Path('/home/zain/Autoware/semantic_segmentation/training_data/BDD100K/images/train/').glob("*.jpg")])
id_path = '/home/zain/Autoware/semantic_segmentation/training_data/BDD100K/labelIds/'


# Paths to save training data with new coarse segmentation masks
labels_save_path = '/home/zain/Autoware/semantic_segmentation/training_data/Coarse_Seg/BDD100K/gt_masks/'
images_save_path = '/home/zain/Autoware/semantic_segmentation/training_data/Coarse_Seg/BDD100K/images/'

# Looping through data
for index in range(0, len(labels)):
    
    id = str(labels[index])
    id = id[84:]
    id_image_path = id_path + id 
    print(id_image_path)

    # Open images and pre-existing masks
    image = Image.open(str(images[index]))
    label = Image.open(str(labels[index]))
    id_image = Image.open(id_image_path)

    # Create new Coarse Segmentation mask
    coarseSegColorMap = createMask(id_image) 

    # Save images
    image.save(images_save_path + str(index) + ".png","PNG")
    coarseSegColorMap.save(labels_save_path + str(index) + ".png","PNG")

    print(index)

print('--- COMPLETE ---')                