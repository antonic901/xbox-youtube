# -*- coding: utf-8 -*-
import requests
import gui
import os.path
import invidious
import urllib
import utils
import sys
import xbmcaddon

COLOR_CODE_MAIN = 'ffe52d27'
PLUGIN_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
PLUGIN_RELATIVE_PATH = sys.argv[0]
ICON = os.path.join(PLUGIN_PATH, 'icon.png')

LIMIT = 20

def play(**kwargs):
    stream_url = invidious.getVideoLink(kwargs.get('id', None))
    if stream_url:
        gui.play(stream_url)

def clear_history():
    utils.clear_history()
    gui.notify('History cleared.')

def open_settings():
    xbmcaddon.Addon().openSettings()

def import_subscription():
    if utils.importSubcriptions():
        gui.notify('Successfully imported subcriptions from YouTube.')
    else:
        gui.notify("Subscriptions file can't be found.")

def subscribe(**kwargs):
    channel = invidious.getInfoAboutChannel(kwargs.get('id'))
    array = [kwargs.get('id'), channel['authorUrl'], channel['author']]
    if utils.subscribe(array):
        gui.notify('Successfully subscribed to channel %s' % channel['author'])
    else:
        gui.notify('Already subscribed.')

def list_index():
    gui.add_item('Trending', url_params={'f': 'trending'}, is_folder=True)
    gui.add_item('Popular', url_params={'f': 'popular'}, is_folder=True)
    gui.add_item('Search', url_params={'f': 'searchMenu', 'q': '-'}, is_folder=True)
    gui.add_item('Subscriptions', url_params={'f': 'subscriptions'}, is_folder=True)
    gui.add_item('Settings', url_params={'f': 'settings'}, is_playable=False)
    gui.end_listing()

def list_trending(**kwargs):
    page_number = int(kwargs.pop('pageNumber', 1)) + 1

    if page_number == 2:
        gui.add_item('All', ICON, {'f': 'trending', 'pageNumber': page_number}, is_folder=True)
        gui.add_item('Music', ICON, {'f': 'trending', 'pageNumber': page_number, 'type': 'music'}, is_folder=True)
        gui.add_item('Gaming', ICON, {'f': 'trending', 'pageNumber': page_number, 'type': 'gaming'}, is_folder=True)
        gui.add_item('News', ICON, {'f': 'trending', 'pageNumber': page_number, 'type': 'news'}, is_folder=True)
        gui.add_item('Movies', ICON, {'f': 'trending', 'pageNumber': page_number, 'type': 'movies'}, is_folder=True)

    else:
        videos = invidious.getTrending(kwargs.pop('type', None))
        if not videos:
            gui.end_listing()
            return

        for video in videos:
            video_id = video['videoId']
            title = video['title']
            description = video['description']
            date = video['published']
            channel_id = video['authorId']
            channel_title = video['author']
            thumb = video['videoThumbnails'][3]['url']
            duration_in_seconds = video['lengthSeconds']
            gui.add_item(title, thumb, {'f': 'play', 'id': video_id},
                {'title': title, 'plot': description, 'year': date, 'director': channel_title},
                    duration_in_seconds, 
                    context_menu_items=[
                        ('Go to [B]%s[/B]' % channel_title, 'xbmc.Container.Update(%s?'
                        'f=channelMenu&id=%s)' % (PLUGIN_RELATIVE_PATH, channel_id)),
                        ('Suggested videos', 
                        'xbmc.Container.Update(%s?'
                        'f=suggestedVideos&id=%s)' % (PLUGIN_RELATIVE_PATH, video_id))], total_items=21)

    gui.end_listing()

def list_popular(**kwargs):
    videos = invidious.getPopular()
    if not videos:
        gui.end_listing()
        return

    for video in videos:
        video_id = video['videoId']
        title = video['title']
        date = video['published']
        channel_id = video['authorId']
        channel_title = video['author']
        thumb = video['videoThumbnails'][3]['url']
        duration_in_seconds = video['lengthSeconds']
        gui.add_item(title, thumb, {'f': 'play', 'id': video_id},
            {'title': title, 'year': date, 'director': channel_title},
                duration_in_seconds, 
                context_menu_items=[
                        ('Go to [B]%s[/B]' % channel_title, 'xbmc.Container.Update(%s?'
                        'f=channelMenu&id=%s)' % (PLUGIN_RELATIVE_PATH, channel_id)),
                        ('Suggested videos', 
                        'xbmc.Container.Update(%s?'
                        'f=suggestedVideos&id=%s)' % (PLUGIN_RELATIVE_PATH, video_id))], total_items=LIMIT + 1)

    gui.end_listing()

