import inspect
from CTFd.utils.uploads import upload_file
print(inspect.signature(upload_file))
print(inspect.getsource(upload_file))
