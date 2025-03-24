_Perfectum_ -- chain-based text processing library aiming for simplicity and productivity.

# Usage

```python
from perfectum.chain.all import *

chain = Chain(
    [
        Translate("en"),
        Asciify(),
        Trim(),
        CollapseWhitespace(),
        Gpt("gpt-4o-mini", "Summarize the text in a less than 10 words."),
    ]
)
print(chain)

text = open("sample.text").read()
text = chain.process(text)
print(text)
```
