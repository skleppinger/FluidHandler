from infrareuse.components.application_component import (
    ApplicationComponent,
    ConfigurableApplicationComponent,
)
from infrareuse.dependency_resolver import DependencyResolver, ResolveByNameAndType
from typing import Any
import infrareuse.factory as factory
import asyncio


class DeviceManager(ApplicationComponent):
    PREFIX = "DeviceManager"

    def __init__(
        self,
        resolver: DependencyResolver,
        **kwargs: dict[str, Any],
    ) -> None:
        super().__init__(**kwargs)
        self.resolver = resolver
        self.local_config = self._global_config.get(self.PREFIX, {})
        self.components = self.load_components()
        self._loop = asyncio.get_event_loop()

    def load_components(self) -> list[ApplicationComponent]:
        components = []
        for component_name, component_config in self.local_config.items():
            component_class = factory.load_classes([component_config])[0]
            additional_config = component_config.copy()
            additional_config.pop("module", None)
            additional_config.pop("enabled", None)
            required_kwargs = self.resolver.resolve_object_kwargs(
                component_class,
                policy=ResolveByNameAndType,
                additional_objects=additional_config,
            )
            if issubclass(component_class, ConfigurableApplicationComponent):
                component_class.validate_config(
                    required_kwargs, surpress_warnings=False
                )
            component = component_class(**required_kwargs)
            self.resolver.add_object(component, component_name)
            components.append(component)
        return components

    def configure(self) -> None:
        super().configure()

    def pre_run(self) -> None:
        pass

    def start(self) -> None:
        print("Starting TestManager")
