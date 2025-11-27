import requests
import json

def generate_python_app(api_key, user_idea):
    """
    Generates a complete Streamlit app using direct HTTP requests to Gemini.
    Zero dependencies on google-generative-ai SDK.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    prompt = f"""
    You are a Senior Python Developer specializing in Streamlit.
    Your goal is to write a COMPLETE, SINGLE-FILE Streamlit application based on the user's idea.
    
    ### USER IDEA:
    "{user_idea}"
    
    ### ARCHITECTURAL RULES:
    1. **Single File:** The entire app must fit in `app.py`. No external local imports.
    2. **Robustness:** Handle errors gracefully. If inputs are missing, show a warning, not a crash.
    3. **UI/UX:** Use `st.set_page_config`, columns, and expanders to make it look professional.
    4. **Dependencies:** Only use standard libraries + `streamlit`, `pandas`, `numpy`, `requests`, `matplotlib`, `plotly`.
    5. **Self-Contained:** If the app needs data, generate dummy data or use a public API. Do not ask the user to upload a file unless explicitly requested.
    
    ### OUTPUT FORMAT:
    Return ONLY the Python code. No markdown backticks, no explanations. Just the raw code.
    """
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            return f"# Error: API returned {response.status_code} - {response.text}"
            
        data = response.json()
        # Extract text from Gemini response structure
        try:
            text = data['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError):
            return "# Error: Unexpected response format from Gemini."

        # Clean markdown
        code = text.replace("```python", "").replace("```", "")
        return code
        
    except Exception as e:
        return f"# Error generating app: {str(e)}"

def generate_requirements(code):
    """Scans the code to generate requirements.txt"""
    reqs = ["streamlit"]
    if "pandas" in code: reqs.append("pandas")
    if "numpy" in code: reqs.append("numpy")
    if "requests" in code: reqs.append("requests")
    if "plotly" in code: reqs.append("plotly")
    if "matplotlib" in code: reqs.append("matplotlib")
    if "openai" in code: reqs.append("openai")
    
    return "\n".join(reqs)