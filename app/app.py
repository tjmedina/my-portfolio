from flask import Flask, Response, render_template

import time
import requests
import cv2

app = Flask(__name__)
app.config["DEBUG"] = True


cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

def gen_frames():
    while True:
        ret, frame = cap.read()
        if frame is None:
            break
        
        buffer = cv2.imencode(".jpg", frame)[1]
        
        if not ret:
            continue
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')  # concatena frame para mostrar el resultado
        time.sleep(0.05)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/data", methods=["GET"])
def data():
    data = requests.get('https://randomuser.me/api')
    return data.json()

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == ("__main__"):
    app.run(host="0.0.0.0", debug=True, port="5000")