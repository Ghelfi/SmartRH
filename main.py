from app import get_app

if __name__ == '__main__':

    conf = {
        'menu_items': [
            {
                'image': 'search.svg',
                'text': 'Recherche',
                'children': 'Recherche'
            },
            {
                'image': 'window.svg',
                'text': 'Discussion',
                'children': "Discussion"
            },
            {
                'image': 'transfer.svg',
                'text': 'Transfert',
                'children': 'Transfert'
            },
            {
                'image': 'settings.svg',
                'text': 'Réglages',
                'children': 'Réglages',
            },
        ]
    }

    app = get_app(config=conf)
    app.run_server(debug=True)
