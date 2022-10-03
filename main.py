#!/usr/bin/env python3
import random
import sys

import numpy as np
from PIL import Image

from modelling import write_face, read_face
from viewing import view_model, view_image
from file_manager import load_json, save_json


def get_parent(namespace, model):
    if "parent" in model:
        return split_namespace_pathid(namespace, model["parent"])[1]
    else:
        return None

def split_namespace_pathid(namespace, namespace_pathid):
    try:
        namespace, pathid = namespace_pathid.split(":")
        return namespace, pathid
    except ValueError:
        return namespace, namespace_pathid
    except AttributeError:
        return namespace, None

def recursive_compile_list(list1, list2):  # list1 contents take priority
    for i, item in enumerate(list2):
        if list1[i] is None:
            print(f"INFO: Adding {item} at index {i} to list {list1} from list {list2}")
            list1[i + 1] = item
        elif list1[i] == list2[i]:
            print(f"INFO: Ignoring duplicate {item} list addition to list {list1} from list {list2}")
        else:
            print(f"INFO: Replacing item {list1[i]} with {list2[i]} at index {i} in list {list1} from list {list2}")
            # raise ValueError("Unexpected item was received: recieved")
        return list1

def recursive_compile_dict(dict1, dict2):  # dict1 contents take priority
    for key, dict2value in dict2.items():
        if key not in dict1:
            dict1[key] = dict2value
        elif type(dict1[key]) == list and type(dict2value) == list:
            dict1[key] = recursive_compile_list(dict1[key], dict2value)
        elif type(dict1[key]) == dict and type(dict2value) == dict:
            dict1[key] = recursive_compile_dict(dict1[key], dict2value)
        elif type(dict1[key]) == str and type(dict2value) == str:
            print(f"INFO: Ignoring duplicate key assignment '{key}' to '{dict2value}' as it is already assigned to '{dict1[key]}'")
        else:
            raise ValueError(f"ERROR: Unexpected value of type {type(dict2value)} ({dict2value}) was received")
    return dict1

def get_texture(alias, textures):
    while alias[0] == '#':
        try:
            alias = textures[alias[1:]]
        except KeyError:
            return
    return alias


config = load_json("config.json")
load_pack = config["load_pack"]
save_pack = config["save_pack"]
namespace = config["namespace"]

if not bool(blocks := sys.argv[1:]):
    blocks = ["block/comparator_on", "block/repeater_1tick_on", "block/stone", "block/grass_block"]


for block in blocks:
    current_model = load_json(f"{load_pack}/assets/{namespace}/models/{block}.json")
    full_model = current_model

    while parent := get_parent(namespace, current_model):
        current_model = load_json(f"{load_pack}/assets/{namespace}/models/{parent}.json")
        full_model = recursive_compile_dict(full_model, current_model)

    save_json("json.json", full_model)

    voxel_count = 16
    voxel_data = np.zeros([voxel_count, voxel_count, voxel_count, 4], dtype=np.uint8)  # TODO: make voxel_count + 2 not distort model

    for element in full_model["elements"]:

        # voxel_data[element["from"][2]:element["to"][2], element["from"][1]:element["to"][1], element["from"][0]:element["to"][0]] = [random.randint(0, 255) for _ in range(3)] + [255]

        for face, face_data in element["faces"].items():

            texture = get_texture(face_data["texture"], full_model["textures"])
            namespace, pathid = split_namespace_pathid("minecraft", texture)

            # if texture is not None:
                # img = Image.open("{}/assets/{}/textures/{}.png".format(load_pack, namespace, pathid))
            # else:
                # img = Image.open("missing.png")
            img = Image.open(f"{load_pack}/assets/minecraft/textures/block/debug2.png")
            img_data = np.array(img)

            try:
                uv = face_data["uv"]
            except KeyError:
                # uv = [0, 0, 0, 0]
                uv = [0, 0, voxel_count, voxel_count]

            try:
                rotation = face_data["rotation"]
            except KeyError:
                rotation = 0

            write_face(face, uv, rotation, element["from"], element["to"], img_data, voxel_data)

    new_model = full_model#load_json(f"{load_pack}/assets/{namespace}/models/{block}.json")

    for i_element, element in enumerate(full_model["elements"]):
        for face, face_data in element["faces"].items():

            img_data = read_face(face, uv, rotation, element["from"], element["to"], voxel_data)
            print(img_data)
            img = Image.fromarray(img_data)

            texture = get_texture(face_data["texture"], full_model["textures"])
            namespace, pathid = split_namespace_pathid("minecraft", texture)
            img.save(f"{save_pack}/assets/{namespace}/textures/{block}_{i_element}_{face}.png")

            new_model["textures"][f"{block}_{i_element}_{face}"] = f"{block}_{i_element}_{face}"
            new_model["elements"][i_element]["faces"][face]["texture"] = f"#{block}_{i_element}_{face}"

            save_json(f"{save_pack}/assets/{namespace}/models/{block}.json", new_model)

    # view_model(voxel_data, point_size=150)