def list_channel_menu(**kwargs):
    gui.add_item('Videos', url_params={'f': 'channelVideos', 'id': kwargs.get('id')}, is_folder=True)
    gui.add_item('Latest', url_params={'f': 'channelLatest', 'id': kwargs.get('id')}, is_folder=True)
    gui.add_item('Playlists', url_params={'f': 'channelPlaylists', 'id': kwargs.get('id')}, is_folder=True)
    gui.add_item('Search', url_params={'f': 'channelSearch', 'id': kwargs.get('id'), 'q': '-'}, is_folder=True)
    gui.add_item('Related Channels', url_params={'f': 'channelRelated', 'id': kwargs.get('id')}, is_folder=True)
    gui.add_item('Subscribe', url_params={'f': 'subscribe', 'id': kwargs.get('id')}, is_playable=False)
    gui.end_listing()

def list_channel_videos(**kwargs):
    page_number = int(kwargs.pop('pageNumber', 1)) + 1
    videos = invidious.getVideosForChannel(kwargs.get('id'), page_number - 1)
    if not videos:
        gui.end_listing()
        return

    for video in videos:
        video_id = video['videoId']
        title = video['title']
        date = video['published']
        channel_id = video['authorId']
        channel_title = video['author']
        thumb = video['videoThumbnails'][3]['url']
        duration_in_seconds = video['lengthSeconds']
        gui.add_item(title, thumb, {'f': 'play', 'id': video_id},
            {'title': title, 'year': date, 'director': channel_title},
                duration_in_seconds,
                context_menu_items=[
                        ('Go to [B]%s[/B]' % channel_title, 'xbmc.Container.Update(%s?'
                        'f=channelMenu&id=%s)' % (PLUGIN_RELATIVE_PATH, channel_id)),
                        ('Suggested videos', 
                        'xbmc.Container.Update(%s?'
                        'f=suggestedVideos&id=%s)' % (PLUGIN_RELATIVE_PATH, video_id))], total_items=LIMIT + 1)

    kwargs['f'] = 'channelVideos'
    kwargs['pageNumber'] = page_number
    gui.add_item('[B][COLOR %s]Next page (%s)[/COLOR][/B]' % (COLOR_CODE_MAIN, page_number), ICON, kwargs,
                is_folder=True, total_items=LIMIT + 1)

    gui.end_listing()

def list_channel_latest(**kwargs):
    videos = invidious.getLatestForChannel(kwargs.get('id'))
    if not videos:
        gui.end_listing()
        return

    for video in videos:
        video_id = video['videoId']
        title = video['title']
        date = video['published']
        channel_id = video['authorId']
        channel_title = 'No info'
        thumb = video['videoThumbnails'][3]['url']
        duration_in_seconds = video['lengthSeconds']
        gui.add_item(title, thumb, {'f': 'play', 'id': video_id},
            {'title': title, 'year': date, 'director': channel_title},
                duration_in_seconds, 
                context_menu_items=[
                        ('Go to [B]%s[/B]' % channel_title, 'xbmc.Container.Update(%s?'
                        'f=channelMenu&id=%s)' % (PLUGIN_RELATIVE_PATH, channel_id)),
                        ('Suggested videos', 
                        'xbmc.Container.Update(%s?'
                        'f=suggestedVideos&id=%s)' % (PLUGIN_RELATIVE_PATH, video_id))],total_items=LIMIT + 1)

    gui.end_listing()

def list_channel_playlists(**kwargs):
    playlists = invidious.getPlaylistsForChannel(kwargs.get('id'))
    if not playlists:
        gui.end_listing()
        return

    for playlist in playlists:
        playlist_id = playlist['playlistId']
        title = playlist['title']
        channel_id = playlist['authorId']
        channel_title = playlist['author']
        thumb = playlist['playlistThumbnail']
        gui.add_item(title, thumb,
            url_params={'f': 'videosPlaylists', 'id': playlist_id},
            video_info_labels={'title': title, 'director': channel_title},
            is_folder=True,
            context_menu_items=[
                        ('Go to [B]%s[/B]' % channel_title, 'xbmc.Container.Update(%s?'
                        'f=channelMenu&id=%s)' % (PLUGIN_RELATIVE_PATH, channel_id))], total_items=LIMIT + 1)

    gui.end_listing()

def list_channel_search(**kwargs):
    gui.add_item('Videos', url_params={'f': 'searchVideos', 'q': '-', 'type': 'video', 'id': kwargs.get('id')}, is_folder=True)
    gui.add_item('Playlists', url_params={'f': 'searchPlaylists', 'q': '-', 'type': 'playlist', 'id': kwargs.get('id')}, is_folder=True)
    gui.add_item('Channels', url_params={'f': 'searchChannels', 'q': '-', 'type': 'channel', 'id': kwargs.get('id')}, is_folder=True)
    gui.end_listing()

