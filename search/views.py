import requests
from django.conf import settings
from django.shortcuts import render
from isodate import parse_duration
from serpapi import GoogleSearch


def index(request):
    videos = []
    images = []
    if request.method == 'POST':

        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part': 'snippet',
            'q': request.POST['search'],
            'key':  settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 9,
            'type': 'video'

        }

        video_ids = []
        r = requests.get(search_url, params=search_params)
        results = r.json()['items']
        
        for result in results:
            video_ids.append(result['id']['videoId'])

        video_params = {
            'key':  settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet,contentDetails',
            'id': ','.join(video_ids),
            'maxResults': 9,
        }
        r = requests.get(video_url, params=video_params)
        results = r.json()['items']

        for result in results:
            video_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={result["id"]}',
                'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail': result['snippet']['thumbnails']['high']['url']
            }
            videos.append(video_data)

            ImageParams = {
                "api_key": settings.SERPAPI_API_KEY,
                "engine": "google",
                "q": request.POST['search'],
                "location": "Austin, Texas, United States",
                "google_domain": "google.com",
                "gl": "us",
                "hl": "en",
                "num": "9",
                "tbm": "isch",
            }
        
        search = GoogleSearch(ImageParams)
        
        for image_result in search.get_dict()['images_results']:
            link = image_result["original"]

        try:
            print("link: " + link)
        except:
            pass
        for image_result in search.get_dict()['images_results']:
            image_data = {
                'title': image_result['title'],
                'thumbnail': image_result['thumbnail']
            }
            images.append(image_data)
        
    context = {
        'videos': videos,
        'images': images
    }
    
    
    return render(request, 'search/index.html', context)
   