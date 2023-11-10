from deepface import DeepFace


def verify(
    img1_path,
    img2_path,
    model_name,
    detector_backend,
    distance_metric,
    enforce_detection,
    align,
):
    obj = DeepFace.verify(
        img1_path=img1_path,
        img2_path=img2_path,
        model_name=model_name,
        detector_backend=detector_backend,
        distance_metric=distance_metric,
        align=align,
        enforce_detection=enforce_detection,
    )
    return obj
