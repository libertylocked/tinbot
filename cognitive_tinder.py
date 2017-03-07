"""Run profile photos through MS cognitive services"""
import fb_auth
import requests
import config_keys

_CV_URL = 'https://westus.api.cognitive.microsoft.com/vision/v1.0/describe?maxCandidates=1'
_EMOTION_URL = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'

def main():
    """Main function"""
    session = fb_auth.get_tinder_session()
    while True:
        loop(session)

def loop(session):
    """Runs through recommended users and run their photos thru cog services"""
    nearby = session.nearby_users()
    for hopeful in nearby:
        # print user id
        print hopeful.id
        # filter rules
        if should_skip_profile(hopeful):
            print 'Skipped ' + hopeful.name
            continue
        # print hopeful's info
        print hopeful.name
        print hopeful.schools
        print hopeful.jobs
        print hopeful.bio.encode('ascii', 'ignore')
        # send a post request to CV API
        for photo_url in hopeful.photos:
            print ' '
            print photo_url
            print get_cv_caption(photo_url)
            print get_emotions(photo_url)
        # let user swipe
        swipe = raw_input('swipe y/n/s: ')
        if swipe == 'y':
            hopeful.like()
        elif swipe == 'n':
            hopeful.dislike()
        print '==============================='

def should_skip_profile(hopeful):
    """Skip profiles based on filter rules"""
    if len(hopeful.bio) < 5:
        return True

    return False

def get_cv_caption(url):
    """Gets the CV caption in JSON"""
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': config_keys.CV_KEY
    }
    json_data = {
        'url': url
    }
    response = requests.post(_CV_URL, json=json_data, headers=headers)
    return response.json()['description']['captions']

def get_emotions(url):
    """Gets emotions in JSON"""
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': config_keys.EMOTION_KEY
    }
    json_data = {
        'url': url
    }
    response = requests.post(_EMOTION_URL, json=json_data, headers=headers)
    return response.json()

if __name__ == "__main__":
    main()