def list_channel_related(**kwargs):
    channel = invidious.getInfoAboutChannel(kwargs.get('id'))
    if not channel:
        gui.end_listing()
        return

    for channel in channel['relatedChannels']:
        channel_id = channel['authorId']
        title = channel['author']
        # description = channel['description']
        thumb = channel['authorThumbnails'][3]['url']
        gui.add_item(title, thumb,
            url_params={'f': 'channelMenu', 'id': channel_id},
            video_info_labels={'title': title, 'director': title},
            is_folder=True,
            total_items=LIMIT + 1)

    gui.end_listing()

def list_search_menu(**kwargs):
    gui.add_item('Videos', url_params={'f': 'searchVideos', 'q': '-', 'type': 'video'}, is_folder=True)
    gui.add_item('Playlists', url_params={'f': 'searchPlaylists', 'q': '-', 'type': 'playlist'}, is_folder=True)
    gui.add_item('Channels', url_params={'f': 'searchChannels', 'q': '-', 'type': 'channel'}, is_folder=True)
    gui.add_item('Clear history...', url_params={'f': 'historyClear'}, is_playable=False)

    for history in utils.getHistory():
        if history['type'] == 'video':
            gui.add_item('[B]History:[/B] {} in {}'.format(history['q'], history['type']), url_params={'f': 'searchVideos', 'q': history['q'], 'type': history['type']}, is_folder=True)
        elif history['type'] == 'playlist':
            gui.add_item('[B]History:[/B] {} in {}'.format(history['q'], history['type']), url_params={'f': 'searchPlaylists', 'q': history['q'], 'type': history['type']}, is_folder=True)
        elif history['type'] == 'channel':
            gui.add_item('[B]History:[/B] {} in {}'.format(history['q'], history['type']), url_params={'f': 'searchChannels', 'q': history['q'], 'type': history['type']}, is_folder=True)

    gui.end_listing()

def list_search_videos(**kwargs):
    page_number = int(kwargs.pop('pageNumber', 1)) + 1
    if page_number == 2 and kwargs.get('q') == '-':
        q = gui.get_search_input('Search')
        if q is None:
            return
        kwargs['q'] = q
        utils.saveInHistory(q, 'video')

    if kwargs.get('id', None):
        videos = invidious.searchChannel(kwargs.get('id'), kwargs.get('q'), page_number - 1)
    else:
        videos = invidious.search(kwargs.get('q'), page_number-1, kwargs.get('type'))

    if not videos:
        gui.end_listing()
        return
        
    for video in videos:
        if video['type'] == kwargs.get('type'):
            video_id = video['videoId']
            title = video['title']
            description = video['description']
            date = video['published']
            channel_id = video['authorId']
            channel_title = video['author']
            thumb = video['videoThumbnails'][3]['url']
            duration_in_seconds = video['lengthSeconds']
            gui.add_item(title, thumb, {'f': 'play', 'id': video_id},
                {'title': title, 'plot': description, 'year': date, 'director': channel_title},
                    duration_in_seconds, 
                    context_menu_items=[
                        ('Go to [B]%s[/B]' % channel_title, 'xbmc.Container.Update(%s?'
                        'f=channelMenu&id=%s)' % (PLUGIN_RELATIVE_PATH, channel_id)),
                        ('Suggested videos', 
                        'xbmc.Container.Update(%s?'
                        'f=suggestedVideos&id=%s)' % (PLUGIN_RELATIVE_PATH, video_id))],total_items=LIMIT + 1)

    kwargs['f'] = 'searchVideos'
    kwargs['pageNumber'] = page_number
    gui.add_item('[B][COLOR %s]Next page (%s)[/COLOR][/B]' % (COLOR_CODE_MAIN, page_number), ICON, kwargs,
                    is_folder=True, total_items=LIMIT + 1)

    gui.end_listing()

def list_search_playlists(**kwargs):
    page_number = int(kwargs.pop('pageNumber', 1)) + 1
    if page_number == 2 and kwargs.get('q') == '-':
        q = gui.get_search_input('Search')
        if q is None:
            return
        kwargs['q'] = q
        utils.saveInHistory(q, 'playlist')
    
    if kwargs.get('id', None):
        playlists = invidious.searchChannel(kwargs.get('id'), kwargs.get('q'), page_number - 1)
    else:
        playlists = invidious.search(kwargs.get('q'), page_number-1,kwargs.get('type'))

    if not playlists:
        gui.end_listing()
        return

    for playlist in playlists:
        if playlist['type'] == kwargs.get('type'):
            playlist_id = playlist['playlistId']
            title = playlist['title']
            channel_id = playlist['authorId']
            channel_title = playlist['author']
            thumb = playlist['playlistThumbnail']
            gui.add_item(title, thumb,
                url_params={'f': 'videosPlaylists', 'id': playlist_id},
                video_info_labels={'title': title, 'director': channel_title},
                is_folder=True,
                context_menu_items=[
                        ('Go to [B]%s[/B]' % channel_title, 'xbmc.Container.Update(%s?'
                        'f=channelMenu&id=%s)' % (PLUGIN_RELATIVE_PATH, channel_id))], total_items=LIMIT + 1)

    kwargs['f'] = 'searchPlaylists'
    kwargs['pageNumber'] = page_number
    gui.add_item('[B][COLOR %s]Next page (%s)[/COLOR][/B]' % (COLOR_CODE_MAIN, page_number), ICON, kwargs,
                is_folder=True, total_items=LIMIT + 1)

    gui.end_listing()

