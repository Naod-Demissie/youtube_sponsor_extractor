"""
Sponsor extraction functionality using OpenRouter API
"""
import json
from openai import OpenAI
from constants import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_MODEL, OPENROUTER_HEADERS, PROMPT_TEMPLATE

def extract_sponsor_info(description):
    """Use OpenRouter API to extract sponsor information from the description."""
    if not OPENROUTER_API_KEY:
        raise ValueError("OpenRouter API key not found in .env file")

    prompt = PROMPT_TEMPLATE.replace("{description}", description)

    client = OpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=OPENROUTER_API_KEY,
    )

    try:
        completion = client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},  # Ensure JSON response format
            extra_headers=OPENROUTER_HEADERS,
        )
        
        # Get the response content
        response_content = completion.choices[0].message.content
        
        # Debug the response content
        if not response_content or response_content.isspace():
            return []  # Return empty array if response is empty
            
        # Try to parse the JSON, with fallback handling
        try:
            # Clean the response if it has markdown code blocks
            if response_content.strip().startswith('```json') and response_content.strip().endswith('```'):
                # Extract content from markdown code block
                response_content = response_content.strip().removeprefix('```json').removesuffix('```').strip()
            elif response_content.strip().startswith('```') and response_content.strip().endswith('```'):
                # Extract content from generic code block
                response_content = response_content.strip().removeprefix('```').removesuffix('```').strip()
                
            sponsor_info = json.loads(response_content)
            
            # Validate the response structure and clean the data
            cleaned_sponsors = []
            
            if isinstance(sponsor_info, list):
                raw_sponsors = sponsor_info
            elif isinstance(sponsor_info, dict) and 'sponsors' in sponsor_info:
                raw_sponsors = sponsor_info['sponsors']
            else:
                # If it's not in the expected format, return an empty list
                return []
                
            # Clean the data - remove entries with <NA> or None values
            for sponsor in raw_sponsors:
                if not isinstance(sponsor, dict):
                    continue
                    
                # Ensure both Brand and URL keys exist
                if 'Brand' not in sponsor or 'URL' not in sponsor:
                    continue
                    
                # Skip entries with empty, None, or <NA> values
                brand = sponsor.get('Brand')
                url = sponsor.get('URL')
                
                if brand in (None, '', '<NA>', 'NA', 'N/A') or url in (None, '', '<NA>', 'NA', 'N/A'):
                    continue
                    
                # Add clean entry
                cleaned_sponsors.append({
                    'Brand': brand,
                    'URL': url if url else ''
                })
                
            return cleaned_sponsors
                
        except json.JSONDecodeError:
            # If JSON parsing fails, return empty list
            return []
        except Exception as e:
            # Handle any other errors in processing
            print(f"Error processing sponsor data: {str(e)}")
            return []
            
    except Exception as e:
        raise Exception(f"OpenRouter API error: {str(e)}")
