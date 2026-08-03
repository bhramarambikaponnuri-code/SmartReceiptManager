import cv2
import numpy as np
import time
import streamlit as st

from ocr.preprocess import ImagePreprocessor

@st.cache_resource(show_spinner=False)
def get_reader():
    import easyocr

    return easyocr.Reader(
        ["en"],
        gpu=False,
        verbose=False
    )


def extract_text(image_path):
    """
    Performs preprocessing, rotation detection and OCR.

    Returns
    -------
    text : str
    best_image : numpy.ndarray
    best_angle : str
    best_confidence : float
    timings : dict
    """

    # ----------------------------
    # Overall Timer
    # ----------------------------

    total_start = time.perf_counter()

    # ----------------------------
    # Image Loading
    # ----------------------------

    load_start = time.perf_counter()

    original = cv2.imread(image_path)

    load_time = time.perf_counter() - load_start

    if original is None:
        raise FileNotFoundError(image_path)

    # ----------------------------
    # Image Preprocessing
    # ----------------------------

    preprocess_start = time.perf_counter()

    processed = ImagePreprocessor.preprocess(original)

    preprocess_time = time.perf_counter() - preprocess_start

    # Save processed image for debugging
    cv2.imwrite(
        "processed_preview.png",
        processed
    )

    # ----------------------------
    # OCR (0° first)
    # ----------------------------

    ocr_start = time.perf_counter()

    reader = get_reader()
    results = reader.readtext(
        processed,
        detail=1,
        paragraph=False,
        decoder="greedy"
    )

    best_text = results
    best_image = processed
    best_angle = "0°"

    if results:
        best_confidence = np.mean([r[2] for r in results])
    else:
        best_confidence = 0

    # ----------------------------
    # Try other rotations only if needed
    # ----------------------------

    if best_confidence < 0.65:

        rotations = [
            ("90°", cv2.rotate(processed, cv2.ROTATE_90_CLOCKWISE)),
            ("180°", cv2.rotate(processed, cv2.ROTATE_180)),
            ("270°", cv2.rotate(processed, cv2.ROTATE_90_COUNTERCLOCKWISE))
        ]

        for angle, img in rotations:

            results = reader.readtext(
                img,
                detail=1,
                paragraph=False,
                decoder="greedy"
            )

            confidence = (
                np.mean([r[2] for r in results])
                if results else 0
            )

            if confidence > best_confidence:

                best_confidence = confidence
                best_text = results
                best_angle = angle
                best_image = img

    ocr_time = time.perf_counter() - ocr_start

    # ----------------------------
    # Convert OCR Results to Text
    # ----------------------------

    text = ""

    for detection in best_text:
        text += detection[1] + "\n"

    # ----------------------------
    # Total Time
    # ----------------------------

    total_time = time.perf_counter() - total_start

    timings = {
        "image_load": load_time,
        "preprocessing": preprocess_time,
        "ocr": ocr_time,
        "total": total_time
    }

    # ----------------------------
    # Console Output
    # ----------------------------

    print("\n" + "=" * 50)
    print("OCR PERFORMANCE")
    print("=" * 50)
    print(f"Image Load     : {load_time:.3f} sec")
    print(f"Preprocessing  : {preprocess_time:.3f} sec")
    print(f"OCR            : {ocr_time:.3f} sec")
    print(f"Total          : {total_time:.3f} sec")
    print("=" * 50)

    return (
        text,
        best_image,
        best_angle,
        best_confidence,
        timings
    )


def choose_best_result(original_result, processed_result):
    """
    Compare OCR results and return the better one.
    """

    original_score = (
        len(original_result["texts"])
        * original_result["average_confidence"]
    )

    processed_score = (
        len(processed_result["texts"])
        * processed_result["average_confidence"]
    )

    if original_score >= processed_score:
        return original_result, "Original Image"

    return processed_result, "Processed Image"