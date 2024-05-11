import numpy as np
from skimage import io
from sklearn.cluster import KMeans
import numpy.typing as npt


def create_palette(image: npt.NDArray, k: int) -> npt.NDArray:
    """Creates a palette of k colors that best represents the image"""
    return KMeans(n_clusters=k, max_iter=1, n_init='auto').fit(np.reshape(image, (-1, 3))).cluster_centers_


def find_closest(value: npt.NDArray, palette: npt.NDArray) -> npt.NDArray:
    """For a given color, finds the closest color to it in the palette by
    Euclidean distance"""
    distances = np.sum((palette - value) ** 2, axis=1)
    min_idx = np.argmin(distances)
    return palette[min_idx]


def apply_palette(image: npt.NDArray, palette: npt.NDArray) -> npt.NDArray:
    """Takes a color palette and an image and replaces every pixel in the image
    with a color in the palette that is the closest by Euclidean distance to the original color"""
    new_image = np.reshape(image, (-1, 3))[:, np.newaxis, :]
    distances = np.sum((new_image - palette) ** 2, axis=2)
    min_indices = np.argmin(distances, axis=1)
    new_image = palette[min_indices]
    return new_image.reshape(image.shape)


def format_image(img_link: str) -> npt.NDArray | None:
    """Takes in image and returns matrix representing it with colors from 0 to 1"""
    try:
        io.imread(img_link)
    except BaseException as e:
        print(f"{e}\nFailed to find file")
        return None
    else:
        return io.imread(img_link) / 255


def pixelize_image(image: npt.NDArray, pixel_size: int) -> npt.NDArray:
    """Takes in an image and returns an image of the same size
        but with larger 'pixels' """
    height, width, _ = np.shape(image)
    new_height = height // pixel_size
    new_width = width // pixel_size
    # Sum up the pixel value to corresponding map
    reshaped_image = (image[:new_height * pixel_size, :new_width * pixel_size]
                      .reshape(new_height, pixel_size, new_width, pixel_size, 3))
    pixel_map = reshaped_image.sum(axis=(1, 3))
    # Average values
    pixel_map /= pixel_size ** 2
    # update values in image
    new_image_indices_i = np.arange(height) // pixel_size
    new_image_indices_j = np.arange(width) // pixel_size

    # Use indices to create the new_image array
    new_image = pixel_map[new_image_indices_i[:, np.newaxis], new_image_indices_j]
    return new_image


def write_image(image: npt.NDArray, path: str) -> None:
    """Save an image to the specified path"""
    image *= 255
    image = np.clip(image, 0, 255).astype(np.uint8)
    # print(np.shape(image))
    io.imsave(path, image)


if __name__ == "__main__":
    im = input("Enter image to pixelize (do not include path): ")
    im_link = f"./photos/{im}"
    img = format_image(im_link)
    if img is None:
        pass
    else:
        # im = "mountain_sunset"
        # pixel_group = 4
        # palette_size = 60
        # im_link = f"./photos/{im}.jpg"
        pixel_group = ""
        while not pixel_group.isdigit():
            pixel_group = input("What size pixel groups (1-10)? ")
            if pixel_group.isdigit() and 10 > int(pixel_group) > 0:
                pixel_group = int(pixel_group)
                break
            pixel_group = ""

        palette_size = ""
        while not pixel_group.isdigit():
            palette_size = input("How many colors to use? ")
            if palette_size.isdigit() and int(palette_size) > 0:
                palette_size = int(palette_size)
                break
            palette_size = ""

        color_palette = create_palette(img, palette_size)
        print("Created palette")
        pixelated_image = pixelize_image(img, pixel_group)
        print("Pixelated")
        final_image = apply_palette(pixelated_image, color_palette)
        print("Applied")
        to_write = f"./pixelated_photos/{im}{pixel_group}px{palette_size}pz.jpg"
        write_image(final_image, to_write)
