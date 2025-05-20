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
# OPENROUTER_MODEL = "google/gemma-3-27b-it:free"
OPENROUTER_MODEL = "deepseek/deepseek-chat-v3-0324:free"
# OPENROUTER_MODEL = "google/gemini-2.0-flash-exp:free"

OPENROUTER_HEADERS = {


    "HTTP-Referer": "http://localhost:8501",
    "X-Title": "YouTube Sponsor Extractor",
}

# Prompt Template for Sponsor Extraction
# PROMPT_TEMPLATE = """
# You are a specialized extraction tool that identifies sponsor information from YouTube video descriptions.

# Your task:
# 1. Extract ALL sponsor information from the provided YouTube video description
# 2. Look for any sponsored products, affiliate links, promotional content, or any items with affiliate/shortened links
# 3. For each sponsor, extract the COMPLETE brand name AND product model (if available)
# 4. Always include the FULL product name as shown in the description (e.g., "IDEAFORMER IR3 V2" not just "IDEAFORMER")
# 5. Return ONLY a valid JSON array of objects with 'Brand' and 'URL' keys
# 6. If no sponsors are found, return an empty array []
# 7. DO NOT include social media links (like Instagram, Twitter, Facebook, TikTok, LinkedIn, etc.) in the results
# 8. Do not include any explanations, markdown formatting, or text outside the JSON
# Description:
# {description}

# Respond with ONLY the JSON array:
# """
PROMPT_TEMPLATE = """
You are a highly specialized information extraction system designed to identify **sponsored content** from YouTube video descriptions.

Your task is to analyze the given video description and extract structured data about sponsorships. You must accurately identify any **paid promotions, affiliate links, sponsored products, or partnerships**.

Extraction Rules:
1. Extract ALL sponsor-related information from the description.
2. Look for any of the following:
   - Mentions of sponsors or promotional partners
   - Products or services offered with discount codes, coupons, or calls to action (e.g., "Check out", "Get X% off", "Use code", etc.)
   - Affiliate or shortened links (e.g., bit.ly, tinyurl, amzn.to, etc.)
   - Any URLs associated with product placements or brand mentions
3. For each sponsor, return an object with:
   - "Brand": The full, explicit brand or product name as shown (e.g., "IDEAFORMER IR3 V2", not just "IDEAFORMER")
   - "URL": The direct URL or affiliate link associated with that sponsor
4. If multiple URLs or links point to the same brand, include only the most relevant (typically the one with the most complete tracking or full product path).
5. DO NOT include:
   - Social media links (e.g., YouTube, Instagram, Twitter, Facebook, TikTok, LinkedIn)
   - Personal donation links (Patreon, Ko-fi, BuyMeACoffee)
   - General channel merch or non-sponsored links unless clearly marked as sponsored or affiliate
6. Return ONLY a valid JSON array of objects in the format:
   [
     {
       "Brand": "Full Product or Brand Name",
       "URL": "https://..."
     },
     ...
   ]
7. If NO sponsored content is found, return exactly:
   []
8. DO NOT include any text, comments, markdown, or explanations outside the JSON array.

Now, extract the data from this description:

{description}

Respond with ONLY the JSON array:
"""
