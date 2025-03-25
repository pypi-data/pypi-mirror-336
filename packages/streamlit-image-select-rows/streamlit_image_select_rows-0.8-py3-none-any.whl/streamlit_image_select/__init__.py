import base64
import io
import os
from pathlib import Path

import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from typing import List, Dict, Union, Optional

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "image_select", url="http://localhost:3001"
    )
else:
    path = (Path(__file__).parent / "frontend" / "build").resolve()
    _component_func = components.declare_component("image_select", path=path)


@st.cache_data
def _encode_file(img):
    with open(img, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/jpeg;base64, {encoded}"


@st.cache_data
def _encode_numpy(img):
    pil_img = Image.fromarray(img)
    buffer = io.BytesIO()
    pil_img.save(buffer, format="JPEG")
    encoded = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/jpeg;base64, {encoded}"

def image_select(
    label: str,
    images: Optional[List[Union[str, np.ndarray, Image.Image]]] = None,
    images_rows: Optional[List[Dict[str, Union[List[str], List[np.ndarray], List[Image.Image], List[str]]]]] = None,
    captions: Optional[List[str]] = None,
    index: Union[int, Dict[str, int]] = 0,
    *,
    use_container_width: bool = True,
    return_value: str = "original",
    disabled: bool = False,
    key: Optional[str] = None,
    custom_css: Optional[str] = None,
    align: str = "center",
):
    """Shows several images and returns the image selected by the user.

    Args:
        label (str): The label shown above the images. [HTML code will be rendered]
        images (list): The images to show. Allowed image formats are paths to local
            files, URLs, PIL images, and numpy arrays.
        images_rows (list): Alternative to `images`. A list of dictionaries. Each 
            dictionary entry has a key "images" with a list of images. Each dictionary
            will be plotted in its own row. Each image dictionary can also have the key "captions" for captions. Additionally, the key "tooltip" can be used to add a tooltip to the image.
        captions (list of str): The captions to show below the images. Defaults to
            None, in which case no captions are shown. [HTML code will be rendered]. Only used when images_rows is None. Otherwise, the captions are taken from the images_rows key "caption".
        index (int or dict, optional): The index of the image that is selected by default.
            Defaults to 0. Should be a dictionary when `images_rows` is used.
        use_container_width (bool, optional): Whether to stretch the images to the
            width of the surrounding container. Defaults to True.
        return_value ("original" or "index", optional): Whether to return the
            original object passed into `images` or the index of the selected image.
            Defaults to "original".
        disabled (bool, optional): Whether the component is disabled. Defaults to False.
        key (str, optional): The key of the component. Defaults to None.
        custom_css (str, optional): Custom CSS to apply to the component. Defaults to None.

    Returns:
        (any): The image selected by the user (same object and type as passed to
            `images`).
    """

    # Check for valid inputs
    if not images and not images_rows:
        raise ValueError("Either `images` or `images_rows` must be provided, but neither was found.")

    if images and images_rows:
        raise ValueError("Only one of `images` or `images_rows` can be provided, not both.")

    if images_rows:
        if not isinstance(index, dict):
            raise ValueError("`index` must be a dictionary when `images_rows` is passed. Example dict: {'rowIndex': 0, 'index': 0}")
        if "rowIndex" not in index or "index" not in index:
            raise ValueError("`index` dictionary must contain 'rowIndex' and 'index' keys.")
        if not (isinstance(index["rowIndex"], int) and isinstance(index["index"], int)):
            raise ValueError("`index['rowIndex']` and `index['index']` must both be integers.")

    if images:
        if not isinstance(images, list) or not all(isinstance(img, (str, np.ndarray, Image.Image)) for img in images):
            raise TypeError("`images` must be a list of strings (paths/URLs), numpy arrays, or PIL Images.")
        # if index and not isinstance(index, int):
        #     raise TypeError("`index` must be an integer when `images` is provided.")
        # if index < 0 or index >= len(images):
        #     raise ValueError(f"`index` must be between 0 and {len(images) - 1}, but it is {index}.")

    if captions:
        if images and len(captions) != len(images):
            raise ValueError("The number of `captions` must match the number of `images` when `images` is provided.")
        if images_rows:
            for row in images_rows:
                if "captions" in row and len(row["captions"]) != len(row["images"]):
                    raise ValueError("Each row's `captions` list must match the length of its `images` list.")

    # Encode local images/numpy arrays/PIL images to base64.
    encoded_images = []
    
    if images:
        row = {"images": [], "captions": []}
        for i, img in enumerate(images):
            if isinstance(img, (np.ndarray, Image.Image)):  # numpy array or PIL image
                row["images"].append(_encode_numpy(np.asarray(img)))
            elif os.path.exists(img):  # local file
                row["images"].append(_encode_file(img))
            else:  # url, use directly
                row["images"].append(img)
            
            if captions:
                if captions[i]:
                    row["captions"].append(captions[i])
        encoded_images.append(row)
        if index:
            if isinstance(index,dict) == False:
                index = {"rowIndex": 0, "index": index}
    
    if images_rows:
        for image_row in images_rows:
            row = {"images": [], "captions": [], "tooltip": [], "vertical_label": ""}
            for i,img in enumerate(image_row["images"]):
                if isinstance(img, (np.ndarray, Image.Image)):  # numpy array or PIL image
                    row["images"].append(_encode_numpy(np.asarray(img)))
                elif os.path.exists(img):  # local file
                    row["images"].append(_encode_file(img))
                else:  # url, use directly
                    row["images"].append(img)
                
                if "captions" in image_row:
                    if image_row["captions"]:
                        if image_row["captions"][i]:
                            row["captions"].append(image_row["captions"][i])
                        else:
                            row["captions"].append("")
                    else:
                        row["captions"].append("")
                else:
                    row["captions"].append("")
                            
                if "tooltip" in image_row:
                    if image_row["tooltip"]:
                        if image_row["tooltip"][i]:
                            row["tooltip"].append(image_row["tooltip"][i])
                        else:
                            row["tooltip"].append("")
                        
                    else:
                        row["tooltip"].append("")
                else:
                    row["tooltip"].append("")
        
        
            if "vertical_label" in image_row:
                row["vertical_label"] = image_row["vertical_label"]
            encoded_images.append(row)
    # Pass everything to the frontend.
    component_value = _component_func(
        label=label,
        images_rows=encoded_images,
        captions=captions,
        index=index,
        use_container_width=use_container_width,
        key=key,
        default=index,
        disabled=disabled,
        defaultValue=index,
        custom_css=custom_css,
        align=align,
    )

    # If the component is disabled, return the default (initial) value.
    if disabled:
        component_value = index
        
    # The frontend component returns the index of the selected image but we want to
    # return the actual image.
    if component_value is None:
        return None

    if return_value == "original":
        if images:
            return images[component_value["index"]]
        else:
            # Flatten the list of image rows to return the correct image.
            return images_rows[component_value["rowIndex"]]["images"][component_value["index"]]
    elif return_value == "index":
        return component_value
    else:
        raise ValueError(
            "`return_value` must be either 'original' or 'index' "
            f"but is '{return_value}'."
        )
