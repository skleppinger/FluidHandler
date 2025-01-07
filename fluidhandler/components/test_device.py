from infrareuse.base_config import Config
from infrareuse.components.application_component import ConfigurableApplicationComponent
from typing import Any
from pathlib import Path
import tempfile
from infrareuse.logging.custom_logger import logger
from infrareuse.logging.logging_helpers import (
    create_file_handler,
    add_handler_to_logger,
)


class TestConfig(Config):
    foo: int
    bar: int
    baz: int
    PREFIX = "test_component"


class TestComponent(ConfigurableApplicationComponent):
    CONFIG = TestConfig

    def __init__(
        self, **kwargs: dict[str, Any]
    ) -> None:  # TODO fix, the config isn't showing up in the required kwargs
        super().__init__(**kwargs)
        self.params = self.CONFIG.model_validate(kwargs)
        print(self.params)

        # Make sure logging is working for the application, repeat of custom logger test
        self._logger = logger
        temp_dir = tempfile.gettempdir()
        temp_file = Path(temp_dir + "/test.log")
        handle = create_file_handler(temp_file)
        add_handler_to_logger(self._logger, handle)
        self._logger.info("TestComponent initialized")
        self._logger.info(f"TestComponent params: {self.params}")
        assert temp_file.exists()
        assert temp_file.stat().st_size > 0
