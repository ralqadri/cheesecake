import os, time, atexit
from flask import Flask, request, render_template, send_from_directory, after_this_request
from pytube import YouTube
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        videolink = request.form['link']
        videodirectory = './downloads'
        videofiletitle = download_video(videolink)
        videofilepath = os.path.join(videodirectory, videofiletitle)

        return send_from_directory(directory=videodirectory, path=videofiletitle, as_attachment=True)
    else:
        return render_template('index.html')
    
def download_video(videolink):
    yt = YouTube(videolink)
    yt = yt.streams.get_highest_resolution()
    try:
        yt.download('./downloads')
    except:
        print('🚨 error! video is not available to download!')

    print('')
    print('📲 downloaded video: ' + yt.title + ' - ' + videolink)
    print('🚓 yt.get_file_path: ' + yt.get_file_path())
    print('')
    
    videopath = str(yt.title) + '.mp4'

    return videopath

def print_every_5_mins():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

scheduler = BackgroundScheduler()
scheduler.add_job(print_every_5_mins, 'interval', minutes=5)
scheduler.start()

# shut down the background scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())