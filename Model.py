from openai import OpenAI
from bs4 import BeautifulSoup
import requests
import ast

"""

 You are an assistant that MUST return only real, verified HTML selectors from live websites. 
            You will ALWAYS perform the following steps before answering:

            1. For each given homepage and relevant page URL, fetch the live HTML of the relevant page.
            2. Inspect the HTML DOM to find the EXACT tag name, CSS class, and/or ID for each required field.
            - These values MUST match exactly with the live HTML at the time of scraping.
            - Do not make up or guess any class names, IDs, or tags. 
            - If you cannot find the field on the given site, you must check an alternative reputable site with similar content and get the real selector from there.
            3. For each field, return a list in the format: [tagname, unique_class_name, unique_id]
            - If a field does not have a class or ID in the HTML, set that position to None.
            - You MUST NOT return [None, None, None] unless you have confirmed across multiple similar sites that the field truly does not exist anywhere.
            4. Output ONLY the final Python list in the following format:
                - First element: a list of all field names.
                - Each following element: 
                    [
                        homepage_url, 
                        relevant_page_url,
                        {{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Accept-Language": "en-US,en;q=0.9"}}, 
                        {{
                            field1: [tag, class, id],
                            field2: [tag, class, id],
                            ...
                        }}
                    ]
            5. Your output must be valid Python syntax, no extra explanations, no placeholders.

            PROMPT:
            {prompt}

            NUMBER OF WEBSITES:
            {number_of_websites}

            STRICT RULES:
            - Always verify selectors from the live page source before answering.
            - Always provide the most specific class or ID possible for accurate scraping.
            - Do not invent selectors — answer only after confirming from HTML.
            - Use lowercase tag names exactly as in HTML.

"""

def DataModel(raw_data):
    
    client = OpenAI(api_key="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")

    response = client.responses.create(
        model = "gpt-4o-mini",
        input= f"""
        You are given the following raw JSON-like data from multiple websites (Justdial, Sulekha, etc.) containing details about driving schools in Mumbai:

{raw_data}

The "address" field in some entries contains a JSON array or object with nested "LocalBusiness" entries.
Parse all "LocalBusiness" entries, no matter how deeply nested.

For each "LocalBusiness" entry:

"name" → value from the business object.

"location" → combine addressLocality, addressRegion, postalCode, and addressCountry into one string, separated by commas, skipping any missing parts.

"phone_number" → take from "telephone" if present; if not, take from the top-level "phone" in the source entry; if still not available, leave as an empty string.

"email" → take from the top-level "email" if available; otherwise leave as an empty string.

Rules:

Include all businesses, even if some fields are missing.

Output must be only a valid Python list of dictionaries in the following format — no extra text, no markdown, no explanations:

[
    {{
        "name": "XYZ Motor Driving School",
        "location": "Andheri West, Mumbai, 400053, IN",
        "phone_number": "+91 9876543210",
        "email": "xyz@gmail.com"
    }},
    {{
        "name": "ABC Driving School",
        "location": "Borivali West, Mumbai, 400092, IN",
        "phone_number": "",
        "email": ""
    }}
]
        """
    )
    
    return ast.literal_eval(response.output_text.strip())

def Model(prompt, number_of_websites):
    client = OpenAI(api_key="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")
    
    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"""
           You are a search URL generator for a lead generation system.

            Your task:
            - Read the user query, detect:
            1. The search topic (type of business/service)
            2. The location
            3. The number of results requested
            - Choose the most relevant and reputable websites for that category in the given location.
            - Construct the exact, real search/listing page URL for each chosen site.
            - Return exactly the number of results requested.
            - Each URL must be a direct, working link to the listing page for that topic in that location.

            Rules:
            1. Use only reputable, established listing sites (e.g., Sulekha, Justdial, UrbanPro, Yelp, TripAdvisor, etc.).
            2. Do not guess — use real URL structures from the actual site.
            3. Do not return social media links.
            4. Do not return search engine result pages (e.g., Google, Bing).
            5. Output only a valid Python list of strings (each string is a URL).
            6. Do not include any text other than the Python list.

            User query:
            {prompt}
            
            Number expected outcome :
            {number_of_websites}

            Output format:
            [
                "https://...",
                "https://...",
                "https://..."
            ]

        """
    )

    clean_output = response.output_text.strip()

    # if clean_output.startswith("```"):
    #     clean_output = "\n".join(line for line in clean_output.splitlines() if not line.strip().startswith("```"))
    return ast.literal_eval(clean_output)


if __name__ == "__main__":
    websites_list = Model("barber shop in narhe", 3)
