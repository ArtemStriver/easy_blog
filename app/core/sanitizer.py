from typing import Iterable, Dict
import re
import html
import bleach
from bleach.linkifier import Linker

"""
Модуль для санитизации HTML-контента.
Использует библиотеку bleach для очистки HTML от опасных тегов и атрибутов.
--sanitize_html: очистка HTML-контента: удаляет запрещённые теги/атрибуты, комментарии и т.д.
  Возвращает безопасный HTML, который можно рендерить в браузере.
--html_to_text: превращает HTML-контент в "краткий текстовый превью"
    - Удаляет все теги (без сохранения <br> в новые строки).
    - Декодирует HTML-сущности (&amp; -> &).
    - Обрезает строку до max_length, сохраняя целые слова, добавляет ellipsis.
"""

ALLOWED_TAGS = [
    "p", "br", "strong", "em", "ul", "ol", "li", "a",
    "h1", "h2", "h3", "h4", "blockquote", "code", "pre"
]

ALLOWED_ATTRIBUTES: Dict[str, Iterable[str]] = {
    "a": ["href", "title", "rel", "target", "referrerpolicy"],
}

BLEACH_CLEAN_KWARGS = {
    "tags": ALLOWED_TAGS,
    "attributes": ALLOWED_ATTRIBUTES,
    "strip": True,
    "strip_comments": True,
}

linker = Linker(callbacks=[
    lambda attrs, new: attrs.update({
        "rel": "nofollow noopener noreferrer",
        "target": "_blank",
    }) or attrs
])


def sanitize_html(content: str) -> str:
    if not content:
        return ""

    content = str(content)
    content = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]+", "", content)
    cleaned = bleach.clean(content, **BLEACH_CLEAN_KWARGS)
    linkified = linker.linkify(cleaned)

    return linkified

def html_to_text(content: str, max_length: int = 200, ellipsis: str = "…") -> str:
    if not content:
        return ""

    cleaned_html = bleach.clean(content, tags=[], strip=True, strip_comments=True)
    text = html.unescape(cleaned_html)
    text = re.sub(r"\s+", " ", text).strip()

    if len(text) <= max_length:
        return text

    cut = text[: max_length + 1]
    last_space = cut.rfind(" ")
    if last_space == -1:
        return cut[:max_length].rstrip() + ellipsis
    return cut[:last_space].rstrip() + ellipsis
