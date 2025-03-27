from libc.stdint cimport *
cimport numpy as np
import numpy as np
cimport cython
import cython
from cython.parallel cimport prange
from libcpp.unordered_map cimport unordered_map

cdef extern from "colorcrop.hpp" nogil :
    void find_start_y(uint32_t* img, uint32_t* colors, int32_t width, int32_t height, int32_t color_length,
                  int32_t* start_y)
    void find_end_y(uint32_t* img, uint32_t* colors, int32_t width, int32_t height, int32_t color_length,
                int32_t* end_y)
    void find_start_x(uint32_t* img, uint32_t* colors, int32_t width, int32_t height, int32_t color_length,
                    int32_t* start_x)
    void find_end_x(uint32_t* img, uint32_t* colors, int32_t width, int32_t height, int32_t color_length,
                int32_t* end_x)
    void find_coord(int32_t action, uint32_t* img, uint32_t* colors, int32_t width, int32_t height, int32_t color_length,
                int32_t* coord)

cdef crop_image_right_size(object img, int32_t start_x, int32_t start_y, int32_t end_x, int32_t end_y):
    return img[start_y:end_y, start_x:end_x]


cpdef crop_image(object img, object search_for_colors, bint parallel=False):
    """
    Crops an image based on allowed colors using external C++ routines.

    This function determines the cropping boundaries of an image by searching for specified allowed colors.
    It leverages external functions from "colorcrop.hpp" to compute the starting and ending coordinates along
    both the x and y axes. The function accepts an image and an array of colors, ensures proper type and
    memory alignment, and returns the cropped image along with the crop coordinates.

    Parameters
    ----------
    img : numpy.ndarray
        The input image as a NumPy array with shape (height, width, channels). The channels must be either 3 (RGB)
        or 4 (RGBA). If the image has 3 channels, an alpha channel with full opacity (255) will be appended.
    search_for_colors : numpy.ndarray
        A 2D NumPy array where each row represents a color in RGB or RGBA format. If provided with 3 channels,
        an alpha channel with full opacity (255) is added to each color.
    parallel : bool, optional
        Flag indicating whether to use parallel processing for computing crop coordinates. If True, the function
        uses a parallel loop (with Cython's prange) to compute the boundaries. Default is False.

    Returns
    -------
    list
        A two-element list where:
          - The first element is the cropped image (NumPy array).
          - The second element is a dictionary containing the crop boundaries:
                {
                    "start_x": int,  # Starting x-coordinate
                    "end_x": int,    # Ending x-coordinate
                    "start_y": int,  # Starting y-coordinate
                    "end_y": int     # Ending y-coordinate
                }

    Raises
    ------
    ValueError
        If either the image or the search_for_colors array is empty, or if the channel configuration is not supported
        (only RGB/RGBA images are allowed).

    Notes
    -----
    - The function ensures that both input arrays are of type np.uint8 and are C-contiguous and aligned.
    - When necessary, the image and search_for_colors arrays are copied to meet these requirements.
    - If parallel processing is enabled, the crop coordinates are computed using a parallel loop with
      the external function 'find_coord'.
    - The actual cropping is performed by slicing the original image based on the computed coordinates.
    - External functions used (from "colorcrop.hpp"):
          find_start_y, find_end_y, find_start_x, find_end_x, and find_coord.
    - RGBA is faster than RGB
    """
    cdef:
        object img_original=img
        uint32_t* img32
        uint32_t* search_for_colors_32
        int32_t start_x_allowed_color
        int32_t start_y_allowed_color
        int32_t end_x_allowed_color
        int32_t end_y_allowed_color
        int32_t width, height, color_length, channels
        int32_t number_of_channels_img
        int32_t number_of_channels_search_for_colors
        int32_t para_index
        unordered_map[int32_t,int32_t] para_map = {0:-1,1:-1,2:-1,3:-1}

    if not np.any(img) or not np.any(search_for_colors):
        raise ValueError("Empty arrays not allowed")
    number_of_channels_img = img.shape[len(img.shape)-1]
    number_of_channels_search_for_colors=len(search_for_colors[0])
    if (number_of_channels_img not in [3,4] or number_of_channels_search_for_colors not in [3,4]) and (len(img.shape)!=3):
        raise ValueError("Only RGB / RGBA allowed")

    if img.dtype != np.uint8:
        img = img.astype(np.uint8)
    if search_for_colors.dtype != np.uint8:
        search_for_colors = search_for_colors.astype(np.uint8)

    if number_of_channels_img == 3:
        img = np.concatenate((img, np.full((img.shape[0], img.shape[1], 1), 255, dtype=np.uint8)), axis=2)

    if number_of_channels_search_for_colors == 3:
        search_for_colors=np.hstack([search_for_colors, np.full((search_for_colors.shape[0],1), 255, dtype=np.uint8)])

    if not search_for_colors.flags["C_CONTIGUOUS"] or not search_for_colors.flags["ALIGNED"]:
        search_for_colors=search_for_colors.copy()

    if not img.flags["C_CONTIGUOUS"] or not img.flags["ALIGNED"]:
        img=img.copy()
    height=img.shape[0]
    width=img.shape[1]
    img32 = <uint32_t*>(<size_t>(img.ctypes._arr.__array_interface__["data"][0]))
    color_length=search_for_colors.shape[0]
    search_for_colors_32 = <uint32_t*>(<size_t>(search_for_colors.ctypes._arr.__array_interface__["data"][0]))
    start_x_allowed_color = 0
    start_y_allowed_color = 0
    end_x_allowed_color = img.shape[1]
    end_y_allowed_color = img.shape[0]
    if not parallel:
        with nogil:
            find_start_y(img32,search_for_colors_32,width,height,color_length,&start_y_allowed_color)
            find_end_y(img32,search_for_colors_32,width,height,color_length,&end_y_allowed_color)
            find_start_x(img32,search_for_colors_32,width,height,color_length,&start_x_allowed_color)
            find_end_x(img32,search_for_colors_32,width,height,color_length,&end_x_allowed_color)
        return [crop_image_right_size(
                img_original,
                start_x_allowed_color,
                start_y_allowed_color,
                end_x_allowed_color,
                end_y_allowed_color,
                ),
                {
                    "start_x":start_x_allowed_color,
                    "end_x": end_x_allowed_color,
                    "start_y":start_y_allowed_color,
                    "end_y": end_y_allowed_color,
                }
            ]

    else:
        para_map[0]=start_x_allowed_color
        para_map[1]=end_x_allowed_color
        para_map[2]=start_y_allowed_color
        para_map[3]=end_y_allowed_color
        for para_index in prange(4,nogil=True,schedule="static",chunksize=1,num_threads=4):
            find_coord(para_index, img32,search_for_colors_32,width,height,color_length,&(para_map[para_index]))
        return [crop_image_right_size(
                img_original,
                para_map[0],
                para_map[2],
                para_map[1],
                para_map[3],
                ),
                {
                    "start_x":para_map[0],
                    "end_x": para_map[1],
                    "start_y":para_map[2],
                    "end_y": para_map[3],
                }
            ]

