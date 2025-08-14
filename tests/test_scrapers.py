import pytest
from bs4 import BeautifulSoup

from components.scrapers.base_scrapers import BaseHTMLScraper, BaseTableScraper, TableMappingScraper
from components.scrapers.extractors.base_extractor import BaseCellsExtractor
from tests.tests_data.test_data import good_url, mock_html_table, mock_html_table_headers, mapping_dict_result


def test_base_html_scraper():
    scraper = BaseHTMLScraper(url=good_url)
    assert scraper is not None, "BaseHTMLScraper should not be None"
    assert scraper.soup is not None, "BaseHTMLScraper soup should not be None"


@pytest.mark.parametrize(
    "skip_header, expected_row_texts",
    [
        (True, ["Row1Col1", "Row2Col1"]),
        (False, ["Header1", "Row1Col1", "Row2Col1"]),
    ]
)
def test_base_table_scraper(skip_header, expected_row_texts):
    soup = BeautifulSoup(mock_html_table, "html.parser")
    table_tag = soup.find("table")
    scraper = BaseTableScraper(table_tag)

    rows = scraper.rows(skip_header=skip_header)

    assert len(rows) == len(expected_row_texts), f"Expected {len(expected_row_texts)} rows, got {len(rows)}"

    for row, expected_text in zip(rows, expected_row_texts):
        cell_text = row.td.text if row.td else row.th.text
        assert cell_text == expected_text, f"Expected '{expected_text}', instead got '{cell_text}'"


def test_table_mapping_scraper():
    soup = BeautifulSoup(mock_html_table, "html.parser")
    table_tag = soup.find("table")
    mapping_dict = TableMappingScraper(
        table=table_tag,
        keys_extractor=BaseCellsExtractor(col_idx=0),
        values_extractor=BaseCellsExtractor(col_idx=1)
        ).create_mapping()

    assert mapping_dict == mapping_dict_result, f"Should got {mapping_dict_result}, instead got {mapping_dict}"