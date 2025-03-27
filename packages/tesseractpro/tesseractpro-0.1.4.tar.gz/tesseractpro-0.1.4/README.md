# Tesseract Pro Python API

-- This project is under active development. Please do not use in production before version 1.0.0 --

### Example

#### Get visible tools for current chart

```python
import time
from tesseractpro import TesseractPro

tpro = TesseractPro(
    api_token="Your-API-token"
)

candles = 100  # the amount of candles to fetch
chart = tpro.get_chart(
    space_id="cb0c8e03-62c6-4a1c-a872-18ed1c4c8f96",
    symbol="btcusdt",
    timeframe=32,
    start_time=int(time.time()),
    end_time=int(time.time()) - (32*60*candles)
)

for tool in chart.get_tools():
    print(f"Tool: {tool['id']} is {tool['type']})

```

#### Get OHLC candles for the timeframe of the current chart

```python
import time
from tesseractpro import TesseractPro

tpro = TesseractPro(
    api_token="[YOUR-API-TOKEN]"
)

candles = 100  # the amount of candles to fetch
chart = tpro.get_chart(
    space_id="[SPACE-ID]",
    symbol="btcusdt",
    timeframe=32,
    start_time=int(time.time()),
    end_time=int(time.time()) - (32*60*candles)
)

print(chart.get_candles())

```

#### Fetch BTCUSDT prices

```python
import time
from tesseractpro import TesseractPro

tpro = TesseractPro(
    api_token="[YOUR-API-TOKEN]"
)

candles = 100  # the amount of candles to fetch
chart = tpro.get_chart(
    space_id="[SPACE-ID]",
    symbol="btcusdt",
    timeframe=32,
    start_time=int(time.time()),
    end_time=int(time.time()) - (32*60*candles)
)

chart.on(chart.ON_PRICE, lambda data: print(data))

chart.wait_for_events()
```

#### Watch for tool updates on BTCUSDT 32min chart

```python
import time
from tesseractpro import TesseractPro

tpro = TesseractPro(
    api_token="[YOUR-API-TOKEN]"
)

candles = 100  # the amount of candles to fetch
chart = tpro.get_chart(
    space_id="[SPACE-ID]",
    symbol="btcusdt",
    timeframe=32,
    start_time=int(time.time()),
    end_time=int(time.time()) - (32*60*candles)
)

chart.on(chart.ON_TOOL_UPDATE, lambda data: print(f"Updated tool {data['id']}"))

chart.wait_for_events()
```
