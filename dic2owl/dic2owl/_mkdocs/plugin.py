"""A plugin for MkDocs to run pre-build functionality."""
import os
import re
import shutil
from contextlib import redirect_stderr
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.error import HTTPError

from mkdocs.config.config_options import Type
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin
from mkdocstrings.loggers import get_logger

# Remove the print statement concerning 'owlready2_optimized' when importing owlready2
# (which is imported also in emmo).
with open(os.devnull, "w", encoding="utf8") as handle:
    with redirect_stderr(handle):
        from ontopy import get_ontology

if TYPE_CHECKING:
    from mkdocs.config import Config
    from ontopy.ontology import Ontology


LOGGER = get_logger(__name__)

VERSION_IRI_REGEX = re.compile(
    r"https?://(?P<domain>[a-zA-Z._-]+)/(?P<path>[a-zA-Z_-]+(/[a-zA-Z_-]+)*)"
    r"/(?P<version>[0-9a-zA-Z._-]+)(/(?P<name>[a-zA-Z_-]+))?(/(?P<filename>[a-zA-Z_.-]+))?"
)


class OntologyBuildPlugin(BasePlugin):
    """Build ontologies."""

    config_scheme = (
        ("ontology_dir", Type(str, default="ontology")),
        ("publish_dir", Type(str, default="docs/ontology/versions")),
        ("create_dirs", Type(bool, default=False)),
    )

    def on_pre_build(  # pylint: disable=too-many-locals,too-many-branches
        self, config: "Config"  # pylint: disable=unused-argument
    ) -> None:
        """Build versioned ontologies.

        Hook for the [`pre-build` event](https://www.mkdocs.org/dev-guide/plugins/#on_pre_build).

        Parameters:
            config: The MkDocs Config object.

        """
        # root_dir = Path(__file__).resolve().parent.parent.parent.parent
        ontology_dir = Path(self.config["ontology_dir"]).resolve()
        publish_dir = Path(self.config["publish_dir"]).resolve()

        LOGGER.debug(
            "Resolved config values:\n  ontology_dir=%s\n  publish_dir=%s",
            ontology_dir,
            publish_dir,
        )

        if not ontology_dir.exists():
            raise PluginError("The given 'ontology_dir' must exist.")

        if not publish_dir.exists():
            if self.config["create_dirs"]:
                publish_dir.mkdir(parents=True, exist_ok=True)
            else:
                raise PluginError(
                    "The given 'publish_dir' must exist. "
                    "Otherwise, 'create_dirs' should be 'True'."
                )

        ontology_files = list(ontology_dir.glob("*.ttl"))
        try:
            catalog_file = sorted(ontology_dir.glob("catalog-*.xml"), reverse=True)[0]
        except IndexError as exc:
            raise PluginError(
                "Could not find a catalog file in the 'ontology_dir'."
            ) from exc

        LOGGER.debug("Building ontologies:")
        for ontology_file in ontology_files:
            LOGGER.debug("  * %s", ontology_file.name)
            ontology: "Ontology" = get_ontology(str(ontology_file))
            try:
                ontology.load()
            except HTTPError:
                pass
            try:
                version_iri = ontology.get_version(as_iri=True)
            except TypeError as exc:
                raise PluginError(str(exc)) from exc

            version_iri_match = VERSION_IRI_REGEX.fullmatch(version_iri)
            if version_iri_match is None:
                raise PluginError(
                    f"Could not retrieve versionIRI properly from {ontology_file.name!r}"
                )

            version_iri_parts = version_iri_match.groupdict()
            version_iri_parts["top_name"] = version_iri_parts["path"].rsplit("/", 1)[-1]

            relative_destination_dir = (
                Path()
                / version_iri_parts["top_name"]
                / version_iri_parts["version"]
                / version_iri_parts["name"]
                if version_iri_parts["name"]
                else Path()
                / version_iri_parts["top_name"]
                / version_iri_parts["version"]
            )
            (publish_dir / relative_destination_dir).mkdir(parents=True, exist_ok=True)
            shutil.copyfile(
                src=ontology_file,
                dst=publish_dir / relative_destination_dir / ontology_file.name,
            )

            shutil.copyfile(
                src=catalog_file,
                dst=publish_dir / relative_destination_dir / catalog_file.name,
            )
            lines = []
            for line in (
                (publish_dir / relative_destination_dir / catalog_file.name)
                .read_text("utf8")
                .splitlines()
            ):
                if "<uri" in line and ontology_file.name not in line:
                    match = re.match(r"^.* uri=\"(?P<filename>.*)\.ttl\"/>$", line)
                    if not match:
                        raise PluginError(
                            "Could not determine filename in catalog file."
                        )
                    filename: str = match.group("filename")
                    lines.append(
                        re.sub(
                            r"uri=\".*\.ttl\"",
                            f'uri="../{filename}/{filename}.ttl"',
                            line,
                        )
                    )
                else:
                    lines.append(line)
            (publish_dir / relative_destination_dir / catalog_file.name).write_text(
                "\n".join(lines) + "\n", encoding="utf8"
            )
