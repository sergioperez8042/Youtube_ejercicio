import abc

class ISearch(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def searchType(self):
        pass
    
    
