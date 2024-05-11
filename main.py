import os
import tempfile
import tensorflow as tf
from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np

model = tf.keras.models.load_model(r"models\test_cheat.h5")
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/video')
def student():
    return render_template('video.html')

@app.route('/uploadvideo', methods=['GET','POST'])
def process_video():
    if request.method == 'POST':
        if 'video' not in request.files:
            return render_template('home.html', error='No video file uploaded.')
        video_file = request.files['video']
        if video_file.filename == '':
            return render_template('home.html', error='No video file selected.')
        temp_video_file = tempfile.NamedTemporaryFile(delete=False)
        video_file.save(temp_video_file.name)
        temp_video_file.close()
        cap = cv2.VideoCapture(temp_video_file.name)

        cheat_times = []
        normal_times = []
        frame_count = 0
        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        frame_skip_interval = 5  

        while cap.isOpened():
            ret, frame = cap.read()
            
            if not ret:
                break
            
            frame_count += 1
            
            if frame_count % frame_skip_interval != 0:
                continue
            resize = tf.image.resize(frame, (256, 256))
            yhat = model.predict(np.expand_dims(resize / 255, 0))
            if yhat > 0.5:
                normal_times.append(frame_count / frame_rate)
            else:
                cheat_times.append(frame_count / frame_rate)
            
        cap.release()
        cv2.destroyAllWindows()

        cheat_seconds = list(set(int(time) for time in cheat_times))
        normal_seconds = list(set(int(time) for time in normal_times))
        if 0 in cheat_seconds:
            cheat_seconds.remove(0)
        if 0 in normal_seconds:
            normal_seconds.remove(0)
        return redirect(url_for('result', cheat_seconds=cheat_seconds,normal_seconds=normal_seconds))
    return render_template('home.html')

@app.route('/result')
def result():
    cheat_seconds=request.args.getlist('cheat_seconds', type=int)
    normal_seconds=request.args.getlist('normal_seconds', type=int)
    cheat_updated=[]
    normal_updated=[]
    for i in cheat_seconds:
        a=i//3600
        b=i//60
        c=i%60
        if a<10:
            a="0"+str(a)
        if b<10:
            b="0"+str(b)
        if c<10:
            c="0"+str(c)
        s=str(a)+":"+str(b)+":"+str(c)   
        cheat_updated.append(s)
        if i in normal_seconds:
            normal_seconds.remove(i)
    for j in normal_seconds:
        a=j//3600
        b=j//60
        c=j%60
        if a<10:
            a="0"+str(a)
        if b<10:
            b="0"+str(b)
        if c<10:
            c="0"+str(c)
        s=str(a)+":"+str(b)+":"+str(c)
        normal_updated.append(s)

    return render_template('result.html', cheat_seconds=cheat_updated,normal_seconds=normal_updated)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
