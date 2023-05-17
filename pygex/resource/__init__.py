from pathlib import Path


RESOURCES_PATH = Path(__file__).parent.resolve().__str__().replace('\\', '/') + '/'

__all__ = 'RESOURCES_PATH',
