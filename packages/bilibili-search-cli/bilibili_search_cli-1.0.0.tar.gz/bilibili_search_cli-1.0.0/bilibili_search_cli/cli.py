import requests
import random
import time
from fake_useragent import UserAgent
import logging
import json
from urllib.parse import quote
from datetime import datetime
import argparse
from . import __version__

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_random_ua():
    ua = UserAgent()
    return ua.random

def create_session():
    session = requests.Session()
    return session

def format_number(num_str):
    try:
        if isinstance(num_str, (int, float)):
            return int(num_str)
        if not num_str or num_str == 'Unknown':
            return 0
        return int(num_str.replace(',', ''))
    except:
        return 0

def get_bilibili_videos(keyword, limit=20):
    # Use Bilibili search API
    encoded_keyword = quote(keyword)
    url = f"https://api.bilibili.com/x/web-interface/search/type?keyword={encoded_keyword}&page=1&search_type=video&page_size={limit}"
    
    # Set request headers
    headers = {
        'authority': 'api.bilibili.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'cookie': "buvid3=randomstring; b_nut=1679904000; i-wanna-go-back=-1; b_ut=7; _uuid=randomstring; buvid4=randomstring",  # Simulate basic Cookie
        'dnt': '1',
        'origin': 'https://search.bilibili.com',
        'pragma': 'no-cache',
        'referer': 'https://search.bilibili.com/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': get_random_ua()
    }
    
    try:
        # Add random delay
        time.sleep(random.uniform(2, 5))
        
        session = create_session()
        response = session.get(
            url,
            headers=headers,
            timeout=15
        )
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Check API response status
        if data['code'] != 0:
            logger.error(f"API Error: {data['message']}")
            return []
            
        # Get video results
        video_results = data['data'].get('result', [])
        
        if not video_results:
            logger.info("No videos found")
            return []
            
        # Process video information
        processed_videos = []
        for video in video_results[:limit]:  # Limit return count
            try:
                video_info = {
                    "title": video['title'].replace('<em class="keyword">', '').replace('</em>', ''),
                    "author": video['author'],
                    "bvid": video.get('bvid', ''),
                    "play_count": format_number(video.get('play', 0)),
                    "duration": video.get('duration', ''),
                    "pubdate": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(video.get('pubdate', 0))),
                    "url": f"https://www.bilibili.com/video/{video.get('bvid', '')}"
                }
                processed_videos.append(video_info)
                
            except KeyError as e:
                logger.error(f"Error parsing video info: {e}")
                continue
        
        # Output structured data
        output = {
            "keyword": keyword,
            "total_count": len(processed_videos),
            "videos": processed_videos
        }
        
        # Print JSON formatted result
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return processed_videos
                
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        logger.error(f"Response content: {response.text if 'response' in locals() else 'No response'}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
    except Exception as e:
        logger.error(f"Unknown error: {e}")
    finally:
        if 'session' in locals():
            session.close()
    
    return []

def main():
    parser = argparse.ArgumentParser(
        description='''
Bilibili Video Search Tool - Quick search for Bilibili videos with structured output

This tool helps you search for videos on Bilibili and outputs the information in JSON format.
Output includes: title, author, play count, duration, publication date, and video URL.

Example Usage:
  bilibili-search "happy new year"          # Search for "happy new year", return default 20 results
  bilibili-search "dance" -n 5             # Search for "dance" and return 5 results
  bilibili-search "music video" -n 10      # Search phrases with spaces using quotes
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter  # Preserve description formatting
    )
    
    parser.add_argument(
        'keyword',
        help='Search keyword (use quotes if it contains spaces)'
    )
    
    parser.add_argument(
        '-n', '--number',
        type=int,
        default=20,
        help='Number of results to return (default: 20, max: 100)',
        choices=range(1, 101),
        metavar='N'
    )
    
    # Add version information
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    args = parser.parse_args()
    
    if args.number < 1:
        parser.error("Number of results must be greater than 0")
    
    get_bilibili_videos(args.keyword, args.number)

if __name__ == "__main__":
    main()