def list_search_channels(**kwargs):
    page_number = int(kwargs.pop('pageNumber', 1)) + 1
    if page_number == 2 and kwargs.get('q') == '-':
        q = gui.get_search_input('Search')
        if q is None:
            return
        kwargs['q'] = q
        utils.saveInHistory(q, 'channel')

    if kwargs.get('id', None):
        channels = invidious.searchChannel(kwargs.get('id'), kwargs.get('q'), page_number - 1)
    else:
        channels = invidious.search(kwargs.get('q'), page_number-1,kwargs.get('type'))

    if not channels:
        gui.end_listing()
        return

    for channel in channels:
        if channel['type'] == kwargs.get('type'):
            channel_id = channel['authorId']
            title = channel['author']
            description = channel['description']
            thumb = channel['authorThumbnails'][3]['url']
            gui.add_item(title, thumb,
                url_params={'f': 'channelMenu', 'id': channel_id},
                video_info_labels={'title': title, 'plot': description, 'director': title},
                is_folder=True,
                context_menu_items=[
                        ('Subscribe to [B]%s[/B]' % title, 'xbmc.Container.Update(%s?'
                        'f=subscribe&id=%s)' % (PLUGIN_RELATIVE_PATH, channel_id))], total_items=LIMIT + 1)

    kwargs['f'] = 'searchChannels'
    kwargs['pageNumber'] = page_number
    gui.add_item('[B][COLOR %s]Next page (%s)[/COLOR][/B]' % (COLOR_CODE_MAIN, page_number), ICON, kwargs,
                is_folder=True, total_items=LIMIT + 1)

    gui.end_listing()

def list_videos_playlists(**kwargs):
    videos = invidious.getInfoAboutPlaylist(kwargs.get('id'))['videos']
    if not videos:
        gui.end_listing()
        return

    for video in videos:
        video_id = video['videoId']
        title = video['title']
        thumb = video['videoThumbnails'][3]['url']
        duration_in_seconds = video['lengthSeconds']
        gui.add_item(title, thumb, {'f': 'play', 'id': video_id},
            {'title': title},
                duration_in_seconds, 
                context_menu_items=[
                        # ('Go to [B]%s[/B]' % channel_title, 'xbmc.Container.Update(%s?'
                        # 'f=channelMenu&id=%s)' % (PLUGIN_RELATIVE_PATH, channel_id)),
                        ('Suggested videos', 
                        'xbmc.Container.Update(%s?'
                        'f=suggestedVideos&id=%s)' % (PLUGIN_RELATIVE_PATH, video_id))], total_items=LIMIT + 1)

    gui.end_listing()

def list_subscriptions(**kwargs):
    channels = utils.readCsvFile()
    for channel in channels:
        channel_id = channel[0]
        title = channel[2]
        # description = channel['description']
        # thumb = channel['authorThumbnails'][3]['url']
        gui.add_item(title,
            url_params={'f': 'channelMenu', 'id': channel_id},
            video_info_labels={'title': title, 'director': title},
            is_folder=True,
            total_items=LIMIT + 1)

    gui.end_listing()

def list_suggested_videos(**kwargs):
    videos = invidious.getInfoAboutVideo(kwargs.get('id'))['recommendedVideos']
    if not videos:
        gui.end_listing()
        return
        
    for video in videos:
        video_id = video['videoId']
        title = video['title']
        thumb = video['videoThumbnails'][3]['url']
        duration_in_seconds = video['lengthSeconds']
        gui.add_item(title, thumb, {'f': 'play', 'id': video_id},
            {'title': title},
                duration_in_seconds, 
                context_menu_items=[
                        # ('Go to [B]%s[/B]' % channel_title, 'xbmc.Container.Update(%s?'
                        # 'f=channelMenu&id=%s)' % (PLUGIN_RELATIVE_PATH, channel_id)),
                        ('Suggested videos', 
                        'xbmc.Container.Update(%s?'
                        'f=suggestedVideos&id=%s)' % (PLUGIN_RELATIVE_PATH, video_id))], total_items=LIMIT + 1)

    gui.end_listing()