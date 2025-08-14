import tempfile
import os

from components.html_generator.wikipedia_html_generators import WikipediaCollateralAdjectiveHTMLGenerator
from tests.tests_data.test_data import mapping_dict


def test_wikipedia_animal_html_generate_and_save():
    with (tempfile.TemporaryDirectory() as tmpdir):
        generator = WikipediaCollateralAdjectiveHTMLGenerator(output_dir=tmpdir, output_file_name="test")
        generator.generate_and_save(data=mapping_dict)

        assert os.path.exists(os.path.join(tmpdir, "test.html")), \
        f"WikipediaCollateralAdjectiveHTMLGenerator failed to generate {os.path.join(tmpdir, 'test.html')}"

