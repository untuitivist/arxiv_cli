from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any


ATOM_NS = {"atom": "http://www.w3.org/2005/Atom", "opensearch": "http://a9.com/-/spec/opensearch/1.1/"}


def parse_feed(xml_text: str) -> dict[str, Any]:
    root = ET.fromstring(xml_text)
    entries = [parse_entry(entry) for entry in root.findall("atom:entry", ATOM_NS)]
    return {
        "feed_title": _text(root, "atom:title"),
        "feed_id": _text(root, "atom:id"),
        "updated": _text(root, "atom:updated"),
        "total_results": _int_text(root, "opensearch:totalResults"),
        "start_index": _int_text(root, "opensearch:startIndex"),
        "items_per_page": _int_text(root, "opensearch:itemsPerPage"),
        "entries": entries,
    }


def parse_entry(entry: ET.Element) -> dict[str, Any]:
    links: dict[str, str] = {}
    for link in entry.findall("atom:link", ATOM_NS):
        href = link.attrib.get("href")
        if not href:
            continue
        rel = link.attrib.get("rel", "")
        title = link.attrib.get("title", "")
        key = title or rel or "alternate"
        links[key] = href
    return {
        "id": _text(entry, "atom:id"),
        "title": _clean_space(_text(entry, "atom:title")),
        "summary": _clean_space(_text(entry, "atom:summary")),
        "published": _text(entry, "atom:published"),
        "updated": _text(entry, "atom:updated"),
        "authors": [_text(author, "atom:name") for author in entry.findall("atom:author", ATOM_NS)],
        "categories": [category.attrib.get("term", "") for category in entry.findall("atom:category", ATOM_NS)],
        "primary_category": _primary_category(entry),
        "comment": _arxiv_field(entry, "comment"),
        "journal_ref": _arxiv_field(entry, "journal_ref"),
        "doi": _arxiv_field(entry, "doi"),
        "links": links,
    }


def _primary_category(entry: ET.Element) -> str | None:
    for child in entry:
        if child.tag.endswith("primary_category"):
            return child.attrib.get("term")
    return None


def _arxiv_field(entry: ET.Element, name: str) -> str | None:
    for child in entry:
        if child.tag.endswith(name):
            return _clean_space(child.text or "")
    return None


def _text(node: ET.Element, selector: str) -> str | None:
    child = node.find(selector, ATOM_NS)
    if child is None or child.text is None:
        return None
    return child.text


def _int_text(node: ET.Element, selector: str) -> int | None:
    text = _text(node, selector)
    if text is None:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def _clean_space(text: str | None) -> str | None:
    if text is None:
        return None
    return " ".join(text.split())
