import os
from typing import Dict, Tuple, List

from components.html_generator.html_generator import HTMLGenerator



class WikipediaCollateralAdjectiveHTMLGenerator(HTMLGenerator):
    """
    HTML generator for Wikipedia collateral adjectives of animals
    """
    DEFAULT_CONFIG_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "wikipedia_html_generator_config.yaml"
    )

    def __init__(self, output_dir: str, output_file_name: str, config_path: str = DEFAULT_CONFIG_PATH):
        """
        WikipediaCollateralAdjectiveHTMLGenerator constructor
        :param output_dir: output directory
        :param output_file_name: output file name
        :param config_path: path to config file (yaml)
        """
        super().__init__(output_dir, output_file_name, config_path)

    def generate(self, mapping: Dict[str, List[Tuple[str]]]) -> str:
        """
        generates the HTML page for collateral adjectives of animals
        :param mapping: dictionary mapping collateral adjectives to list of animals tuple
        :return: the HTML page
        """
        html = self.config.get("html_start")

        for adj, animals_list in mapping.items():
            animal_cells = ""
            for animal in animals_list:
                name = animal[0]

                if os.path.exists(os.path.join(self.output_dir, f"{name.lower()}.jpg")):
                    img_path = os.path.join(self.output_dir, f"{name.lower()}.jpg")
                elif os.path.exists(os.path.join(self.output_dir, f"{name.lower()}.png")):
                    img_path = os.path.join(self.output_dir, f"{name.lower()}.png")
                else:
                    img_path = "No image found"
                # Each animal entry: name + clickable image + local path string
                animal_cells += f"""
                <div class="animal-entry">
                                        <a href="{img_path}">{name}</a><br/>
                                        <img src="{img_path}" alt="{name}"><br/>
                                        <span class="local-path">{img_path}</span>
                                        </div>"""

            html += f"""        <tr>
                <td>{adj}</td>
                <td>{animal_cells}</td>
                </tr>
                """

        html += self.config.get("html_end")

        return html
