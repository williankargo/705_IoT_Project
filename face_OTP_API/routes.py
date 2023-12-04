from flask import Blueprint, request, jsonify, g
import logging
import service
import hashlib
from database import DatabaseManager
import tempfile

blueprint = Blueprint("routes", __name__)
db_manager = DatabaseManager()


@blueprint.before_request
def before_request():
    g.db_manager = db_manager


@blueprint.teardown_request
def teardown_request(exception=None):
    if hasattr(g, "db_manager"):
        # Close the database connection at the end of the request
        del g.db_manager


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

        # img1_data = "./OwnerData/pinkuan.jpg"  # owner's image path
        users_data = db_manager.get_all_users()  # owners's image
        # print(
        #     "users_data: ", users_data[0][1]
        # )  # users_data[0][0]: blobData, users_data[0][1]: phoneNumber

        """
        Turn image_data to hash value
        """
        # with open(img1_data, "rb") as img_file:
        #     img1_data_base64 = img_file.read()
        # hash_obj = hashlib.sha256()
        # hash_obj.update(img1_data_base64)
        # hash_str = hash_obj.hexdigest()
        # img1_data_hash = hash_str  # TODO: you guys can use this as a key to sort the DB
        # logging.warn("img1_data_hash: %s ", img1_data_hash)

        model_name = input_args.get("model_name", "Facenet")
        detector_backend = input_args.get("detector_backend", "opencv")
        enforce_detection = input_args.get("enforce_detection", True)
        distance_metric = input_args.get("distance_metric", "cosine")
        align = input_args.get("align", True)

        for picture, phone in users_data:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_img:
                temp_img.write(picture)
                temp_img_path = temp_img.name
            verification = service.verify(
                img1_path=temp_img_path,
                img2_path=img2_data,
                model_name=model_name,
                detector_backend=detector_backend,
                distance_metric=distance_metric,
                align=align,
                enforce_detection=enforce_detection,
            )

            verification["verified"] = str(verification["verified"])
            if verification["verified"] == "True":
                return jsonify(verification)

        return jsonify(verification)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return (
            jsonify({"error": str(e)}),
            400,
        )
