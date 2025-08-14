import os

from datetime import date

HTML_START = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Animal Collateral Adjectives</title>
    <style>
        body { font-family: Arial, sans-serif; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; vertical-align: top; }
        th { background-color: #f4f4f4; }
        img { max-width: 150px; max-height: 150px; display: block; margin-top: 4px; }
        .animal-entry { margin-bottom: 12px; }
        .local-path { font-size: 0.85em; color: #555; }
    </style>
</head>
<body>
    <h1>Animal Collateral Adjectives</h1>
    <table>
        <tr>
            <th>Collateral Adjective</th>
            <th>Animals</th>
        </tr>
"""
HTML_END = f"""    </table>
    <p><em>Generated on: {date.today()}</em></p>
</body>
</html>"""

def generate_html(mapping, file_name: str = "assignment_output", tmp_dir: str = "/tmp"):
    html = HTML_START

    for adj, animals_list in mapping.items():
        animal_cells = ""
        for animal in animals_list:
            name = animal["name"]
            if os.path.exists(f"{tmp_dir}/{name.lower()}.jpg"):
                img_path = f"{tmp_dir}/{name.lower()}.jpg"
            elif os.path.exists(f"{tmp_dir}/{name.lower()}.png"):
                img_path = f"{tmp_dir}/{name.lower()}.png"
            else:
                img_path = "No image found"
            # Each animal entry: name + clickable image + local path string
            animal_cells += f"""<div class="animal-entry">
<a href="{img_path}">{name}</a><br/>
<img src="{img_path}" alt="{name}"><br/>
<span class="local-path">{img_path}</span>
</div>"""

        html += f"""        <tr>
            <td>{adj}</td>
            <td>{animal_cells}</td>
        </tr>
"""

    html += HTML_END

    file_path = os.path.join(tmp_dir, f"{file_name}.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)

    return file_path