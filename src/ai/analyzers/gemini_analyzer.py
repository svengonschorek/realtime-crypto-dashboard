import markdown, webbrowser, tempfile
import os, sys

from google import genai

# Add the project root to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, "..", "..", "..")
sys.path.append(os.path.abspath(project_root))

from src.api.bybit.history_data import get_data

klines_5m = get_data("SOL", "USDT", "5")

prompts_dir = os.path.join(script_dir, "..", "prompts")

with open(os.path.join(prompts_dir, "user_prompt.txt"), "r") as file:
    user_prompt = file.read()

prompt_with_data = user_prompt + "\n\n5-minute K-line data:\n" + str(klines_5m)

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=prompt_with_data
)

html = markdown.markdown(response.text)

with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
    f.write(html)
    webbrowser.open('file://' + f.name)
