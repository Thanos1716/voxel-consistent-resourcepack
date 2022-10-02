import matplotlib.pyplot as plt
import numpy as np

def view_model(model, testrgb=False, testaxes=False):
    # RGB test
    if testrgb:
        for x in range(model.shape[2]):
            for y in range(model.shape[1]):
                for z in range(model.shape[0]):
                    model[z, y, x] = [256 * x / 16, 256 * y / 16, 256 * z / 16, 100]

    # Axes viewer
    if testaxes:
        model[0 , 0, :] = [255,   0,   0, 255]
        model[0 , :, 0] = [0,   255,   0, 255]
        model[:,  0, 0] = [0,     0, 255, 255]
        model[0,  0, 0] = [0,     0,   0, 255]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(elev=30, azim=-90, roll=0)
    # ax.set_aspect("equal")
    z, x, y = np.meshgrid(*list(map(range, model.shape[:3])))
    print(np.prod(list(model.shape)[:3]))
    ax.scatter(x, y, z, c=model.reshape(np.prod(list(model.shape)[:3]), 4) / 255, s=150)# + voxel_data[x, y, z, 1] + voxel_data[x, y, z, 2]))"""alpha=(voxel_data[x, y, z, 3]), """
    # print(x, y, z)
    # print(voxel_data[x, y, z])

    plt.show()

    # plt.waitforbuttonpress(0) # this will wait for indefinite time
    plt.close(fig)

def view_image(image_data):
    img = Image.fromarray(img_data)
    img.show()
    # img.save("nuffin.png")

