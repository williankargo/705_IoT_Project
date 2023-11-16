from flask import Blueprint, request, jsonify
import logging
import service
import hashlib

blueprint = Blueprint("routes", __name__)


@blueprint.route("/")
def home():
    return "<h1>Hello World!</h1>"


@blueprint.route("/verify", methods=["POST"])
def verify():
    try:
        input_args = request.get_json()

        if input_args is None:
            return jsonify({"error": "empty input set passed"}), 400

        img2_data = input_args.get("img2")  # user's image string
        if img2_data is None:
            return jsonify({"error": "you must upload user picture"}), 400

        if not img2_data.startswith("data:image"):
            img2_data = f"data:image/jpeg;base64,{img2_data}"

        img1_data = "./OwnerData/pinkuan.jpg"  # owner's image path
        
        '''
        Turn image_data to hash value
        '''
        with open(img1_data, "rb") as img_file:
            img1_data_base64 = img_file.read()
        hash_obj = hashlib.sha256()
        hash_obj.update(img1_data_base64)
        hash_str = hash_obj.hexdigest()
        img1_data_hash = hash_str  # TODO: you guys can use this as a key to sort the DB
        logging.warn("img1_data_hash: %s ", img1_data_hash)

        model_name = input_args.get("model_name", "Facenet")
        detector_backend = input_args.get("detector_backend", "opencv")
        enforce_detection = input_args.get("enforce_detection", True)
        distance_metric = input_args.get("distance_metric", "cosine")
        align = input_args.get("align", True)

        verification = service.verify(
            img1_path=img1_data,
            img2_path=img2_data,
            model_name=model_name,
            detector_backend=detector_backend,
            distance_metric=distance_metric,
            align=align,
            enforce_detection=enforce_detection,
        )

        verification["verified"] = str(verification["verified"])

        return jsonify(verification)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return (
            jsonify({"error": str(e)}),
            400,
        )
