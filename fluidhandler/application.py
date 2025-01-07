from pathlib import Path
from typing import Any

from infrareuse.application_container import CustomApplication
from infrareuse.components.application_component import ApplicationComponent


class FluidHandlerApplication(CustomApplication):
    def __init__(self) -> None:
        super().__init__()
        self.managers: list[ApplicationComponent] = []

    def configure(
        self, config_path: Path | str | None = None, **kwargs: dict[str, Any]
    ) -> None:
        super().configure(config_path, additional_objects=[], **kwargs)

    def pre_run(self) -> None:
        for manager in self.managers:
            manager.pre_run()

    def run(self) -> None:
        for manager in self.managers:
            manager.start()


if __name__ == "__main__":
    app = FluidHandlerApplication()
    app.configure(config_path="fluidhandler/config/config.yaml")
    app.pre_run()
    app.run()
