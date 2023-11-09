from flask import Blueprint, request, jsonify
import logging
import service

blueprint = Blueprint("routes", __name__)


@blueprint.route("/")
def home():
    return "<h1>Welcome to DeepFace API!</h1>"


@blueprint.route("/represent", methods=["POST"])
def represent():
    input_args = request.get_json()

    if input_args is None:
        return {"message": "empty input set passed"}

    img_path = input_args.get("img")
    if img_path is None:
        return {"message": "you must pass img_path input"}

    model_name = input_args.get("model_name", "Facenet")
    detector_backend = input_args.get("detector_backend", "opencv")
    enforce_detection = input_args.get("enforce_detection", True)
    align = input_args.get("align", True)

    obj = service.represent(
        img_path=img_path,
        model_name=model_name,
        detector_backend=detector_backend,
        enforce_detection=enforce_detection,
        align=align,
    )

    return obj


# We mainly use API in our IoT project
@blueprint.route("/verify", methods=["POST"])
def verify():
    logging.debug("verify")
    input_args = request.get_json()

    logging.debug("inputs_args: ", input_args)

    if input_args is None:
        return {"message": "empty input set passed"}

    img1_path = input_args.get("img1_path")
    img2_path = input_args.get("img2_path")

    img1_path = "./OwnerData/pinkuan.jpg"  # owner
    if img1_path is None:
        return {"message": "you must upload Owener picture"}

    model_name = input_args.get("model_name", "Facenet")
    detector_backend = input_args.get("detector_backend", "opencv")
    enforce_detection = input_args.get("enforce_detection", True)
    distance_metric = input_args.get("distance_metric", "cosine")
    align = input_args.get("align", True)

    verification = service.verify(
        img1_path=img1_path,
        img2_path=img2_path,
        model_name=model_name,
        detector_backend=detector_backend,
        distance_metric=distance_metric,
        align=align,
        enforce_detection=enforce_detection,
    )

    verification["verified"] = str(verification["verified"])

    return verification
