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

## Multi-level chaining

```python
from perfectum.all import *

normalize = Chain(
    [
        Asciify(),
        TabToWhitespace(),
        CollapseWhitespace(),
        Trim(),
    ]
)

translate_and_generate_poem = Chain(
    [
        Translate("en"),
        Gpt("gpt-4o-mini", "Write a short poem using text provided by user."),
    ]
)

chain = Chain(
    [
        normalize,
        translate_and_generate_poem,
    ]
)

text = "Привет! Я слышал, что ты сломала ногу позавчера. Как ты себя чувствуешь?"
text = chain.process(text)
print(text)
```

As you can see, processing text becomes straightforward by creating separate chains for each task and then combining them into a single chain.
