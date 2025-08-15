from flask import Flask, Response, request, send_file, send_from_directory, jsonify
import os

app = Flask(__name__)

# Folder paths
VIDEO_FOLDER = os.path.join(app.root_path, 'static', 'videos')
IMAGE_FOLDER = os.path.join(app.root_path, 'static', 'images')

# ----------------------------
# Video streaming with range support
# ----------------------------
@app.route('/video/<path:filename>')
def stream_video(filename):
    file_path = os.path.join(VIDEO_FOLDER, filename)

    if not os.path.exists(file_path):
        return "Video not found", 404

    range_header = request.headers.get('Range', None)
    if not range_header:
        return send_file(file_path)

    size = os.path.getsize(file_path)
    byte1, byte2 = 0, None

    m = range_header.replace('bytes=', '').split('-')
    if m[0]:
        byte1 = int(m[0])
    if len(m) > 1 and m[1]:
        byte2 = int(m[1])

    length = size - byte1
    if byte2 is not None:
        length = byte2 - byte1 + 1

    with open(file_path, 'rb') as f:
        f.seek(byte1)
        data = f.read(length)

    rv = Response(data, status=206, mimetype="video/mp4", direct_passthrough=True)
    rv.headers.add('Content-Range', f'bytes {byte1}-{byte1 + length - 1}/{size}')
    rv.headers.add('Accept-Ranges', 'bytes')
    return rv

# ----------------------------
# Image serving
# ----------------------------
@app.route('/image/<path:filename>')
def serve_image(filename):
    file_path = os.path.join(IMAGE_FOLDER, filename)
    if not os.path.exists(file_path):
        return "Image not found", 404
    return send_from_directory(IMAGE_FOLDER, filename)

# ----------------------------
# API to list files (optional)
# ----------------------------
@app.route('/list/videos')
def list_videos():
    files = os.listdir(VIDEO_FOLDER)
    return jsonify(files)

@app.route('/list/images')
def list_images():
    files = os.listdir(IMAGE_FOLDER)
    return jsonify(files)

# ----------------------------
# Main entry
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
