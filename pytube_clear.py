from pytube import YouTube
from pytube import Playlist
from pytube import Channel
import urllib.request

import asyncio

import os


import youtube_dl


def stream_detection(streams, mode='best', resolution='1080p'):
    print(streams)
    if mode == 'best':
        stream = streams.filter(progressive=True, file_extension=format).order_by('resolution').desc().first()
    elif mode == 'fixed':
        stream = streams.filter(progressive=True, file_extension=format, resolution=resolution).order_by('resolution').desc().first()
    return stream


def download_video(link, **kwargs):
    print(link)
    yt = YouTube(link)
    title = yt.title
    title = title.replace('/', '_')
    author = yt.author
    author = author.replace('/', '_')
    thumbnail = yt.thumbnail_url
    print(thumbnail)
    print(author)
    print(yt)
    try:
        stream = stream_detection(yt.streams)
        print('Downloading started for {}'.format(title))
        stream.download('downloads/{}'.format(author))
        print('Downloading ended for {}'.format(title))
    except:
        print('Downloading started for {}'.format(title))
        id_a = '140'
        id_v = '136'

        #ydl_opts = {'format': '{}+{}'.format(id_v, id_a), 'outtmpl': r'downloads/{}/{}'.format(author, eval("r'{}'".format(title)))}
        ydl_opts = {}

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(
                link, download=False)
            formats = meta.get('formats', [meta])
            url_link = None
            highest = {'id':None, 'res': 0}
            exact_res_found = False

            for f in formats:
                if f['format_note'] == kwargs.get('resolution', '720p') and f['ext'] == 'mp4':
                    id_v = f['format_id']
                    exact_res_found=True
                    pass
                if f['height'] is not None:
                    if f['height'] >= highest['res'] and f['ext'] == 'mp4':
                        highest.update({'id':f['format_id'], 'res': f['height']})

                if f['ext'] == 'm4a':
                    id_a = f['format_id']
                print(f)

        if exact_res_found:
            ydl_opts = {'format': '{}+{}'.format(id_v, id_a), 'outtmpl': r'downloads/{}/{}'.format(author, eval("r'{}'".format(title)))}
        else:
            ydl_opts = {'format': '{}+{}'.format(highest['id'], id_a),
                        'outtmpl': r'downloads/{}/{}'.format(author, eval("r'{}'".format(title)))}

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        print('Downloading ended for {}'.format(title))


def downloader(url, mode='channel', **kwargs):
    #mode=['channel', 'playlist', 'video']
    print('Started')
    print('res', kwargs['resolution'])
    try:
        if mode == 'channel':
            print('..channel mode')
            channel = Channel(url)
            author = channel.channel_name
            for index, link in enumerate(channel):
                print(link)
                download_video(link, resolution=kwargs['resolution'])


        if mode == 'playlist':
            print('..playlist mode')
            playlist = Playlist(url)
            for index, link in enumerate(playlist.video_urls):
                print(link)
                download_video(link, resolution=kwargs['resolution'])


        if mode == 'video':
            print(url)
            download_video(url, resolution=kwargs['resolution'])
            pass
    except:
        print('Error occured')

