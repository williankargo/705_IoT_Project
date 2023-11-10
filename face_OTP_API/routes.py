from flask import Blueprint, request, jsonify
import logging
import service

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

        img1_path = "./OwnerData/pinkuan.jpg"  # owner's image path

        model_name = input_args.get("model_name", "Facenet")
        detector_backend = input_args.get("detector_backend", "opencv")
        enforce_detection = input_args.get("enforce_detection", True)
        distance_metric = input_args.get("distance_metric", "cosine")
        align = input_args.get("align", True)

        verification = service.verify(
            img1_path=img1_path,
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
            jsonify(
                {"error": str(e)}
            ),
            400,
        )
