from abc import ABC, abstractmethod


class SpecificLayout(ABC):

    @abstractmethod
    def get_layout(self):
        pass

    @abstractmethod
    def generate_callbacks(self):
        pass

class UnderConstructionLayout(SpecificLayout):

    def get_layout(self):
        return 'En construction'

    def generate_callbacks(self):
        pass

class SearchLayout(SpecificLayout):

    def get_layout(self):
        return 'Recherche'

    def generate_callbacks(self):
        pass

class ChatLayout(SpecificLayout):

    def get_layout(self):
        return 'Discussion'

    def generate_callbacks(self):
        pass

class SettingsLayout(SpecificLayout):

    def get_layout(self):
        return 'Réglages'

    def generate_callbacks(self):
        pass

class UploadLayout(SpecificLayout):

    def get_layout(self):
        return 'Transfert'

    def generate_callbacks(self):
        pass


menu_layout_mapping_dictionnary = {
    "Recherche": SearchLayout(),
    "Discussion": ChatLayout(),
    "Réglages": SettingsLayout(),
    "Transfert": UploadLayout()
}
