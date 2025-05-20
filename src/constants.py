"""
Constants and configuration for YouTube Sponsor Extractor
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# OpenRouter API Configuration
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL = "google/gemma-3-27b-it:free"
# OPENROUTER_MODEL = "deepseek/deepseek-chat-v3-0324:free"
OPENROUTER_HEADERS = {
    "HTTP-Referer": "http://localhost:8501",
    "X-Title": "YouTube Sponsor Extractor",
}

# Prompt Template for Sponsor Extraction
PROMPT_TEMPLATE = """
You are a specialized extraction tool that identifies sponsor information from YouTube video descriptions.

Your task:
1. Extract ALL sponsor information from the provided YouTube video description
2. Look for any sponsored products, affiliate links, promotional content, or any items with affiliate/shortened links
3. For each sponsor, extract the COMPLETE brand name AND product model (if available)
4. Always include the FULL product name as shown in the description (e.g., "IDEAFORMER IR3 V2" not just "IDEAFORMER")
5. Return ONLY a valid JSON array of objects with 'Brand' and 'URL' keys
6. If no sponsors are found, return an empty array []
7 . Do not include any explanations, markdown formatting, or text outside the JSON

Here are examples of correct extractions:

Example 1 Input:
```
IDEAFORMER IR3 V2 - https://amzn.to/3CkO8EO
GOVEE FLOOR LAMP PRO - https://amzn.to/4fp5zCy
UNITREE GO2 - https://amzn.to/48Km9u2
```

Example 1 Correct Output:
```json
[
  {"Brand": "IDEAFORMER IR3 V2", "URL": "https://amzn.to/3CkO8EO"},
  {"Brand": "GOVEE FLOOR LAMP PRO", "URL": "https://amzn.to/4fp5zCy"},
  {"Brand": "UNITREE GO2", "URL": "https://amzn.to/48Km9u2"}
]
```

Example 2 Input:
```
Check out the new Samsung Galaxy S22 Ultra (affiliate link): https://amzn.to/3xyzabc
I'm using the Blue Yeti Microphone for this video: https://bit.ly/blueyeti
```

Example 2 Correct Output:
```json
[
  {"Brand": "Samsung Galaxy S22 Ultra", "URL": "https://amzn.to/3xyzabc"},
  {"Brand": "Blue Yeti Microphone", "URL": "https://bit.ly/blueyeti"}
]
```

Example 3 Input:
```
This video is sponsored by NordVPN. Get 70% off a 3-year plan by visiting https://nordvpn.com/techreview
The laptop stand I'm using is from MOFT: https://www.moft.us/ref10
```

Example 3 Correct Output:
```json
[
  {"Brand": "NordVPN", "URL": "https://nordvpn.com/techreview"},
  {"Brand": "MOFT laptop stand", "URL": "https://www.moft.us/ref10"}
]
```

Description:
{description}

Respond with ONLY the JSON array:
"""
