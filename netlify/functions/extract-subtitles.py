import json
from youtube_transcript_api import YouTubeTranscriptApi

def handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type', 
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    }
    
    if event['httpMethod'] == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    try:
        body = json.loads(event['body'])
        url = body.get('url', '')
        
        # Extraire video_id
        if 'v=' in url:
            video_id = url.split('v=')[1].split('&')[0]
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
        else:
            raise ValueError('URL YouTube invalide')
        
        # Extraire sous-titres auto-générés anglais
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        text = ' '.join([item['text'] for item in transcript])
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'subtitles': text,
                'language': 'en-auto',
                'video_id': video_id,
                'message': 'Vrais sous-titres extraits !'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
