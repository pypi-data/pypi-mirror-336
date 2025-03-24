import argparse
import sys
from importlib.metadata import version
from pathlib import Path
from typing import Dict, Optional, Type

from loguru import logger

from pipzap import __version__ as zap_version
from pipzap.core import DependencyPruner, SourceType
from pipzap.core.dependencies import ProjectDependencies
from pipzap.formatting import PoetryFormatter, RequirementsTXTFormatter, UVFormatter
from pipzap.formatting.base import DependenciesFormatter
from pipzap.parsing import DependenciesParser, ProjectConverter, Workspace

KNOWN_FORMATTERS: Dict[SourceType, Type[DependenciesFormatter]] = {
    SourceType.POETRY: PoetryFormatter,
    SourceType.REQUIREMENTS: RequirementsTXTFormatter,
    SourceType.UV: UVFormatter,
}


class PipZapCLI:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="Dependency pruning and merging tool",
            epilog=zap_version,
        )
        self._setup_parser()

    def run(self, do_raise: bool = False, args: Optional[argparse.Namespace] = None) -> None:
        args = args or self.parser.parse_args()

        if not args.verbose:
            logger.remove()
            logger.add(
                sys.stderr,
                format="<level>• {level: <7}</level> | <level>{message}</level>",
                level="INFO",
            )

        logger.debug(f"Starting PipZap v{zap_version} (uv v{version('uv')})")

        if args.format is not None:
            args.format = SourceType(args.format)

        try:
            with Workspace(args.file) as workspace:
                source_format = ProjectConverter(args.python_version).convert_to_uv(workspace)
                parsed = DependenciesParser().parse(workspace)
                pruned = DependencyPruner().prune(parsed)

            return self._output_results(pruned, args.output, args.format or source_format, args.force)

        except Exception as err:
            if args.verbose:
                logger.exception(err)
            else:
                logger.error(err)

            if do_raise:
                raise err

    def _output_results(
        self,
        deps: ProjectDependencies,
        output: Optional[Path],
        out_format: SourceType,
        force: bool,
    ) -> None:
        """Outputs the formatted pruned dependencies.

        The result is written to the specified output file or printed to stdout if no file is provided.
        """
        result = KNOWN_FORMATTERS[out_format](deps).format()
        if not output:
            print("\n" + result)
            return

        if output.is_file() and not force:
            raise ValueError(f"Output file {output} already exists. Specify --force to allow overriding")

        output.write_text(result)
        logger.info(f"Results written to {output}")

    def _setup_parser(self):
        self.parser.add_argument("file", type=Path, help="Path to the dependency file")
        self.parser.add_argument("-v", "--verbose", action="store_true", help="Produce richer logs")
        self.parser.add_argument(
            "-o",
            "--output",
            type=Path,
            default=None,
            help="Output file (defaults to stdout)",
        )
        self.parser.add_argument("--force", action="store_true", help="Allow overriding existing files")
        self.parser.add_argument(
            "-f",
            "--format",
            type=str,
            choices=[f.name.lower() for f in KNOWN_FORMATTERS],
            help="Output format for dependency list (defaults to the same as input)",
        )
        self.parser.add_argument(
            "-p",
            "--python-version",
            type=str,
            default=None,
            help="Python version (required for requirements.txt)",
        )
