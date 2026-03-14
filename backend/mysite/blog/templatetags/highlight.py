from django import template
import re

register = template.Library()

@register.filter()
def highlight(text, word):
    if not word:
        return text
    pattern = re.compile(re.escape(word), re.IGNORECASE)
    return pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)