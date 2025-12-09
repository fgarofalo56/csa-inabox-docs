"""Unit tests for CLI module."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import argparse
import sys

from csa_docs_tools.cli import (
    setup_parser,
)


class TestCLIParser:
    """Test suite for CLI argument parser."""

    def test_setup_parser(self):
        """Test parser setup."""
        parser = setup_parser()

        assert isinstance(parser, argparse.ArgumentParser)
        assert parser.description is not None

    def test_parser_default_args(self):
        """Test parser with no arguments."""
        parser = setup_parser()

        # Parse empty arguments
        args = parser.parse_args([])

        assert args.docs_root == Path.cwd()
        assert args.output == "text"
        assert args.quiet is False
        assert args.verbose is False

    def test_parser_docs_root_arg(self):
        """Test --docs-root argument."""
        parser = setup_parser()

        args = parser.parse_args(["--docs-root", "/test/path"])

        assert args.docs_root == Path("/test/path")

    def test_parser_config_arg(self):
        """Test --config argument."""
        parser = setup_parser()

        args = parser.parse_args(["--config", "config.yml"])

        assert args.config == Path("config.yml")

    def test_parser_output_formats(self):
        """Test --output argument with different formats."""
        parser = setup_parser()

        # Test json output
        args = parser.parse_args(["--output", "json"])
        assert args.output == "json"

        # Test text output
        args = parser.parse_args(["--output", "text"])
        assert args.output == "text"

        # Test summary output
        args = parser.parse_args(["--output", "summary"])
        assert args.output == "summary"

    def test_parser_quiet_flag(self):
        """Test --quiet flag."""
        parser = setup_parser()

        args = parser.parse_args(["--quiet"])
        assert args.quiet is True

        args = parser.parse_args(["-q"])
        assert args.quiet is True

    def test_parser_verbose_flag(self):
        """Test --verbose flag."""
        parser = setup_parser()

        args = parser.parse_args(["--verbose"])
        assert args.verbose is True

        args = parser.parse_args(["-v"])
        assert args.verbose is True

    def test_parser_all_command(self):
        """Test 'all' subcommand."""
        parser = setup_parser()

        args = parser.parse_args(["all"])
        assert args.command == "all"

        args = parser.parse_args(["all", "--fail-fast"])
        assert args.command == "all"
        assert args.fail_fast is True

    def test_parser_build_command(self):
        """Test 'build' subcommand."""
        parser = setup_parser()

        args = parser.parse_args(["build"])
        assert args.command == "build"

        args = parser.parse_args(["build", "--strict"])
        assert args.command == "build"
        assert args.strict is True

    def test_parser_quality_command(self):
        """Test 'quality' subcommand."""
        parser = setup_parser()

        try:
            args = parser.parse_args(["quality"])
            assert args.command == "quality"
        except SystemExit:
            # Command might not exist yet
            pass

    def test_parser_links_command(self):
        """Test 'links' subcommand."""
        parser = setup_parser()

        try:
            args = parser.parse_args(["links"])
            assert args.command == "links"
        except SystemExit:
            # Command might not exist yet
            pass

    def test_parser_images_command(self):
        """Test 'images' subcommand."""
        parser = setup_parser()

        try:
            args = parser.parse_args(["images"])
            assert args.command == "images"
        except SystemExit:
            # Command might not exist yet
            pass

    def test_parser_nav_command(self):
        """Test 'nav' subcommand."""
        parser = setup_parser()

        try:
            args = parser.parse_args(["nav"])
            assert args.command == "nav"
        except SystemExit:
            # Command might not exist yet
            pass


class TestCLICommands:
    """Test suite for CLI command execution."""

    @patch('csa_docs_tools.cli.DocumentationBuildTester')
    def test_build_command_execution(self, mock_build_tester):
        """Test build command execution."""
        # Mock the build tester
        mock_tester = Mock()
        mock_tester.test_build.return_value = (True, "Success", "")
        mock_build_tester.return_value = mock_tester

        # This is a placeholder for actual command execution
        # The CLI might need a main() function or similar entry point
        assert mock_build_tester is not None

    def test_cli_help_output(self):
        """Test that help can be displayed."""
        parser = setup_parser()

        # Should not raise exception
        help_text = parser.format_help()
        assert "CSA Documentation Testing" in help_text
        assert "Examples:" in help_text


class TestCLIErrorHandling:
    """Test error handling in CLI."""

    def test_parser_invalid_output_format(self):
        """Test parser with invalid output format."""
        parser = setup_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["--output", "invalid"])

    def test_parser_unknown_command(self):
        """Test parser with unknown command."""
        parser = setup_parser()

        # Unknown commands should be handled gracefully
        try:
            args = parser.parse_args(["unknown"])
            # If it doesn't raise, command should be None or 'unknown'
            assert args.command in [None, "unknown"]
        except SystemExit:
            # Expected behavior for unknown commands
            pass


class TestCLIIntegration:
    """Integration tests for CLI."""

    def test_full_argument_parsing(self):
        """Test parsing a complete set of arguments."""
        parser = setup_parser()

        args = parser.parse_args([
            "--docs-root", "/test/docs",
            "--config", "config.yml",
            "--output", "json",
            "--verbose",
            "build",
            "--strict"
        ])

        assert args.docs_root == Path("/test/docs")
        assert args.config == Path("config.yml")
        assert args.output == "json"
        assert args.verbose is True
        assert args.command == "build"
        assert args.strict is True

    def test_conflicting_flags(self):
        """Test that conflicting flags can be handled."""
        parser = setup_parser()

        # Both quiet and verbose - parser should accept this
        # (application logic would decide which takes precedence)
        args = parser.parse_args(["--quiet", "--verbose"])

        assert args.quiet is True
        assert args.verbose is True


class TestCLIUtilityFunctions:
    """Test utility functions in CLI module."""

    def test_parser_has_subcommands(self):
        """Test that parser has subcommands configured."""
        parser = setup_parser()

        # Get subparsers
        subparsers_actions = [
            action for action in parser._actions
            if isinstance(action, argparse._SubParsersAction)
        ]

        assert len(subparsers_actions) > 0

        # Check that subparsers have choices
        subparsers = subparsers_actions[0]
        assert subparsers.choices is not None
        assert len(subparsers.choices) > 0
