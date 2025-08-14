import os

mapping_dict = {
'scolopacine': [('Dunlin', 'https://en.wikipedia.org/wiki/Dunlin'),
                ('Sandpiper', 'https://en.wikipedia.org/wiki/Sandpiper')],
'aquiline': [('Eagle', 'https://en.wikipedia.org/wiki/Eagle')]
}

test_image_path = os.path.join(os.path.dirname(__file__), "test.jpg")