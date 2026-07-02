#!/usr/bin/env python3
"""
Retail Location Intelligence Knowledge Updater (Idea 210)

Crawls geomarketing literature, retail real-estate research, and location science
publications to extract methods, benchmarks, and best practices. Deduplicates by URL
hash and appends dated entries to SECOND-KNOWLEDGE-BRAIN.md for continuous learning.

Usage:
    python knowledge_updater.py                    # Run full crawl
    python knowledge_updater.py --dry-run          # Preview without writing
    python knowledge_updater.py --source cbre      # Crawl specific source only
    python knowledge_updater.py --force            # Re-crawl all sources

Requirements:
    - requests
    - beautifulsoup4
    - feedparser (for RSS feeds)
    - html2text (for content extraction)
    - python-dateutil (for date parsing)

Author: Retail Location Intelligence (Idea 210)
Version: 1.0
"""

from __future__ import annotations

import argparse
import hashlib
import logging
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
    import feedparser
    import html2text
    from dateutil import parser as date_parser
except ImportError as e:
    print(f"Missing required library: {e}")
    print("Install with: pip install requests beautifulsoup4 feedparser html2text python-dateutil")
    sys.exit(1)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('knowledge_updater.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


# Constants
BRAIN_FILE = Path(__file__).resolve().parent.parent / "SECOND-KNOWLEDGE-BRAIN.md"
USER_AGENT = "Mozilla/5.0 (compatible; RetailLocationIntelligence/1.0; +https://github.com/retail-location-intelligence)"
REQUEST_TIMEOUT = 30
MAX_CONTENT_LENGTH = 500000  # 500KB max per page


# Data sources configuration
SOURCES = {
    "arxiv_spatial_econ": {
        "url": "https://arxiv.org/list/econ.GN/recent",
        "type": "html",
        "parser": "parse_arxiv",
        "enabled": True
    },
    "ssrn_retail": {
        "url": "https://papers.ssrn.com/sol3/Results.cfm",
        "type": "html",
        "parser": "parse_ssrn",
        "enabled": False  # Requires scraping, may have rate limits
    },
    "cbre_research": {
        "url": "https://www.cbre.com/research-and-reports",
        "type": "html",
        "parser": "parse_cbre",
        "enabled": True
    },
    "jll_research": {
        "url": "https://www.jll.com/en/research",
        "type": "html",
        "parser": "parse_jll",
        "enabled": True
    },
    "icsc": {
        "url": "https://www.icsc.org/press-releases/",
        "type": "html",
        "parser": "parse_icsc",
        "enabled": True
    },
    "nrf_research": {
        "url": "https://nrf.com/research",
        "type": "html",
        "parser": "parse_nrf",
        "enabled": True
    },
    "urban_land_institute": {
        "url": "https://uli.org/research/",
        "type": "html",
        "parser": "parse_uli",
        "enabled": True
    },
    "icsc_research_foundation": {
        "url": "https://www.icsc.org/research-foundation/",
        "type": "html",
        "parser": "parse_icsc_rf",
        "enabled": True
    }
}


# Keywords for relevance scoring
KEYWORDS = [
    "trade area", "trade-area", "catchment",
    "huff model", "huff gravity", "gravity model",
    "reilly", "retail gravitation",
    "christaller", "central place",
    "saturation", "market saturation", "retail saturation",
    "footfall", "foot traffic", "pedestrian",
    "site selection", "retail location", "location intelligence",
    "geomarketing", "geo-marketing",
    "retail real estate", "commercial real estate",
    "market area", "service area", "trade area analysis",
    "analog method", "sales forecasting retail",
    "retail demographics", "consumer spending",
    "retail analytics", "location analytics"
]


@dataclass
class KnowledgeEntry:
    """A single knowledge entry from crawling."""
    title: str
    url: str
    authors: str
    year: int | None
    venue: str
    summary: str
    relevance_score: float
    date_found: date

    def to_markdown(self) -> str:
        """Convert entry to markdown format for brain file."""
        h = self._url_hash()
        return (
            f"- {self.date_found.isoformat()} — **{self.title}** "
            f"({self.authors}, {self.year or 'n.d.'}, {self.venue}) "
            f"[{self.url}] <!--h:{h}-->\n"
        )

    def _url_hash(self) -> str:
        """Generate 12-character hash of URL for deduplication."""
        return hashlib.sha256(self.url.encode()).hexdigest()[:12]


def url_hash(url: str) -> str:
    """Generate URL hash for deduplication."""
    return hashlib.sha256(url.encode()).hexdigest()[:12]


def get_existing_hashes(brain_path: Path) -> set[str]:
    """Extract all existing URL hashes from brain file."""
    if not brain_path.exists():
        return set()

    text = brain_path.read_text(encoding="utf-8")
    return set(re.findall(r"<!--h:([0-9a-f]{12})-->", text))


def make_request(url: str, session: requests.Session | None = None) -> requests.Response | None:
    """Make HTTP request with error handling."""
    if session is None:
        session = requests.Session()

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive"
    }

    try:
        response = session.get(url, headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return None


def calculate_relevance(text: str) -> float:
    """
    Calculate relevance score based on keyword matches.

    Returns score from 0.0 to 1.0, where:
    - 1.0 = multiple high-value keywords present
    - 0.5 = some relevant keywords
    - 0.0 = no relevant keywords
    """
    text_lower = text.lower()

    # High-value keywords (core concepts)
    high_value = [
        "huff model", "gravity model", "reilly", "christaller",
        "trade area", "catchment", "saturation", "site selection"
    ]

    # Medium-value keywords (related concepts)
    medium_value = [
        "retail location", "geomarketing", "footfall", "market area",
        "retail real estate", "location analytics", "analog method"
    ]

    # Low-value keywords (peripheral)
    low_value = [
        "demographics", "consumer spending", "retail analytics",
        "commercial real estate", "retail"
    ]

    score = 0.0

    for keyword in high_value:
        if keyword in text_lower:
            score += 0.3

    for keyword in medium_value:
        if keyword in text_lower:
            score += 0.15

    for keyword in low_value:
        if keyword in text_lower:
            score += 0.05

    # Bonus for multiple matches
    if score > 0:
        score += min(score * 0.2, 0.2)  # Max 20% bonus

    return min(score, 1.0)


def extract_text_from_html(html_content: str) -> str:
    """Extract clean text from HTML using html2text."""
    try:
        converter = html2text.HTML2Text()
        converter.ignore_links = False
        converter.ignore_images = True
        converter.ignore_emphasis = False
        converter.body_width = 0  # Don't wrap lines
        return converter.handle(html_content)
    except Exception as e:
        logger.warning(f"HTML to text conversion failed: {e}")
        # Fallback to BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(separator=' ', strip=True)


def parse_date(date_str: str | None, default_year: int | None = None) -> int | None:
    """Parse year from various date formats."""
    if not date_str:
        return default_year

    try:
        # Try ISO format first
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.year
    except (ValueError, AttributeError):
        pass

    try:
        # Try dateutil parser
        dt = date_parser.parse(date_str)
        return dt.year
    except (ValueError, AttributeError):
        pass

    # Try to extract 4-digit year
    year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
    if year_match:
        return int(year_match.group())

    # Check if it's just a year
    if date_str.isdigit() and 1900 <= int(date_str) <= date.today().year + 1:
        return int(date_str)

    return default_year


# Source-specific parsers

def parse_arxiv(response: requests.Response, base_url: str) -> list[KnowledgeEntry]:
    """Parse arXiv spatial economics listing."""
    soup = BeautifulSoup(response.text, 'html.parser')
    entries = []

    # arXiv lists papers in <dl> with <dt> for IDs and <dd> for titles/abstracts
    dl = soup.find('dl')
    if not dl:
        logger.warning("No paper list found in arXiv response")
        return entries

    current_id = None
    current_title = None
    current_authors = []
    current_abstract = None

    for element in dl.children:
        if element.name == 'dt':
            # Extract paper ID and URL
            list_id = element.find('span', class_='list-identifier')
            if list_id:
                current_id = list_id.get_text(strip=True)
                link = element.find('a')
                if link and link.get('href'):
                    current_id = link.get('href')

        elif element.name == 'dd':
            # Extract title
            title_div = element.find('div', class_='list-title mathjax')
            if title_div:
                title_text = title_div.get_text(' ', strip=True)
                current_title = title_text.replace('Title:', '', 1).strip()

            # Extract authors
            authors_div = element.find('div', class_='list-authors')
            if authors_div:
                author_links = authors_div.find_all('a')
                current_authors = [a.get_text(strip=True) for a in author_links]

            # Extract abstract
            abstract_div = element.find('div', class_='list-abstract mathjax')
            if abstract_div:
                current_abstract = abstract_div.get_text(' ', strip=True).replace('Abstract:', '', 1).strip()

            # Create entry if we have required fields
            if current_title and current_id:
                # Get year from ID (arXiv IDs contain year like 2301.12345)
                year = None
                id_match = re.search(r'arXiv:(\d{4})', str(current_id))
                if id_match:
                    year = int(id_match.group(1))

                text_for_relevance = f"{current_title} {current_abstract or ''}"
                relevance = calculate_relevance(text_for_relevance)

                if relevance > 0.1:  # Only include if somewhat relevant
                    entry = KnowledgeEntry(
                        title=current_title,
                        url=f"https://arxiv.org/abs/{current_id.split('/')[-1]}" if '/' in str(current_id) else f"https://arxiv.org/abs/{current_id}",
                        authors=', '.join(current_authors) if current_authors else 'Unknown',
                        year=year,
                        venue='arXiv Spatial Economics',
                        summary=current_abstract[:500] if current_abstract else '',
                        relevance_score=relevance,
                        date_found=date.today()
                    )
                    entries.append(entry)

                # Reset for next entry
                current_id = None
                current_title = None
                current_authors = []
                current_abstract = None

    return entries


def parse_cbre(response: requests.Response, base_url: str) -> list[KnowledgeEntry]:
    """Parse CBRE research reports listing."""
    soup = BeautifulSoup(response.text, 'html.parser')
    entries = []

    # CBRE reports are typically in cards or list items
    report_items = soup.find_all(['div', 'article'], class_=re.compile(r'report|research|insight', re.I))

    for item in report_items[:20]:  # Limit to 20 most recent
        # Try to find title and link
        title_elem = item.find(['h2', 'h3', 'h4', 'a'])
        if not title_elem:
            continue

        if title_elem.name == 'a':
            link = title_elem
            title = title_elem.get_text(strip=True)
        else:
            link = title_elem.find('a')
            title = title_elem.get_text(strip=True)

        if not link or not link.get('href'):
            continue

        url = urljoin(base_url, link.get('href'))

        # Try to extract date
        date_elem = item.find(['time', 'span'], class_=re.compile(r'date|time', re.I))
        year = None
        if date_elem:
            date_text = date_elem.get('datetime') or date_elem.get_text(strip=True)
            year = parse_date(date_text)

        # Try to extract summary
        summary_elem = item.find(['p', 'div'], class_=re.compile(r'summary|abstract|description', re.I))
        summary = summary_elem.get_text(strip=True)[:500] if summary_elem else ''

        text_for_relevance = f"{title} {summary}"
        relevance = calculate_relevance(text_for_relevance)

        if relevance > 0.1:
            entry = KnowledgeEntry(
                title=title,
                url=url,
                authors='CBRE Research',
                year=year or date.today().year,
                venue='CBRE Research Report',
                summary=summary,
                relevance_score=relevance,
                date_found=date.today()
            )
            entries.append(entry)

    return entries


def parse_jll(response: requests.Response, base_url: str) -> list[KnowledgeEntry]:
    """Parse JLL research reports listing."""
    soup = BeautifulSoup(response.text, 'html.parser')
    entries = []

    # JLL reports are typically in article or card elements
    report_items = soup.find_all(['article', 'div'], class_=re.compile(r'research|report|insight', re.I))

    for item in report_items[:20]:
        title_link = item.find('a', href=True)
        if not title_link:
            continue

        title = title_link.get_text(strip=True)
        url = urljoin(base_url, title_link.get('href'))

        # Extract date
        time_elem = item.find('time')
        year = None
        if time_elem and time_elem.get('datetime'):
            year = parse_date(time_elem.get('datetime'))

        # Extract summary
        summary_elem = item.find('p')
        summary = summary_elem.get_text(strip=True)[:500] if summary_elem else ''

        text_for_relevance = f"{title} {summary}"
        relevance = calculate_relevance(text_for_relevance)

        if relevance > 0.1:
            entry = KnowledgeEntry(
                title=title,
                url=url,
                authors='JLL Research',
                year=year or date.today().year,
                venue='JLL Research Report',
                summary=summary,
                relevance_score=relevance,
                date_found=date.today()
            )
            entries.append(entry)

    return entries


def parse_icsc(response: requests.Response, base_url: str) -> list[KnowledgeEntry]:
    """Parse ICSC press releases and research."""
    soup = BeautifulSoup(response.text, 'html.parser')
    entries = []

    # ICSC content in articles or cards
    items = soup.find_all(['article', 'div'], class_=re.compile(r'press|news|article', re.I))

    for item in items[:20]:
        title_link = item.find('a', href=True)
        if not title_link:
            continue

        title = title_link.get_text(strip=True)
        url = urljoin(base_url, title_link.get('href'))

        # Extract date
        time_elem = item.find('time')
        year = None
        if time_elem and time_elem.get('datetime'):
            year = parse_date(time_elem.get('datetime'))

        # Extract summary
        summary_elem = item.find(['p', 'div'], class_=re.compile(r'excerpt|summary|description', re.I))
        summary = summary_elem.get_text(strip=True)[:500] if summary_elem else ''
        if not summary:
            # Fallback to first paragraph
            p_elem = item.find('p')
            summary = p_elem.get_text(strip=True)[:500] if p_elem else ''

        text_for_relevance = f"{title} {summary}"
        relevance = calculate_relevance(text_for_relevance)

        if relevance > 0.1:
            entry = KnowledgeEntry(
                title=title,
                url=url,
                authors='ICSC',
                year=year or date.today().year,
                venue='ICSC' + (' Press Release' if 'press' in str(item.get('class')).lower() else ' Research'),
                summary=summary,
                relevance_score=relevance,
                date_found=date.today()
            )
            entries.append(entry)

    return entries


def parse_nrf(response: requests.Response, base_url: str) -> list[KnowledgeEntry]:
    """Parse NRF research publications."""
    soup = BeautifulSoup(response.text, 'html.parser')
    entries = []

    # NRF research in articles or list items
    items = soup.find_all(['article', 'div', 'li'], class_=re.compile(r'research|report|study', re.I))

    for item in items[:15]:
        title_link = item.find('a', href=True)
        if not title_link:
            continue

        title = title_link.get_text(strip=True)
        url = urljoin(base_url, title_link.get('href'))

        # Extract date
        time_elem = item.find('time') or item.find(['span', 'div'], class_=re.compile(r'date', re.I))
        year = None
        if time_elem:
            date_text = time_elem.get('datetime') or time_elem.get_text(strip=True)
            year = parse_date(date_text)

        # Extract summary
        summary_elem = item.find(['p', 'div'], class_=re.compile(r'description|summary|excerpt', re.I))
        summary = summary_elem.get_text(strip=True)[:500] if summary_elem else ''

        text_for_relevance = f"{title} {summary}"
        relevance = calculate_relevance(text_for_relevance)

        if relevance > 0.1:
            entry = KnowledgeEntry(
                title=title,
                url=url,
                authors='NRF Research',
                year=year or date.today().year,
                venue='NRF Research',
                summary=summary,
                relevance_score=relevance,
                date_found=date.today()
            )
            entries.append(entry)

    return entries


def parse_uli(response: requests.Response, base_url: str) -> list[KnowledgeEntry]:
    """Parse Urban Land Institute research."""
    soup = BeautifulSoup(response.text, 'html.parser')
    entries = []

    # ULI content in cards or articles
    items = soup.find_all(['article', 'div'], class_=re.compile(r'card|report|research|publication', re.I))

    for item in items[:15]:
        title_link = item.find('a', href=True)
        if not title_link:
            continue

        title = title_link.get_text(strip=True)
        url = urljoin(base_url, title_link.get('href'))

        # Extract date
        time_elem = item.find('time') or item.find(['span', 'div'], class_=re.compile(r'date|year', re.I))
        year = None
        if time_elem:
            date_text = time_elem.get('datetime') or time_elem.get_text(strip=True)
            year = parse_date(date_text)

        # Extract summary
        summary_elem = item.find(['p', 'div'], class_=re.compile(r'description|summary|excerpt', re.I))
        summary = summary_elem.get_text(strip=True)[:500] if summary_elem else ''

        text_for_relevance = f"{title} {summary}"
        relevance = calculate_relevance(text_for_relevance)

        if relevance > 0.1:
            entry = KnowledgeEntry(
                title=title,
                url=url,
                authors='Urban Land Institute',
                year=year or date.today().year,
                venue='ULI Research',
                summary=summary,
                relevance_score=relevance,
                date_found=date.today()
            )
            entries.append(entry)

    return entries


def parse_icsc_rf(response: requests.Response, base_url: str) -> list[KnowledgeEntry]:
    """Parse ICSC Research Foundation publications."""
    soup = BeautifulSoup(response.text, 'html.parser')
    entries = []

    # ICSC RF publications
    items = soup.find_all(['article', 'div', 'li'], class_=re.compile(r'publication|research|report', re.I))

    for item in items[:15]:
        title_link = item.find('a', href=True)
        if not title_link:
            continue

        title = title_link.get_text(strip=True)
        url = urljoin(base_url, title_link.get('href'))

        # Extract date
        time_elem = item.find('time') or item.find(['span', 'div'], class_=re.compile(r'date|year', re.I))
        year = None
        if time_elem:
            date_text = time_elem.get('datetime') or time_elem.get_text(strip=True)
            year = parse_date(date_text)

        # Extract summary
        summary_elem = item.find(['p', 'div'], class_=re.compile(r'description|summary|excerpt', re.I))
        summary = summary_elem.get_text(strip=True)[:500] if summary_elem else ''

        text_for_relevance = f"{title} {summary}"
        relevance = calculate_relevance(text_for_relevance)

        if relevance > 0.1:
            entry = KnowledgeEntry(
                title=title,
                url=url,
                authors='ICSC Research Foundation',
                year=year or date.today().year,
                venue='ICSC Research Foundation',
                summary=summary,
                relevance_score=relevance,
                date_found=date.today()
            )
            entries.append(entry)

    return entries


def fetch_source(source_name: str, source_config: dict, session: requests.Session) -> list[KnowledgeEntry]:
    """Fetch entries from a single source."""
    if not source_config.get('enabled', False):
        logger.info(f"Source '{source_name}' is disabled, skipping")
        return []

    logger.info(f"Fetching from {source_name}...")

    url = source_config['url']
    parser_name = source_config.get('parser', 'generic')

    response = make_request(url, session)
    if not response:
        logger.warning(f"Failed to fetch from {source_name}")
        return []

    # Get appropriate parser function
    parsers = {
        'parse_arxiv': parse_arxiv,
        'parse_ssrn': parse_ssrn,  # Not implemented, would return empty
        'parse_cbre': parse_cbre,
        'parse_jll': parse_jll,
        'parse_icsc': parse_icsc,
        'parse_nrf': parse_nrf,
        'parse_uli': parse_uli,
        'parse_icsc_rf': parse_icsc_rf
    }

    parser_func = parsers.get(parser_name)
    if not parser_func:
        logger.warning(f"No parser found for {parser_name}, skipping")
        return []

    try:
        entries = parser_func(response, url)
        logger.info(f"Found {len(entries)} entries from {source_name}")
        return entries
    except Exception as e:
        logger.error(f"Error parsing {source_name}: {e}")
        return []


def fetch_all_sources(sources: dict | None = None, session: requests.Session | None = None) -> list[KnowledgeEntry]:
    """Fetch entries from all enabled sources."""
    if sources is None:
        sources = SOURCES

    if session is None:
        session = requests.Session()

    all_entries = []

    for source_name, source_config in sources.items():
        if not source_config.get('enabled', False):
            continue

        entries = fetch_source(source_name, source_config, session)
        all_entries.extend(entries)

    return all_entries


def append_entries_to_brain(entries: list[KnowledgeEntry], brain_path: Path, dry_run: bool = False) -> int:
    """Append new entries to brain file, avoiding duplicates."""
    if not entries:
        logger.info("No entries to append")
        return 0

    # Get existing hashes
    existing_hashes = get_existing_hashes(brain_path)

    # Filter out duplicates
    new_entries = []
    for entry in entries:
        h = entry._url_hash()
        if h not in existing_hashes and entry.url:
            new_entries.append(entry)
            existing_hashes.add(h)

    if not new_entries:
        logger.info("All entries already exist in brain file")
        return 0

    # Sort by relevance (descending) then date
    new_entries.sort(key=lambda e: (e.relevance_score, e.date_found), reverse=True)

    # Generate markdown
    markdown_lines = []
    for entry in new_entries:
        markdown_lines.append(entry.to_markdown())

    if dry_run:
        logger.info(f"DRY RUN: Would append {len(new_entries)} entries")
        for entry in new_entries:
            logger.info(f"  - {entry.title} ({entry.url})")
        return len(new_entries)

    # Ensure brain file exists
    brain_path.parent.mkdir(parents=True, exist_ok=True)

    # Read existing content or create new
    if brain_path.exists():
        existing_content = brain_path.read_text(encoding="utf-8")
    else:
        existing_content = """# SECOND-KNOWLEDGE-BRAIN — Retail Location Intelligence (Idea 210)

## Core Concepts & Frameworks
- **Huff Model (1964)** — probability a consumer patronizes a store = (attractiveness / distance^λ) normalized across alternatives; λ = distance-decay parameter. Primary demand estimator.
- **Reilly's Law of Retail Gravitation (1931)** — trade boundary between two centers proportional to population, inversely to distance squared.
- **Christaller Central Place Theory (1933)** — hierarchy of centers, threshold and range of goods; explains saturation/spacing.
- **Applebaum Analog Method** — estimate sales by comparing to analogous existing stores' per-capita capture.
- **Trade area / catchment** — primary (60–70% of customers), secondary, tertiary rings.
- **Site-selection criteria** — accessibility, visibility, footfall, co-tenancy, parking, rent, zoning.

## Knowledge Update Log

"""

    # Find or create Knowledge Update Log section
    if "## Knowledge Update Log" in existing_content:
        # Append to existing log section
        insert_point = existing_content.find("## Knowledge Update Log") + len("## Knowledge Update Log")
        new_content = existing_content[:insert_point] + "\n" + "\n".join(markdown_lines) + "\n" + existing_content[insert_point:]
    else:
        # Add log section at end
        new_content = existing_content.rstrip() + "\n\n## Knowledge Update Log\n" + "\n".join(markdown_lines) + "\n"

    # Write updated content
    brain_path.write_text(new_content, encoding="utf-8")
    logger.info(f"Appended {len(new_entries)} new entries to {brain_path.name}")

    return len(new_entries)


def main():
    parser = argparse.ArgumentParser(
        description='Update Retail Location Intelligence knowledge base',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python knowledge_updater.py                    # Run full crawl
  python knowledge_updater.py --dry-run          # Preview without writing
  python knowledge_updater.py --source cbre      # Crawl specific source only
  python knowledge_updater.py --force            # Re-crawl all sources

Sources:
  """ + ", ".join(SOURCES.keys())
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would be added without writing to brain file'
    )

    parser.add_argument(
        '--source',
        choices=list(SOURCES.keys()),
        help='Fetch from specific source only'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Fetch from all sources including disabled ones'
    )

    args = parser.parse_args()

    # Prepare sources
    if args.source:
        sources_to_fetch = {args.source: SOURCES[args.source]}
        if args.force:
            sources_to_fetch[args.source]['enabled'] = True
    else:
        sources_to_fetch = SOURCES.copy()
        if not args.force:
            sources_to_fetch = {k: v for k, v in sources_to_fetch.items() if v.get('enabled', False)}

    logger.info("Starting knowledge update crawl...")
    logger.info(f"Fetching from {len(sources_to_fetch)} source(s): {', '.join(sources_to_fetch.keys())}")

    # Fetch entries
    session = requests.Session()
    entries = fetch_all_sources(sources_to_fetch, session)

    if not entries:
        logger.warning("No entries found from any source")
        return

    # Filter by minimum relevance
    min_relevance = 0.15
    relevant_entries = [e for e in entries if e.relevance_score >= min_relevance]
    logger.info(f"Filtered to {len(relevant_entries)} relevant entries (relevance >= {min_relevance})")

    # Append to brain
    count = append_entries_to_brain(relevant_entries, BRAIN_FILE, dry_run=args.dry_run)

    if not args.dry_run:
        logger.info(f"✓ Knowledge update complete: {count} new entries added")
    else:
        logger.info(f"✓ Dry run complete: {count} entries would be added")


if __name__ == "__main__":
    main()
