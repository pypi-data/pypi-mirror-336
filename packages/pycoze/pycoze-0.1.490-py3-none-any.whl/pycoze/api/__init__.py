from .lib.window import WindowCls
from .lib.tab import TabCls

class Api:
    def __init__(self) -> None:
        self.window = WindowCls()
        self.tab = TabCls()

api = Api()
window = api.window
tab = api.tab

# from ps_view import ViewCls, WebsiteViewCls, FileViewCls, DirectoryViewCls, WorkflowCls