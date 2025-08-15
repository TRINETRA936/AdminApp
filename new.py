from flask import Flask, jsonify, request, Response, send_from_directory
from flask_cors import CORS
from products import products
import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Route to get all products
@app.route("/products", methods=["GET"])
def get_products():
    product_list = []
    for product in products:
        product_data = product.copy()
        product_data["image_url"] = f"http://192.168.0.100:5000/static/images/{product['image']}"
        if "video" in product and product["video"]:
            product_data["video_url"] = f"http://192.168.0.100:5000/static/videos/{product['video']}"
        else:
            product_data["video_url"] = ""
        product_list.append(product_data)
    return jsonify(product_list)

# Route to serve images
@app.route("/static/images/<filename>")
def get_image(filename):
    return send_from_directory("static/images", filename)

# Route to serve videos with range support
@app.route("/static/videos/<filename>")
def get_video(filename):
    path = os.path.join("static/videos", filename)
    range_header = request.headers.get('Range', None)
    if not os.path.exists(path):
        return "Video not found", 404

    file_size = os.path.getsize(path)
    start, end = 0, file_size - 1

    if range_header:
        range_match = range_header.replace("bytes=", "").split("-")
        if range_match[0]:
            start = int(range_match[0])
        if len(range_match) > 1 and range_match[1]:
            end = int(range_match[1])
    length = end - start + 1

    with open(path, "rb") as f:
        f.seek(start)
        data = f.read(length)

    rv = Response(data, 206, mimetype="video/mp4", content_type="video/mp4")
    rv.headers.add("Content-Range", f"bytes {start}-{end}/{file_size}")
    rv.headers.add("Accept-Ranges", "bytes")
    rv.headers.add("Content-Length", str(length))
    return rv

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

