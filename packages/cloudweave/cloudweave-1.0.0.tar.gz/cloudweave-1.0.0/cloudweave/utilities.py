from threading import Lock
import weakref
import abc

class Singleton(abc.ABC):
    """
    Abstract base class implementing a thread-safe singleton pattern.
    Ensures only one instance of a class exists and handles proper initialization.
    """
    _instances = weakref.WeakValueDictionary()  # Store weak references to instances
    _lock = Lock()  # Thread synchronization lock

    def __new__(cls, *args, **kwargs):
        """Create or return the singleton instance"""
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__new__(cls)
                instance._initialized = False
                cls._instances[cls] = instance
            return cls._instances[cls]

    def __init__(self, *args, **kwargs):
        """Initialize the singleton instance if not already initialized"""
        with self._lock:
            if not getattr(self, '_initialized', False):
                self._initialize(*args, **kwargs)
                self._initialized = True

    @abc.abstractmethod
    def _initialize(self, *args, **kwargs):
        """Implementation-specific initialization logic"""
        pass

    def __reduce__(self):
        """Custom pickle reduction"""
        return self.__class__, ()
        
    def __copy__(self):
        """Custom shallow copy behavior"""
        return self
        
    def __deepcopy__(self, memo):
        """Custom deep copy behavior"""
        return self