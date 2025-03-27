# janus-python

Track and Verify LLM function calls with Janus.

## Installation

```bash
pip install janus-python
```

```python
from janus import Janus

load_dotenv()

def add(x: int, y: int) -> int:
    return x + y

def multiply(x: int, y: int) -> int:
    return x * y

janus = Janus(
    api_key=os.getenv("JANUS_API_KEY"), # Get this from withjanus.com
    timeout=10, # Automatically reject in 10 seconds
)

add = janus.track(add)
multiply = janus.verify(multiply)
```
