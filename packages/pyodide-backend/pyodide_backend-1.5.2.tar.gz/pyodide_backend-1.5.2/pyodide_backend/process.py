from .interactive_shell import InteractiveShell
from .matplotlib_plots import FiguresManager


trigger_matplotlib_show_callback = FiguresManager.matplotlib_show


class WasmProcess:
    def __init__(self):
        # Create the custom interactive console.
        self.shell = InteractiveShell(locals={})

        self.shell.run_cell(
            "import matplotlib; matplotlib.use('module://pyodide_backend.matplotlib_custom_backend', force=True)"
        )

    def executeTask(self, task):
        return task(self.shell)

    def kill(self):
        self.reset()

    def reset(self):
        self.shell.reset()
