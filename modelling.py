import numpy as np


# Tells us whether to set the origin of a texture to the "from" or the "to" coordinate
origin_map = { #    [x, y, z]
    "down"  :       [0, 0, 1],
    "up"    :       [0, 1, 0],
    "north" :       [1, 1, 0],
    "south" :       [0, 1, 1],
    "west"  :       [0, 1, 0],
    "east"  :       [1, 1, 1]
}

# Tells us whether a voxel should be translated based on the x coordinate in the texture
translate_x_map = { # [x, y, z]
    "down"  :         [1, 0, 0],
    "up"    :         [1, 0, 0],
    "north" :         [1, 0, 0],
    "south" :         [1, 0, 0],
    "west"  :         [0, 0, 1],
    "east"  :         [0, 0, 1]
}

# Tells us whether a voxel should be translated based on the y coordinate in the texture
translate_y_map = { # [x, y, z]
    "down"  :         [0, 0, 1],
    "up"    :         [0, 0, 1],
    "north" :         [0, 1, 0],
    "south" :         [0, 1, 0],
    "west"  :         [0, 1, 0],
    "east"  :         [0, 1, 0]
}

def write_face(face, uv, uv_rotation, origin_from, origin_to, img_data, voxel_data):

    # img_data = np.rot90(img_data, rotation // 90)

    from viewing import view_model
    for i in range(uv_rotation // 90):
        print(uv)
        # return

        uv = [uv[3]] + uv[:3]
        # xfrom ->yfrom,
        #  yfrom -> xto
        # xto ->yto
        # yto - xfrom


    x_origin = (origin_to[0] - 1) if origin_map[face][0] else origin_from[0]
    y_origin = (origin_to[1] - 1) if origin_map[face][1] else origin_from[1]
    z_origin = (origin_to[2] - 1) if origin_map[face][2] else origin_from[2]

    # print(face)
    # print("uvs:", uv[2] - uv[0], uv[3] - uv[1])

    inconsistent_texture = False

    for i in range(3):
        if (translate_x_map[face][i] + translate_y_map[face][i]) * (origin_to[i] - origin_from[i]) != translate_x_map[face][i] * (uv[2] - uv[0]) + translate_y_map[face][i] * (uv[3] - uv[1]):
            print("WARNING: Texture scaling voxel inconsistent, voxel model will be incorrect")
            inconsistent_texture = True


    for y in range(uv[1], uv[3]):  # these ranges ignore mirrored textures which needs FIXING
        for x in range(uv[0], uv[2]):
            try:

                voxel_data[
                    z_origin - (origin_map[face][2] * 2 - 1) * ((translate_x_map[face][2] * (x - uv[0])) + (translate_y_map[face][2] * (y - uv[1]))),
                    y_origin - (origin_map[face][1] * 2 - 1) * ((translate_x_map[face][1] * (x - uv[0])) + (translate_y_map[face][1] * (y - uv[1]))),
                    x_origin - (origin_map[face][0] * 2 - 1) * ((translate_x_map[face][0] * (x - uv[0])) + (translate_y_map[face][0] * (y - uv[1])))
                ] = [255, 0, 0, 255] if inconsistent_texture else img_data[y, x]
            except IndexError as error:
                print(f"WARNING: Voxel out-of-bounds: {error}")

def read_face(face, uv, uv_rotation, origin_from, origin_to, voxel_data):

    x_origin = (origin_to[0] - 1) if origin_map[face][0] else origin_from[0]
    y_origin = (origin_to[1] - 1) if origin_map[face][1] else origin_from[1]
    z_origin = (origin_to[2] - 1) if origin_map[face][2] else origin_from[2]
    #
    # for i in range(3):
    #     if (translate_x_map[face][i] + translate_y_map[face][i]) * (origin_to[i] - origin_from[i]) != translate_x_map[face][i] * (uv[2] - uv[0]) + translate_y_map[face][i] * (uv[3] - uv[1]):
    #         print("WARNING: Texture scaling voxel inconsistent, voxel model will be incorrect")

    img_data = np.zeros([16, 16, 4], dtype=np.uint8)

    img_data[:, :, :] = 255

    for y in range(uv[1], uv[3]):  # these ranges ignore mirrored textures which needs FIXING
        for x in range(uv[0], uv[2]):
            try:

                img_data[y, x] = voxel_data[
                    z_origin - (origin_map[face][2] * 2 - 1) * ((translate_x_map[face][2] * (x - uv[0])) + (translate_y_map[face][2] * (y - uv[1]))),
                    y_origin - (origin_map[face][1] * 2 - 1) * ((translate_x_map[face][1] * (x - uv[0])) + (translate_y_map[face][1] * (y - uv[1]))),
                    x_origin - (origin_map[face][0] * 2 - 1) * ((translate_x_map[face][0] * (x - uv[0])) + (translate_y_map[face][0] * (y - uv[1])))
                ]
            except IndexError as error:
                print(f"WARNING: Voxel out-of-bounds: {error}")

    return img_data
