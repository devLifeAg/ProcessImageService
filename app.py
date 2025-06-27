from flask import Flask, request, jsonify
import base64
import numpy as np
import face_recognition
from io import BytesIO
from PIL import Image

app = Flask(__name__)

@app.route('/face-encode', methods=['POST'])
def face_encode():
    try:
        img = None

        # Nếu gửi file (form-data)
        if 'image' in request.files:
            file = request.files['image']
            img = Image.open(file.stream).convert('RGB')

        # Nếu gửi JSON base64
        elif request.is_json:
            data = request.get_json()
            if not data or 'image' not in data:
                return jsonify({"error": "Thiếu image base64"}), 400

            base64_data = data['image']
            img_bytes = base64.b64decode(base64_data)
            img = Image.open(BytesIO(img_bytes)).convert('RGB')

        else:
            return jsonify({"error": "Không tìm thấy file hoặc base64"}), 400

        # PIL -> numpy
        img_np = np.array(img)

        # Lấy face encodings
        face_encodings = face_recognition.face_encodings(img_np)
        if not face_encodings:
            return jsonify({"error": "Không tìm thấy khuôn mặt"}), 404

        vector = face_encodings[0]
        return jsonify({"vector": vector.tolist()})

    except Exception as e:
        return jsonify({"error": f"Lỗi xử lý: {str(e)}"}), 500

if __name__ == '__main__':
    app.run()
