import os, time
from flask import Flask, request, render_template, send_from_directory, after_this_request
from pytube import YouTube

app = Flask(__name__)

@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        videolink = request.form['link']
        videodirectory = './downloads'
        videofiletitle = download_video(videolink)
        videofilepath = os.path.join(videodirectory, videofiletitle)


        @after_this_request
        def remove_video(response):
            time.sleep(1)
            while True:
                try:
                    os.remove(videofilepath)
                    break
                except Exception as e:
                    print(e)
                    time.sleep(1)
                    continue
            return response

        return send_from_directory(directory=videodirectory, path=videofiletitle, as_attachment=True)
    else:
        return render_template('index.html')
    
def download_video(videolink):
    yt = YouTube(videolink)
    yt = yt.streams.get_highest_resolution()
    try:
        yt.download('./downloads')
    except:
        print('error!')
    print('downloaded video: ' + yt.title + ' - ' + videolink)
    print('yt.get_file_path: ' + yt.get_file_path())
    
    videopath = str(yt.title) + '.mp4'

    return videopath
