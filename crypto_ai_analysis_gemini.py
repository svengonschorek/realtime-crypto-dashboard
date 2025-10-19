import markdown, webbrowser, tempfile

from google import genai
from crypto_history_data import get_data

klines_5m = get_data("SOL", "USDT", "5m")

with open("prompt.txt", "r") as file:
    prompt = file.read()

prompt_with_data = prompt + "\n\n5-minute K-line data:\n" + str(klines_5m)

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=prompt_with_data
)

html = markdown.markdown(response.text)

with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
    f.write(html)
    webbrowser.open('file://' + f.name)
