import os, time, atexit
from flask import Flask, request, render_template, send_from_directory, after_this_request
from pytube import YouTube
from pytube.cli import on_progress
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
    yt = YouTube(videolink, on_progress_callback=on_progress)
    yt = yt.streams.get_highest_resolution()
    try:
        yt.download('./downloads')
        print("(:")
    except:
        print('🚨 error! video is not available to download!')

    print('')
    print('📲 downloaded video: ' + yt.title + ' - ' + videolink)
    print('🚓 yt.get_file_path: ' + yt.get_file_path())
    print('')
    
    videopath = str(yt.title) + '.mp4'

    return videopath

def clear_downloads():
    directory = "./downloads"

    print('📲 cron job clear_downloads() starting!')
    for item in os.listdir(directory):
        if item.endswith('.mp4'):
            print('🚦 cron job: found file: ' + item + '; deleting...')
            os.remove(os.path.join(directory, item))
    print('📴 cron job clear_downloads() finished!')

scheduler = BackgroundScheduler()
scheduler.add_job(clear_downloads, 'interval', minutes=2)
scheduler.start()

# shut down the background scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())