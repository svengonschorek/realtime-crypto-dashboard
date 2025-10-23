import anthropic
import pandas as pd
import os, json

from history_data import get_data

def format_klines_compact(klines):
    """
    Convert klines to compact CSV format
    klines format: [[timestamp, open, high, low, close, volume], ...]
    """
    df = pd.DataFrame(klines, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    
    # Convert to CSV string (most compact)
    return df.to_csv(index=False, float_format='%.2f')

def create_trading_message_with_cache(klines_5m, klines_15m, klines_1h):
    """
    Create message with prompt caching for kline data
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    # Format klines compactly
    kline_data_5m = format_klines_compact(klines_5m)
    kline_data_15m = format_klines_compact(klines_15m)
    kline_data_1h = format_klines_compact(klines_1h)

    with open("system_prompt.txt", "r") as file:
        system_prompt = file.read()
    
    with open("user_prompt.txt", "r") as file:
        user_prompt = file.read()
    
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4096,
        system=[
            {
                "type": "text", 
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"}
            },
            {
                "type": "text",
                "text": f"Here is the kline data in CSV format for 5 min timeframe:\n\n{kline_data_5m}",
                "cache_control": {"type": "ephemeral"}
            },
            {
                "type": "text",
                "text": f"Here is the kline data in CSV format for 15 min timeframe:\n\n{kline_data_15m}",
                "cache_control": {"type": "ephemeral"}
            },
            {
                "type": "text",
                "text": f"Here is the kline data in CSV format for 1 hour timeframe:\n\n{kline_data_1h}",
                "cache_control": {"type": "ephemeral"}
            }
        ],
        messages=[
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )
    
    return response


klines_5m = get_data("SOL", "USDT", "5", 200)
klines_15m = get_data("SOL", "USDT", "15m", 200)
klines_1h = get_data("SOL", "USDT", "1h", 200)

response = create_trading_message_with_cache(klines_5m, klines_15m, klines_1h)

print(response.content[0].text)

# Save response to JSON file
now = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
file_name = f"analysis/analysis_SOL_USDT_{now}.json"
with open(file_name, "w") as file:
    json.dump(response.content[0].text, file)

# Check cache performance
print(f"\nCache stats:")
print(f"Input tokens: {response.usage.input_tokens}")
print(f"Cache creation tokens: {response.usage.cache_creation_input_tokens}")
print(f"Cache read tokens: {response.usage.cache_read_input_tokens}")
