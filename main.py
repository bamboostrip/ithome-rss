import argparse
import datetime
import calendar
import feedparser
import sys
import re

def get_time_bounds(time_param):
    now_local = datetime.datetime.now().astimezone() 
    
    if time_param == "30m":
        start_time = now_local - datetime.timedelta(minutes=30)
        end_time = now_local
    elif time_param == "1h":
        start_time = now_local - datetime.timedelta(hours=1)
        end_time = now_local
    elif time_param == "1d":
        start_time = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = now_local.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif time_param == "yesterday":
        yesterday = now_local - datetime.timedelta(days=1)
        start_time = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
    else:
        raise ValueError(f"Invalid time parameter: {time_param}")
    
    return start_time.astimezone(datetime.timezone.utc), end_time.astimezone(datetime.timezone.utc)

def clean_html(raw_html):
    cleantext = re.sub(r'<.*?>', '', raw_html)
    cleantext = re.sub(r'\s+', ' ', cleantext)
    return cleantext.strip()

def scrape_ithome(time_param):
    try:
        start_time, end_time = get_time_bounds(time_param)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
        
    print(f"Scraping ITHome news for parameter: '{time_param}'")
    
    feed_url = 'https://www.ithome.com/rss/'
    d = feedparser.parse(feed_url)
    
    if not d.entries:
        print("No entries found or failed to parse the feed.")
        return
        
    matches = []
    
    for entry in d.entries:
        if not hasattr(entry, 'published_parsed') or not entry.published_parsed:
            continue
            
        # published_parsed is UTC struct_time, use calendar.timegm
        entry_time_ts = calendar.timegm(entry.published_parsed)
        entry_time_utc = datetime.datetime.fromtimestamp(entry_time_ts, datetime.timezone.utc)
        
        if start_time <= entry_time_utc <= end_time:
            matches.append((entry_time_utc, entry))
            
    matches.sort(key=lambda x: x[0], reverse=True)
    
    if not matches:
        print(f"No news found in the specified time range ({time_param}).")
        return
        
    for dt_utc, entry in matches:
        dt_local = dt_utc.astimezone()
        desc = clean_html(entry.description) if hasattr(entry, 'description') else ""
        
        print(f"[{dt_local.strftime('%Y-%m-%d %H:%M:%S')}] {entry.title}")
        print(f"Link: {entry.link}")
        print(f"Summary: {desc}")
        print("-" * 60)
        
    print(f"Total: {len(matches)} news items found.")

def main():
    parser = argparse.ArgumentParser(description="Scrape ITHome news and format for summary.")
    parser.add_argument(
        "--time", 
        type=str, 
        required=True, 
        choices=["30m", "1h", "1d", "yesterday"],
        help="Time range: 30m, 1h, 1d (today natural day), yesterday (yesterday natural day)"
    )
    
    args = parser.parse_args()
    scrape_ithome(args.time)

if __name__ == "__main__":
    main()
