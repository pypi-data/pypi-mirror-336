__version__ = "0.1.3"

def version()->str:
    """Return the version of the lib

    Parameters
    ----------
    
    Returns
    -------
    str
        The string with version
    """
    return __version__

# str functions
from .flog import FileLog, Log

__all__ = [version, FileLog, Log]