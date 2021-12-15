from app import get_app

if __name__ == '__main__':

    conf = {
        'menu_items': [
            {
                'image': 'search.svg',
                'text': 'Recherche',
            },
            {
                'image': 'window.svg',
                'text': 'Discussion',
            },
            {
                'image': 'transfer.svg',
                'text': 'Transfert',
            },
            {
                'image': 'settings.svg',
                'text': 'Réglages',
            },
            {
                'image': 'settings.svg',
                'text': 'Test',
            },
        ]
    }

    app = get_app(config=conf)
    app.run_server(debug=True)
