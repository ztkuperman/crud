
test_data = [
    {'id': 1, 'title': "Post 1", "content": "My First Post"},
    {'id': 2, 'title': "Post 2", "content": "My Second Post"},
    {'id': 3, 'title': "Post 3", "content": "My Third Post"},
    ]

def get_posts():
    return test_data

def get_single_post(id: int):
    return [x for x in test_data if x.get('id')==id][0]
