# TikTok Video Scraper and Downloader

A comprehensive Python tool for scraping TikTok videos from hashtags and user IDs. This project includes advanced features for handling rate limits and large-scale data collection.

## Features

- Scrape TikTok videos by hashtags or user IDs
- Automatic handling of page refresh and retry mechanisms
- Duplicate-free video URL storage in JSON format
- Video downloading via Cobalt API (Docker-based)
- Enhanced scraping capabilities using undetected-chromedriver 

## Prerequisites

- Python 3.x
- Google Chrome
- Docker (for Cobalt API)
- Optional: VPN service for large-scale scraping to avoid restrictions

## Installation

### 1. Python Dependencies

Install the required Python packages:

```bash
pip install selenium requests undetected-chromedriver
```

### 2. VPN Setup (Optional)

For large-scale scraping operations:
1. Subscribe to a reliable VPN service (e.g., Surfshark)
2. Configure VPN before running the scraper
3. Use different VPN servers to rotate IPs

### 3. Proxy Configuration (Optional)

For advanced users requiring IP rotation:
1. Set up NGINX as a reverse proxy
2. Configure proxy rotation in the scraper settings
3. Manage request distribution through your proxy setup

### 4. Cobalt API Setup 
Official cobalt tutorial: https://github.com/imputnet/cobalt/blob/main/docs/run-an-instance.md

#### Step 1: Install Docker
Follow the [official Docker installation guide](https://docs.docker.com/get-docker/).

#### Step 2: Create docker-compose.yml

```yaml
services:
    cobalt-api:
        image: ghcr.io/imputnet/cobalt:10  # Pull the latest Cobalt API image

        init: true
        read_only: true
        restart: unless-stopped
        container_name: cobalt-api

        ports:
            - 9000:9000/tcp  # Expose port 9000 to access the API locally
            # Uncomment the next line and remove the one above if using a reverse proxy like Nginx
            # - 127.0.0.1:9000:9000

        environment:
            API_URL: "http://localhost:9000/"
            DURATION_LIMIT: "43200"

        labels:
            - com.centurylinklabs.watchtower.scope=cobalt

        # Uncomment only if you use the COOKIE_PATH variable
        # volumes:
            # - ./cookies.json:/cookies.json

    # Watchtower for automatic updates of the Cobalt image
    watchtower:
        image: ghcr.io/containrrr/watchtower  # Pull Watchtower for automated updates
        restart: unless-stopped
        command: --cleanup --scope cobalt --interval 900 --include-restarting
        volumes:
            - /var/run/docker.sock:/var/run/docker.sock  # Required for Watchtower to manage containers
```

#### Step 3: Launch and Verify

```bash
# Start Cobalt API
docker compose up -d

# Verify installation
curl http://localhost:9000/api/serverInfo
```

## Usage

### Scraping by Hashtag

```bash
python main.py
# Choose: 2 for account scrapper
# enter source csv file ( row[0] is subfolder name, the keyword to group users. row[1] is user id for search)
```

### Scraping by User Profile/ID

```bash
python main.py
# Choose: 2) Scrape by user
# Enter username or user ID: itztherizzler
# Enter max videos: 50
```

## Project Structure

### Core Components

1. `scrape_lists.py`
   - Functions for hashtag and user profile scraping
   - Retry logic and page refresh handling
   - Rate limit management

2. `download.py`
   - Video download management
   - Cobalt API integration
   - Download queue handling

3. `main.py`
   - CLI interface
   - Scraping mode selection
   - Configuration management

### Output Structure

- Scraped lists folder: 
    - `<identifier>_video_urls.json`
- Videos folder: 
    - `/Volumes/T7 Black/Borderx/<identifier>_videos/`
- Logs: `scraper.log`

## Best Practices

1. Rate Limit Management
   - Use VPN for large-scale scraping
   - Implement delays between requests
   - Rotate IP addresses when possible

2. Error Handling
   - Automatic retry on network errors
   - Page refresh on stale data
   - Session management

3. Data Management
   - Regular JSON file backups
   - Duplicate URL prevention
   - Organized video storage

## Troubleshooting

### Common Issues

1. Rate Limiting
   ```bash
   # Adjust Cobalt API limits in docker-compose.yml
   RATELIMIT_MAX: "200"
   RATELIMIT_WINDOW: "600"
   ```

2. Chrome Detection
   ```python
   # Use undetected-chromedriver
   import undetected_chromedriver as uc
   driver = uc.Chrome()
   ```

3. Network Errors
   - Check VPN connection
   - Verify proxy configuration
   - Ensure stable internet connection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Acknowledgments

- Cobalt API team
- Selenium maintainers
- undetected-chromedriver developers

## Author
- Yi Sun (Aven)
- aven@borderxai.com

---
Last updated: January 2025
