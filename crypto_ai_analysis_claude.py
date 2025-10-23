import markdown, webbrowser, tempfile
import os

from binance.crypto_history_data_binance import get_data
from anthropic import Anthropic

klines_5m = get_data("SOL", "USDT", "5m")

with open("prompt.txt", "r") as file:
    prompt = file.read()

prompt_with_data = prompt + "\n\n5-minute K-line data:\n" + str(klines_5m)


client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),  # This is the default and can be omitted
)

message = client.messages.create(
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": prompt_with_data,
        }
    ],
    model="claude-sonnet-4-5-20250929",
)

html = markdown.markdown(message.content[0].text)

with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
    f.write(html)
    webbrowser.open('file://' + f.name)
