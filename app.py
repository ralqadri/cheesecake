import os, time
from flask import Flask, request, render_template, send_from_directory, current_app
from pytube import YouTube

app = Flask(__name__)

@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        videolink = request.form['link']
        videodirectory = '.\downloads'
        videofilename = download_video(videolink)
        videofilepath = os.path.join(videodirectory, videofilename)
        output_video_information(videolink, videodirectory, videofilename, videofilepath)

        videofilehandle = open(videofilepath, 'rb')
        def stream_and_remove_file():
             yield from videofilehandle
             videofilehandle.close()
             os.remove(videofilepath)

        return current_app.response_class(stream_and_remove_file(), headers={'Content-Disposition': 'attachment', 'filename': videofilename + '.mp4'})
        # return send_from_directory(directory=videodirectory, path=videofiletitle, as_attachment=True)
    else:
        return render_template('index.html')
    
def download_video(videolink):
    yt = YouTube(videolink)
    yt = yt.streams.get_highest_resolution()
    try:
        yt.download('./downloads')
    except:
        print('error!')
    # print('downloaded video: ' + yt.title + ' - ' + videolink)
    # print('yt.get_file_path: ' + yt.get_file_path())
    
    videopath = str(yt.title) + '.mp4'

    return videopath


def output_video_information(videolink, videodirectory, videofilename, videofilepath):
        print(' ' * 12)
        print('-' * 64)
        print('videolink: %s' % videolink)
        print('videofiletitle: %s' % videofilename)
        print('videofilepath: %s' % videofilepath)
        print('-' * 64)
        print(' ' * 12)