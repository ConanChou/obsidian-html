import regex as re
from oboe.utils import slug_case, md_link


def format_tags(document, tags):
    """Obsidian style tags. Removes #-icon and adds a span tag."""
    for tag in tags:
        document = document.replace("#" + tag, "<span class=\"tag\">" + tag + "</span>")

    return document


def format_blockrefs(document):
    """Formats Obsidian block references into a span element that can be linked to"""
    regex = re.compile(r" \^(.+)$", re.MULTILINE)
    matches = regex.finditer(document)

    for match in matches:
        document = document.replace(match.group(), f"<span id=\"{match.group(1)}\"></span>")

    return document

def format_highlights(document):
    """Formats the '==highlight==' directly into HTML."""
    regex = re.compile(r"==(.*?)==")
    matches = regex.finditer(document)

    for match in matches:
        document = document.replace(match.group(), f"<mark class=\"highlight\">{match.group(1)}</mark>)")

    return document

def format_url(document):
    regex = re.compile(r'(^\s*---.*---\s*$)(.*)')
    matches = regex.search(document, re.MULTILINE|re.DOTALL)
    if matches:
        front_matter = matches[0].group(1)
        content = matches[1].group(2)
    else:
        front_matter = ''
        content = document

    regex = re.compile(r'(?<!"|\()(http[s]*://[^\s)]*)(?<!\.)|(?<!])[(](http[s]*://[^\s)]*)')
    matches = regex.finditer(content)

    for match in matches:
        url = match.group(1) or match.group(2)
        content = content.replace(match.group(), f"[{url}]({url})")

    return front_matter + document

def format_links(document, links):
    for link in links:
        document = document.replace(f"[[{link.obsidian_link}]]", link.md_link())

    return document

def format_embeds(document, embeds):
    for embed in embeds:
        document = document.replace(f"![[{embed.obsidian_link}]]", embed.md_embed())

    return document

def format_code_blocks(document):
    regex = re.compile(r"```(.*)$\n([\S\s]*?)\n```", re.MULTILINE)
    matches = regex.finditer(document)

    for match in matches:
        # Format as plaintext if not language specified
        lang = match.group(1) if match.group(1) else "plaintext"
        document = document.replace(match.group(),
                    f"<pre><code class=\"{lang} lang-{lang} language-{lang}\">{match.group(2)}</code></pre>")

    return document
