import os, json, atexit, yt_dlp
from flask import Flask, request, render_template, send_from_directory, after_this_request
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
    yt_opts = {
        'outtmpl': './downloads/%(title)s.%(ext)s',
        'format': "mp4"
    } 

    info_file = './downloads/video.info.json'

    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        # error_code = ydl.download_with_info_file(info_file)
        info = ydl.sanitize_info(ydl.extract_info(videolink, download=True))

    # if error_code:
    #     print('🚨 some videos failed to download!')
    # else:
    #     print('✅ all videos successfully downloaded!')

    return info['title'] + '.' + info['ext']


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