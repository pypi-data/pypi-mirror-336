from gettext import gettext as _

from pulp_glue.common.context import (
    EntityDefinition,
    PluginRequirement,
    PulpContentContext,
    PulpEntityContext,
    PulpRemoteContext,
    PulpRepositoryContext,
    PulpRepositoryVersionContext,
)


class PulpConsoleContentContext(PulpContentContext):
    """Context for Console Content."""

    PLUGIN = "console"
    RESOURCE_TYPE = "content"
    ENTITY = _("console content")
    ENTITIES = _("console content")
    HREF = "console_console_content_href"
    ID_PREFIX = "content_console_content"
    NEEDS_PLUGINS = [PluginRequirement("console", specifier=">=1.0.0")]


class PulpConsoleDistributionContext(PulpEntityContext):
    """Context for Console Distribution."""

    PLUGIN = "console"
    RESOURCE_TYPE = "console"
    ENTITY = _("console distribution")
    ENTITIES = _("console distributions")
    HREF = "console_console_distribution_href"
    ID_PREFIX = "distributions_console_console"
    NEEDS_PLUGINS = [PluginRequirement("console", specifier=">=1.0.0")]

    def preprocess_entity(self, body: EntityDefinition, partial: bool = False) -> EntityDefinition:
        body = super().preprocess_entity(body, partial)
        version = body.pop("version", None)
        if version is not None:
            repository_href = body.pop("repository")
            body["repository_version"] = f"{repository_href}versions/{version}/"
        return body


class PulpConsoleRemoteContext(PulpRemoteContext):
    """Context for Console Remote."""

    PLUGIN = "console"
    RESOURCE_TYPE = "console"
    ENTITY = _("console remote")
    ENTITIES = _("console remotes")
    HREF = "console_console_remote_href"
    ID_PREFIX = "remotes_console_console"
    NEEDS_PLUGINS = [PluginRequirement("console", specifier=">=1.0.0")]


class PulpConsoleRepositoryVersionContext(PulpRepositoryVersionContext):
    """Context for Console Repository Version."""

    PLUGIN = "console"
    RESOURCE_TYPE = "console"
    HREF = "console_console_repository_version_href"
    ID_PREFIX = "repositories_console_console_versions"
    NEEDS_PLUGINS = [PluginRequirement("console", specifier=">=1.0.0")]


class PulpConsoleRepositoryContext(PulpRepositoryContext):
    """Context for Console Repository."""

    PLUGIN = "console"
    RESOURCE_TYPE = "console"
    HREF = "console_console_repository_href"
    ID_PREFIX = "repositories_console_console"
    VERSION_CONTEXT = PulpConsoleRepositoryVersionContext
    NEEDS_PLUGINS = [PluginRequirement("console", specifier=">=1.0.0")]
    CAPABILITIES = {
        "sync": [PluginRequirement("console", specifier=">=1.0.0")],
    }

    # Add custom methods for your repository operations here
    # For example:
    # def import_content(self, href: str, artifact: str, ...) -> Any:
    #     body = {...}
    #     return self.pulp_ctx.call("your_import_method_id",
    #                               parameters={self.HREF: href},
    #                               body=body)
