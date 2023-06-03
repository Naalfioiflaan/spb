from django import template

register = template.Library()

@register.filter
def split_into_paragraphs(text):
    paragraphs = []
    current_paragraph = ""
    period_count = 0
    char_count = 0

    for char in text:
        current_paragraph += char
        char_count += 1

        if char == '.':
            period_count += 1

            if period_count == 4:
                if char_count <= 4:
                    period_count -= 1
                else :
                    paragraphs.append(current_paragraph.strip())
                    current_paragraph = ""
                    period_count = 0
            char_count = 0

    if current_paragraph:
        paragraphs.append(current_paragraph.strip())

    return paragraphs
