from enum import Enum
import uuid
import pathlib

class FileStatus(Enum):
    _EMPTY = "-"
    QUEUED = "Queued"
    RUNNING = "Running"
    FINISHED = "Finished"
    EARLY_TERMINATED = "Early terminated"
    UNKOWN = "Unkown"
    NO_OUTPUT = "Denoiser did not respond"
    ERROR = "Failed"
    ERROR_FILE_EXISTS = "Output file already exists"
    ERROR_NDENOISER_UNKOWN = "Unexpected Error in Denoiser"

    def Get_Color(fs):
        match (fs):
            case FileStatus.ERROR | FileStatus.ERROR_FILE_EXISTS | FileStatus.ERROR_NDENOISER_UNKOWN | FileStatus.EARLY_TERMINATED:
                return "red"
            case FileStatus.UNKOWN | FileStatus.NO_OUTPUT:
                return "light_orange"
            case FileStatus.RUNNING:
                return "grey"
            case FileStatus.FINISHED:
                return "green"
            case _:
                return ""
            
    def Get_Significance(fs):
        match (fs):
            case FileStatus.ERROR | FileStatus.UNKOWN:
                return 30
            case FileStatus.ERROR_NDENOISER_UNKOWN:
                return 23
            case FileStatus.ERROR_FILE_EXISTS:
                return 22
            case FileStatus.NO_OUTPUT:
                return 21
            case FileStatus.EARLY_TERMINATED:
                return 20
            case FileStatus.QUEUED | FileStatus.RUNNING | FileStatus.FINISHED:
                return 10
            case FileStatus._EMPTY:
                return 0
            case _:
                return 100
            
    def Get_MostSignificant(listfs: list):
        fsMax = FileStatus._EMPTY
        if listfs is None or len(listfs) == 0:
            return None
        for fs in listfs:
            if FileStatus.Get_Significance(fs) > FileStatus.Get_Significance(fsMax):
                fsMax = fs
        return fsMax

class QueuedObject:
    def __init__(self, path: str):
        self._path = pathlib.Path(path)
        self.id = str(uuid.uuid4())
        self.status: FileStatus = FileStatus.QUEUED
    
    @property
    def basepath(self):
        return self._path.parent
    
    @property
    def filename(self):
        return self._path.name
    
    @property
    def path(self):
        return self._path

class QueuedFile(QueuedObject):
    def __init__(self, path: str):
        super().__init__(path)
        if (not self._path.is_file()):
            raise ValueError("The given path is not a file")
    
class QueuedFolder(QueuedObject):
    def __init__(self, path):
        super().__init__(path)
        if not self._path.is_dir():
            raise ValueError("The given path is not a directory")
        
    @property
    def basepath(self):
        return self._path
    
    @property
    def filename(self):
        return ""

class FileQueue:
    def __init__(self):
        self._fileQueue = {}

    def __getitem__(self, key) -> QueuedObject:
        return self._fileQueue[key]
    
    def __setitem__(self, key, value):
        self._fileQueue[key] = value

    def AddFile(self, qf: QueuedObject):
        if qf.id not in self._fileQueue.keys():
            self._fileQueue[qf.id] = qf

    def remove(self, key):
        self._fileQueue.pop(key)

    def keys(self):
        return self._fileQueue.keys()

    def items(self):
        return self._fileQueue.items()
    
    def values(self):
        return self._fileQueue.values()

    def PopQueued(self) -> QueuedObject | None:
        for id, qf in self._fileQueue.items():
           if qf.status == FileStatus.QUEUED:
               return qf
        return None