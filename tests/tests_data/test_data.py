import os
from collections import defaultdict

good_url = 'https://google.com'
bad_url = 'https://notexistingblabla.com'

mapping_dict = {
'scolopacine': [('Dunlin', 'https://en.wikipedia.org/wiki/Dunlin'),
                ('Sandpiper', 'https://en.wikipedia.org/wiki/Sandpiper')],
'aquiline': [('Eagle', 'https://en.wikipedia.org/wiki/Eagle')]
}

test_image_path = os.path.join(os.path.dirname(__file__), "test.jpg")

mock_html_table = """
<table>
    <tr>
        <th>Header1</th>
        <th>Header2</th>
    </tr>
    <tr>
        <td>Row1Col1</td>
        <td>Row1Col2</td>
    </tr>
    <tr>
        <td>Row2Col1</td>
        <td>Row2Col2</td>
    </tr>
</table>
"""
mock_html_table_headers = ("Header1", "Header2")

mapping_dict_result = defaultdict(list, {'Row1Col1': ['Row1Col2'], 'Row2Col1': ['Row2Col2']})

img_url = "//upload.wikimedia.org/wikipedia/en/thumb/example1.jpg"

mock_wiki_html = f"""
<html>
  <body>
    <img src="{img_url}" />
    <img src="//upload.wikimedia.org/wikipedia/en/example2.svg" />
    <img src="//otherdomain.com/image.jpg" />
  </body>
</html>
"""
