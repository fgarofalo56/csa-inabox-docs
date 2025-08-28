"""Documentation build testing utilities."""

import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml
import logging

logger = logging.getLogger(__name__)


class DocumentationBuildTester:
    """Test MkDocs documentation builds and validate output."""
    
    def __init__(self, docs_root: Path):
        """Initialize with documentation root directory.
        
        Args:
            docs_root: Path to the documentation root directory
        """
        self.docs_root = Path(docs_root)
        self.mkdocs_config = self.docs_root / "mkdocs.yml"
        
    def validate_mkdocs_config(self) -> Tuple[bool, List[str]]:
        """Validate MkDocs configuration file.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        if not self.mkdocs_config.exists():
            errors.append(f"MkDocs config file not found: {self.mkdocs_config}")
            return False, errors
            
        try:
            with open(self.mkdocs_config, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                
            # Check required fields
            required_fields = ['site_name', 'docs_dir']
            for field in required_fields:
                if field not in config:
                    errors.append(f"Required field '{field}' missing from mkdocs.yml")
                    
            # Validate docs_dir exists
            if 'docs_dir' in config:
                docs_dir = self.docs_root / config['docs_dir']
                if not docs_dir.exists():
                    errors.append(f"Documentation directory not found: {docs_dir}")
                    
            # Validate theme configuration
            if 'theme' in config:
                if isinstance(config['theme'], dict):
                    if 'name' not in config['theme']:
                        errors.append("Theme name not specified")
                elif isinstance(config['theme'], str):
                    # Simple theme name is valid
                    pass
                else:
                    errors.append("Invalid theme configuration")
                    
        except yaml.YAMLError as e:
            errors.append(f"Invalid YAML in mkdocs.yml: {e}")
        except Exception as e:
            errors.append(f"Error reading mkdocs.yml: {e}")
            
        return len(errors) == 0, errors
    
    def test_build(self, strict: bool = True) -> Tuple[bool, str, str]:
        """Test building the documentation.
        
        Args:
            strict: Whether to use strict mode (warnings as errors)
            
        Returns:
            Tuple of (success, stdout, stderr)
        """
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                cmd = ["mkdocs", "build", "--site-dir", temp_dir]
                if strict:
                    cmd.append("--strict")
                    
                result = subprocess.run(
                    cmd,
                    cwd=self.docs_root,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout
                )
                
                success = result.returncode == 0
                return success, result.stdout, result.stderr
                
        except subprocess.TimeoutExpired:
            return False, "", "Build timed out after 5 minutes"
        except Exception as e:
            return False, "", f"Build error: {e}"
    
    def validate_nav_structure(self) -> Tuple[bool, List[str]]:
        """Validate navigation structure in mkdocs.yml.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        try:
            with open(self.mkdocs_config, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                
            if 'nav' not in config:
                # No nav structure is valid - MkDocs will auto-generate
                return True, []
                
            nav = config['nav']
            self._validate_nav_items(nav, errors, self.docs_root / config.get('docs_dir', 'docs'))
            
        except Exception as e:
            errors.append(f"Error validating nav structure: {e}")
            
        return len(errors) == 0, errors
    
    def _validate_nav_items(self, nav_items: List, errors: List[str], docs_dir: Path, path_prefix: str = ""):
        """Recursively validate navigation items."""
        for item in nav_items:
            if isinstance(item, str):
                # Simple file reference
                file_path = docs_dir / item
                if not file_path.exists():
                    errors.append(f"Navigation file not found: {item}")
            elif isinstance(item, dict):
                for title, value in item.items():
                    if isinstance(value, str):
                        # Single file
                        file_path = docs_dir / value
                        if not file_path.exists():
                            errors.append(f"Navigation file not found: {value} (title: {title})")
                    elif isinstance(value, list):
                        # Nested navigation
                        self._validate_nav_items(value, errors, docs_dir, f"{path_prefix}/{title}")
    
    def get_build_statistics(self) -> Dict:
        """Get statistics about the documentation build.
        
        Returns:
            Dictionary with build statistics
        """
        stats = {
            'total_markdown_files': 0,
            'total_assets': 0,
            'config_valid': False,
            'nav_valid': False,
            'build_successful': False
        }
        
        # Count markdown files
        docs_dir = self.docs_root / "docs"
        if docs_dir.exists():
            stats['total_markdown_files'] = len(list(docs_dir.glob("**/*.md")))
            stats['total_assets'] = len(list(docs_dir.glob("**/*.{png,jpg,jpeg,gif,svg,pdf}")))
        
        # Check config validity
        stats['config_valid'], _ = self.validate_mkdocs_config()
        stats['nav_valid'], _ = self.validate_nav_structure()
        
        # Test build
        stats['build_successful'], _, _ = self.test_build(strict=False)
        
        return stats
    
    def check_plugin_dependencies(self) -> Tuple[bool, List[str]]:
        """Check if all required MkDocs plugins are available.
        
        Returns:
            Tuple of (all_available, list_of_missing_plugins)
        """
        missing_plugins = []
        
        try:
            with open(self.mkdocs_config, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                
            plugins = config.get('plugins', [])
            if not plugins:
                return True, []
                
            # Convert to list of plugin names
            plugin_names = []
            for plugin in plugins:
                if isinstance(plugin, str):
                    plugin_names.append(plugin)
                elif isinstance(plugin, dict):
                    plugin_names.extend(plugin.keys())
            
            # Test import each plugin
            for plugin_name in plugin_names:
                try:
                    # Try to import the plugin module
                    module_name = f"mkdocs_{plugin_name.replace('-', '_')}"
                    __import__(module_name)
                except ImportError:
                    try:
                        # Try alternative naming conventions
                        __import__(plugin_name.replace('-', '_'))
                    except ImportError:
                        missing_plugins.append(plugin_name)
                        
        except Exception as e:
            logger.warning(f"Error checking plugin dependencies: {e}")
            
        return len(missing_plugins) == 0, missing_plugins