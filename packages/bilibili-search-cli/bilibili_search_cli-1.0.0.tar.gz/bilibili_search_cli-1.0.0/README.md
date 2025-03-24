# Bilibili Search CLI

A command-line tool to search videos on Bilibili and output results in JSON format.

## Features

- Search videos on Bilibili from command line
- Output results in structured JSON format
- Customizable number of results
- Anti-crawler protection built-in

## Installation

```bash
pip install bilibili-search-cli
```

## Usage

Basic search:
```bash
bilibili-search "happy new year"
```

Limit number of results:
```bash
bilibili-search "dance" -n 5
```

Search with spaces in keyword:
```bash
bilibili-search "music video" -n 10
```

Get help:
```bash
bilibili-search --help
```

## Output Format

The tool outputs JSON-formatted data:

```json
{
  "keyword": "happy new year",
  "total_count": 5,
  "videos": [
    {
      "title": "Happy New Year 2025",
      "author": "username",
      "bvid": "BV1X3XbYkEYZ",
      "play_count": 341,
      "duration": "45:22",
      "pubdate": "2025-03-23 11:34:40",
      "url": "https://www.bilibili.com/video/BV1X3XbYkEYZ"
    }
    // ... more videos
  ]
}
```

## Requirements

- Python 3.6 or higher
- requests
- fake-useragent

## License

MIT License 