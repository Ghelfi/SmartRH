from abc import ABC, abstractmethod
import logging

logger = logging.getLogger()

class GenericExtractor(ABC):
    name: str
    version: str

    def __init__(self, name, version) -> None:
        super().__init__()
        self.name = name
        self.version = version

    @abstractmethod
    def run(self, pdf_filepath=None):
        pass

    @abstractmethod
    def __repr__(self) -> str:
        return (
            f"<GenericExtractor("
            f"name={self.name}, "
            f"version={self.version}, "
            f")>"
        )


class DummyExtractor(GenericExtractor):

    def __init__(self, name, version) -> None:
        super().__init__(name, version)

    def run(self, pdf_filepath=None):
        return super().run(pdf_filepath=pdf_filepath)

    def __repr__(self) -> str:
        return (
            f"<DummyExtractor("
            f"name={self.name}, "
            f"version={self.version}, "
            f")>"
        )

def load_extractor(**kwargs)-> GenericExtractor:
    default_extractor = DummyExtractor(**kwargs)
    if "name" not in kwargs:
        logger.error('"name" must be filled in extraction algorithm configuration. {} will be loaded by default.'.format(default_extractor.name))
        return default_extractor

    if kwargs['name'] == "DummyExtractor":
        return DummyExtractor(**kwargs)
    else:
        return default_extractor