from .worker import FileManagerToolSet
from ...utils.remote import toolset_cli


toolset_cli(FileManagerToolSet, "file_manager")
