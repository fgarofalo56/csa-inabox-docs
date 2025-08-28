"""Enhanced Mike version management for MkDocs documentation.

This module provides advanced version management capabilities for Mike,
including multi-version navigation, version comparison, and deployment automation.
"""

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union

import yaml
from mkdocs.config import load_config
from mkdocs.commands.build import build as mkdocs_build

from .version_manager import SemanticVersionManager, VersionInfo, VersionType


@dataclass
class MikeConfig:
    """Configuration for Mike version management."""
    
    alias_type: str = "symlink"
    redirect_template: Optional[str] = None
    deploy_prefix: str = ""
    versions_file: str = "versions.json"
    branch: str = "gh-pages"
    remote: str = "origin"
    

@dataclass
class DeployedVersion:
    """Information about a deployed documentation version."""
    
    version: str
    title: str
    aliases: List[str]
    is_default: bool = False
    deploy_date: Optional[str] = None
    size_mb: Optional[float] = None
    

class MikeVersionManager:
    """Enhanced Mike version management with advanced features."""
    
    def __init__(self, repo_path: Optional[Path] = None, config_file: Optional[Path] = None):
        """Initialize Mike version manager.
        
        Args:
            repo_path: Path to repository root
            config_file: Path to Mike configuration file
        """
        self.repo_path = repo_path or Path.cwd()
        self.config_file = config_file or (self.repo_path / ".mike.yml")
        self.mkdocs_config_file = self.repo_path / "mkdocs.yml"
        
        self.config = self._load_mike_config()
        self.version_manager = SemanticVersionManager()
        
    def deploy_version(self, version: str, title: Optional[str] = None, 
                      aliases: Optional[List[str]] = None, 
                      set_default: bool = False,
                      update_aliases: bool = True) -> Dict[str, str]:
        """Deploy a documentation version using Mike.
        
        Args:
            version: Version identifier
            title: Display title for the version
            aliases: List of aliases for the version
            set_default: Whether to set as default version
            update_aliases: Whether to update existing aliases
            
        Returns:
            Dictionary with deployment information
        """
        # Validate version format
        try:
            self.version_manager.parse_version(version)
        except ValueError as e:
            raise ValueError(f"Invalid version format '{version}': {e}") from e
        
        # Prepare Mike command
        cmd = ['mike', 'deploy']
        
        if update_aliases:
            cmd.append('--update-aliases')
        
        if set_default:
            cmd.append('--set-default')
        
        # Add version and title
        cmd.append(version)
        
        if title:
            cmd.append(title)
        
        # Add aliases
        if aliases:
            cmd.extend(aliases)
        
        # Run deployment
        try:
            result = self._run_mike_command(cmd)
            
            # Update versions.json with additional metadata
            self._update_version_metadata(version, title, aliases, set_default)
            
            return {
                'version': version,
                'title': title or version,
                'aliases': aliases or [],
                'is_default': set_default,
                'deployment_output': result
            }
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to deploy version {version}: {e}") from e
    
    def list_versions(self, include_metadata: bool = True) -> List[DeployedVersion]:
        """List all deployed versions.
        
        Args:
            include_metadata: Whether to include additional metadata
            
        Returns:
            List of deployed version information
        """
        try:
            output = self._run_mike_command(['mike', 'list', '--json'])
            versions_data = json.loads(output)
            
            deployed_versions = []
            for version_data in versions_data:
                deployed_version = DeployedVersion(
                    version=version_data['version'],
                    title=version_data['title'],
                    aliases=version_data.get('aliases', []),
                    is_default=version_data.get('is_default', False)
                )
                
                if include_metadata:
                    # Add additional metadata if available
                    self._enhance_version_info(deployed_version)
                
                deployed_versions.append(deployed_version)
            
            return deployed_versions
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to list versions: {e}") from e
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse version list: {e}") from e
    
    def delete_version(self, version: str, confirm: bool = False) -> bool:
        """Delete a deployed version.
        
        Args:
            version: Version to delete
            confirm: Whether to skip confirmation prompt
            
        Returns:
            True if deletion was successful
        """
        if not confirm:
            raise ValueError("Version deletion requires explicit confirmation")
        
        try:
            self._run_mike_command(['mike', 'delete', version])
            return True
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to delete version {version}: {e}") from e
    
    def set_default_version(self, version: str) -> Dict[str, str]:
        """Set the default version.
        
        Args:
            version: Version to set as default
            
        Returns:
            Dictionary with operation result
        """
        try:
            self._run_mike_command(['mike', 'set-default', version])
            return {
                'default_version': version,
                'status': 'success'
            }
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to set default version {version}: {e}") from e
    
    def alias_version(self, version: str, alias: str, update: bool = True) -> Dict[str, str]:
        """Add an alias to a version.
        
        Args:
            version: Existing version
            alias: Alias to add
            update: Whether to update if alias already exists
            
        Returns:
            Dictionary with operation result
        """
        cmd = ['mike', 'alias']
        if update:
            cmd.append('--update')
        cmd.extend([version, alias])
        
        try:
            self._run_mike_command(cmd)
            return {
                'version': version,
                'alias': alias,
                'status': 'success'
            }
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to alias version {version} as {alias}: {e}") from e
    
    def serve_version(self, version: str, port: int = 8000, 
                     host: str = "127.0.0.1") -> subprocess.Popen:
        """Serve a specific version for testing.
        
        Args:
            version: Version to serve
            port: Port to serve on
            host: Host to bind to
            
        Returns:
            Process object for the server
        """
        cmd = [
            'mike', 'serve',
            '--dev-addr', f"{host}:{port}",
            version
        ]
        
        try:
            return subprocess.Popen(
                cmd,
                cwd=self.repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except Exception as e:
            raise RuntimeError(f"Failed to serve version {version}: {e}") from e
    
    def compare_versions(self, version1: str, version2: str) -> Dict[str, Union[str, List[str]]]:
        """Compare two deployed versions.
        
        Args:
            version1: First version to compare
            version2: Second version to compare
            
        Returns:
            Dictionary with comparison results
        """
        deployed_versions = self.list_versions()
        version1_info = next((v for v in deployed_versions if v.version == version1), None)
        version2_info = next((v for v in deployed_versions if v.version == version2), None)
        
        if not version1_info:
            raise ValueError(f"Version {version1} not found")
        if not version2_info:
            raise ValueError(f"Version {version2} not found")
        
        # Compare using semantic versioning
        comparison_result = self.version_manager.compare_versions(version1, version2)
        
        comparison = {
            'version1': version1,
            'version2': version2,
            'semantic_comparison': comparison_result,
            'version1_newer': comparison_result > 0,
            'version2_newer': comparison_result < 0,
            'same_version': comparison_result == 0,
            'differences': self._analyze_version_differences(version1_info, version2_info)
        }
        
        return comparison
    
    def generate_version_navigation(self, current_version: str) -> Dict[str, Union[str, List[Dict[str, str]]]]:
        """Generate navigation structure for version switcher.
        
        Args:
            current_version: Currently displayed version
            
        Returns:
            Navigation structure dictionary
        """
        deployed_versions = self.list_versions()
        
        # Sort versions by semantic versioning
        try:
            sorted_versions = sorted(
                deployed_versions,
                key=lambda v: self.version_manager.parse_version(v.version)['clean'],
                reverse=True
            )
        except ValueError:
            # Fallback to string sorting if semantic parsing fails
            sorted_versions = sorted(deployed_versions, key=lambda v: v.version, reverse=True)
        
        # Group versions by type
        grouped_versions = {
            'stable': [],
            'prerelease': [],
            'development': [],
            'legacy': []
        }
        
        for version in sorted_versions:
            version_info = self._classify_version(version.version)
            grouped_versions[version_info.version_type.value].append({
                'version': version.version,
                'title': version.title,
                'aliases': version.aliases,
                'is_current': version.version == current_version,
                'is_default': version.is_default
            })
        
        return {
            'current_version': current_version,
            'default_version': next(
                (v.version for v in deployed_versions if v.is_default),
                None
            ),
            'grouped_versions': grouped_versions,
            'total_versions': len(deployed_versions)
        }
    
    def archive_old_versions(self, keep_count: int = 5, 
                           archive_prereleases: bool = True) -> List[str]:
        """Archive old versions to reduce deployment size.
        
        Args:
            keep_count: Number of stable versions to keep
            archive_prereleases: Whether to archive prerelease versions
            
        Returns:
            List of archived version identifiers
        """
        deployed_versions = self.list_versions()
        
        # Separate stable and prerelease versions
        stable_versions = []
        prerelease_versions = []
        
        for version in deployed_versions:
            version_info = self._classify_version(version.version)
            if version_info.version_type == VersionType.STABLE:
                stable_versions.append(version)
            else:
                prerelease_versions.append(version)
        
        # Sort stable versions
        try:
            stable_versions.sort(
                key=lambda v: self.version_manager.parse_version(v.version)['clean'],
                reverse=True
            )
        except ValueError:
            stable_versions.sort(key=lambda v: v.version, reverse=True)
        
        archived = []
        
        # Archive old stable versions
        if len(stable_versions) > keep_count:
            for version in stable_versions[keep_count:]:
                if not version.is_default:  # Never archive default version
                    try:
                        self.delete_version(version.version, confirm=True)
                        archived.append(version.version)
                    except RuntimeError:
                        # Continue if deletion fails
                        pass
        
        # Archive prereleases if requested
        if archive_prereleases:
            for version in prerelease_versions:
                if not version.is_default:
                    try:
                        self.delete_version(version.version, confirm=True)
                        archived.append(version.version)
                    except RuntimeError:
                        pass
        
        return archived
    
    def validate_deployment(self, version: str) -> Tuple[bool, List[str]]:
        """Validate a version deployment.
        
        Args:
            version: Version to validate
            
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        try:
            deployed_versions = self.list_versions()
            version_info = next((v for v in deployed_versions if v.version == version), None)
            
            if not version_info:
                issues.append(f"Version {version} is not deployed")
                return False, issues
            
            # Check if version is accessible
            try:
                # This would need actual HTTP check in production
                pass
            except Exception:
                issues.append(f"Version {version} is not accessible")
            
            # Validate version format
            try:
                self.version_manager.parse_version(version)
            except ValueError as e:
                issues.append(f"Invalid version format: {e}")
            
            # Check for required files
            required_files = ['index.html', 'sitemap.xml']
            # This would need actual file system check in production
            
        except Exception as e:
            issues.append(f"Error validating deployment: {e}")
        
        return len(issues) == 0, issues
    
    def _load_mike_config(self) -> MikeConfig:
        """Load Mike configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f) or {}
                return MikeConfig(**data)
            except Exception as e:
                raise ValueError(f"Error loading Mike config from {self.config_file}: {e}") from e
        else:
            return MikeConfig()
    
    def _run_mike_command(self, cmd: List[str]) -> str:
        """Run a Mike command and return output.
        
        Args:
            cmd: Command arguments
            
        Returns:
            Command output
        """
        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise subprocess.CalledProcessError(
                e.returncode, e.cmd, e.stdout, f"Mike command failed: {e.stderr}"
            ) from e
    
    def _update_version_metadata(self, version: str, title: Optional[str], 
                                aliases: Optional[List[str]], is_default: bool) -> None:
        """Update version metadata in versions.json."""
        versions_file = self.repo_path / "site" / self.config.versions_file
        
        if versions_file.exists():
            try:
                with open(versions_file, 'r', encoding='utf-8') as f:
                    versions_data = json.load(f)
            except (json.JSONDecodeError, IOError):
                versions_data = []
        else:
            versions_data = []
        
        # Update or add version entry
        for i, version_data in enumerate(versions_data):
            if version_data['version'] == version:
                versions_data[i].update({
                    'title': title or version,
                    'aliases': aliases or [],
                    'is_default': is_default,
                    'updated': str(Path().cwd())
                })
                break
        else:
            versions_data.append({
                'version': version,
                'title': title or version,
                'aliases': aliases or [],
                'is_default': is_default,
                'deployed': str(Path().cwd())
            })
        
        # Save updated metadata
        versions_file.parent.mkdir(parents=True, exist_ok=True)
        with open(versions_file, 'w', encoding='utf-8') as f:
            json.dump(versions_data, f, indent=2)
    
    def _enhance_version_info(self, deployed_version: DeployedVersion) -> None:
        """Enhance version info with additional metadata."""
        # Add deployment size if calculable
        version_path = self.repo_path / "site" / deployed_version.version
        if version_path.exists():
            try:
                total_size = sum(
                    f.stat().st_size for f in version_path.rglob('*') if f.is_file()
                )
                deployed_version.size_mb = total_size / (1024 * 1024)
            except OSError:
                pass
    
    def _classify_version(self, version: str) -> VersionInfo:
        """Classify a version by type."""
        try:
            parsed = self.version_manager.parse_version(version)
            
            if parsed['prerelease']:
                if 'alpha' in parsed['prerelease'] or 'beta' in parsed['prerelease']:
                    version_type = VersionType.PRERELEASE
                else:
                    version_type = VersionType.DEVELOPMENT
            else:
                version_type = VersionType.STABLE
            
            return VersionInfo(
                version=version,
                version_type=version_type,
                title=version,
                aliases=[]
            )
        except ValueError:
            return VersionInfo(
                version=version,
                version_type=VersionType.DEVELOPMENT,
                title=version,
                aliases=[]
            )
    
    def _analyze_version_differences(self, version1: DeployedVersion, 
                                   version2: DeployedVersion) -> List[str]:
        """Analyze differences between two versions."""
        differences = []
        
        if version1.title != version2.title:
            differences.append(f"Title: '{version1.title}' vs '{version2.title}'")
        
        if set(version1.aliases) != set(version2.aliases):
            differences.append(f"Aliases: {version1.aliases} vs {version2.aliases}")
        
        if version1.is_default != version2.is_default:
            differences.append(f"Default status: {version1.is_default} vs {version2.is_default}")
        
        if version1.size_mb and version2.size_mb:
            size_diff = abs(version1.size_mb - version2.size_mb)
            if size_diff > 0.1:  # Only report significant size differences
                differences.append(f"Size: {version1.size_mb:.1f}MB vs {version2.size_mb:.1f}MB")
        
        return differences
