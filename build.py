#! /usr/bin/env python3
# Based on https://github.com/simonw/simonw/
import feedparser
import pathlib
import re
import os

root = pathlib.Path(__file__).parent.resolve()

def replace_chunk(content, marker, chunk):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = f"<!-- {marker} starts -->\n{chunk}\n<!-- {marker} ends -->"
    return r.sub(chunk, content)


def fetch_blog_entries():
    entries = feedparser.parse("https://shriker.ca/journal/rss/")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": "%d/%02d/%02d" % (entry.published_parsed.tm_year, entry.published_parsed.tm_mon, entry.published_parsed.tm_mday),
        }
        for entry in entries
    ]


def fetch_portfolio():
    entries = feedparser.parse(
        "https://shriker.ca/tag/portfolio/rss/")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "image": entry["media_content"][0]["url"]
        }
        for entry in entries
    ]


def fetch_artwork():
    entries = feedparser.parse(
        "https://backend.deviantart.com/rss.xml?q=gallery%3Ashriker")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": "%d/%02d/%02d" % (entry.published_parsed.tm_year, entry.published_parsed.tm_mon, entry.published_parsed.tm_mday),
            "image": entry["media_thumbnail"][0]["url"]
        }
        for entry in entries
    ]


if __name__ == "__main__":
    readme = root / "README.md"

    readme_contents = readme.open(encoding="utf-8").read()

    # blog entries
    entries = fetch_blog_entries()[:5]
    entries_md = "\n".join(
        ["* [{title}]({url}) - {published}".format(**entry)
         for entry in entries]
    )
    rewritten = replace_chunk(readme_contents, "blog", entries_md)

    # artwork
    entries = fetch_portfolio()[:5]
    entries_md = "\n".join(
        ['<a href="{url}"><img src="{image}" alt="{title}" height="100"></a> '.format(**entry)
         for entry in entries]
    )
    rewritten = replace_chunk(rewritten, "portfolio", entries_md)

    # artwork
    entries = fetch_artwork()[:10]
    entries_md = "\n".join(
        ['<a href="{url}"><img src="{image}" alt="{title}" height="60"></a> '.format(**entry)
         for entry in entries]
    )
    rewritten = replace_chunk(rewritten, "artwork", entries_md)

    readme.open("w", encoding="utf-8").write(rewritten)
