#! /usr/bin/env python3
import pathlib
import json
from PIL import Image, ImageDraw

# Create coarse semantic segmentation mask
# of combined classes
def createMask(json_filepath, row, col):
    
    # Initializing colormap
    coarseSegColorMap = Image.new(mode="RGB", size=(row, col))
    draw = ImageDraw.Draw(coarseSegColorMap) 

    # Colourmaps for classes
    sky_colour = (61, 184, 255)
    background_objects_colour = (61, 93, 255)
    vulnerable_living_colour = (255, 61, 61)
    small_mobile_vehicle_colour = (255, 190, 61)
    large_mobile_vehicle_colour = (255, 116, 61)
    road_edge_delimiter_colour = (216, 255, 61)
    road_colour = (0, 255, 220)

    
    # Open json file and get object labels and polygon points
    with open(json_filepath, 'r') as file: 
        annotations = json.load(file)
        
        for obj in annotations['objects']:
            
            label = obj['label']
            polygon = obj['polygon']
            coordinates = []

            for i in range(0, len(polygon)):
                    polygon[i][0] = int(polygon[i][0])
                    polygon[i][1] = int(polygon[i][1])
                    coordinates.append(int(polygon[i][0]))
                    coordinates.append(int(polygon[i][1]))

            # If there is a valid label
            if(len(polygon) > 1):
                # SKY
                if label == 'sky':
                    draw.polygon(coordinates, fill = sky_colour, outline = sky_colour) 

                # BACKGROUND OBJECTS
                elif label == 'billboard' or label == 'traffic sign' or label == 'traffic light' or \
                    label == 'pole' or label == 'obs-str-bar-fallback' or label == 'building' or \
                    label == 'bridge' or label == 'vegetation' or label == 'fallback background' or \
                    label == 'parking' or label == 'drivable-fallback' or label == 'sidewalk' or \
                    label == 'non-drivable fallback':
                    draw.polygon(coordinates, fill = background_objects_colour, outline = background_objects_colour) 

                # ROAD
                elif label == 'road':
                    draw.polygon(coordinates, fill = road_colour, outline = road_colour) 

                # ROAD EDGE DELIMITER
                elif label == 'curb' or label == 'wall' or label == 'fence' or label == 'guard rail':
                    draw.polygon(coordinates, fill = road_edge_delimiter_colour, outline = road_edge_delimiter_colour) 
                
                # VULNERABLE LIVING
                elif label == 'person' or label == 'animal':
                    draw.polygon(coordinates, fill = vulnerable_living_colour, outline = vulnerable_living_colour) 

                # SMALL MOBILE VEHICLE
                elif label == 'rider' or label == 'motorcycle' or label == 'bicycle':
                    draw.polygon(coordinates, fill = small_mobile_vehicle_colour, outline = small_mobile_vehicle_colour) 

                # LARGE MOBILE VEHICLE
                elif label == 'autorickshaw' or label == 'car' or label == 'truck' or label == 'bus' or \
                    label == 'caravan' or label == 'vehicle fallback':
                    draw.polygon(coordinates, fill = large_mobile_vehicle_colour, outline = large_mobile_vehicle_colour) 

    return coarseSegColorMap

# Reading dataset labels and images and sorting returned list in alphabetical order
labels = sorted([f for f in pathlib.Path('/home/zain/Autoware/semantic_segmentation/training_data/IDDAW/ground_truth/').glob(("*/*"))])
images = sorted([f for f in pathlib.Path('/home/zain/Autoware/semantic_segmentation/training_data/IDDAW/images/').glob("*/*")])

# Paths to save training data with new coarse segmentation masks
labels_save_path = '/home/zain/Autoware/semantic_segmentation/training_data/Coarse_Seg/IDDAW/gt_masks/'
images_save_path = '/home/zain/Autoware/semantic_segmentation/training_data/Coarse_Seg/IDDAW/images/'

# Looping through data
for index in range(0, len(labels)):

    # Open images and json files
    image = Image.open(str(images[index]))
    json_filepath = str(labels[index])

    # Get image size
    row, col = image.size

    # Create new Coarse Segmentation mask
    coarseSegColorMap = createMask(json_filepath, row, col)

    # Save images
    image.save(images_save_path + str(index) + ".png","PNG")
    coarseSegColorMap.save(labels_save_path + str(index) + ".png","PNG")

    print(index)

print('--- COMPLETE ---')                