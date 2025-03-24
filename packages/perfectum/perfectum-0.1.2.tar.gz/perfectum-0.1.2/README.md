_Perfectum_ -- chain-based text processing library aiming for simplicity and productivity.

# Usage

To install, run:

```bash
pip install perfectum[gpt,translate]
```

And then, edit the _main.py_ file:

```python
from perfectum.all import *

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
