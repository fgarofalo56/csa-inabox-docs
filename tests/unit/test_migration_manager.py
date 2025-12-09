"""Unit tests for MigrationManager."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import yaml

from csa_docs_tools.migration_manager import (
    MigrationManager,
    MigrationRule,
    BreakingChange,
    DeprecationNotice,
    MigrationGuide
)


@pytest.fixture
def temp_migration_dir(tmp_path):
    """Create a temporary directory for migration tests."""
    repo_path = tmp_path / "repo"
    repo_path.mkdir()

    # Create migration config directory
    migration_dir = repo_path / "docs" / "migration"
    migration_dir.mkdir(parents=True)

    return repo_path


@pytest.fixture
def migration_manager(temp_migration_dir):
    """Create a MigrationManager instance."""
    return MigrationManager(temp_migration_dir)


@pytest.fixture
def sample_breaking_change():
    """Create a sample breaking change."""
    return BreakingChange(
        change_id="bc_001",
        title="API Endpoint Changed",
        description="The /api/v1/users endpoint has been moved to /api/v2/users",
        introduced_in="2.0.0",
        affects=["api", "content"],
        migration_steps=[
            "Update all API endpoint references",
            "Test API calls",
            "Update documentation"
        ],
        severity="high"
    )


@pytest.fixture
def sample_deprecation():
    """Create a sample deprecation notice."""
    return DeprecationNotice(
        notice_id="dep_001",
        title="Old Configuration Format",
        description="The old YAML configuration format is deprecated",
        deprecated_in="1.5.0",
        removal_planned="2.0.0",
        replacement="New JSON configuration format",
        affected_pages=["config/setup.md"]
    )


@pytest.fixture
def sample_migration_rule():
    """Create a sample migration rule."""
    return MigrationRule(
        rule_id="rule_001",
        name="Move configuration files",
        description="Move config files from old location to new location",
        from_version="1.0.0",
        to_version="2.0.0",
        rule_type="structure",
        action="move",
        source_path="config/old_config.yml",
        target_path="config/new_config.yml",
        is_breaking=False
    )


class TestMigrationManager:
    """Test suite for MigrationManager."""

    def test_init(self, migration_manager, temp_migration_dir):
        """Test MigrationManager initialization."""
        assert migration_manager.repo_path == temp_migration_dir
        assert migration_manager.config_dir.exists()
        assert isinstance(migration_manager.migration_rules, list)
        assert isinstance(migration_manager.breaking_changes, list)
        assert isinstance(migration_manager.deprecations, list)

    def test_add_breaking_change(self, migration_manager, sample_breaking_change):
        """Test adding a breaking change."""
        migration_manager.add_breaking_change(sample_breaking_change)

        assert len(migration_manager.breaking_changes) == 1
        assert migration_manager.breaking_changes[0].change_id == "bc_001"

        # Verify file was created
        breaking_changes_file = migration_manager.config_dir / "breaking_changes.yml"
        assert breaking_changes_file.exists()

    def test_add_breaking_change_update_existing(self, migration_manager, sample_breaking_change):
        """Test updating an existing breaking change."""
        # Add first time
        migration_manager.add_breaking_change(sample_breaking_change)

        # Update with same ID
        updated_change = BreakingChange(
            change_id="bc_001",
            title="Updated API Endpoint Changed",
            description="Updated description",
            introduced_in="2.0.0",
            affects=["api"],
            migration_steps=["Updated step"],
            severity="critical"
        )
        migration_manager.add_breaking_change(updated_change)

        # Should still have only one change
        assert len(migration_manager.breaking_changes) == 1
        assert migration_manager.breaking_changes[0].title == "Updated API Endpoint Changed"
        assert migration_manager.breaking_changes[0].severity == "critical"

    def test_add_deprecation_notice(self, migration_manager, sample_deprecation):
        """Test adding a deprecation notice."""
        migration_manager.add_deprecation_notice(sample_deprecation)

        assert len(migration_manager.deprecations) == 1
        assert migration_manager.deprecations[0].notice_id == "dep_001"

        # Verify file was created
        deprecations_file = migration_manager.config_dir / "deprecations.yml"
        assert deprecations_file.exists()

    def test_add_migration_rule(self, migration_manager, sample_migration_rule):
        """Test adding a migration rule."""
        migration_manager.add_migration_rule(sample_migration_rule)

        assert len(migration_manager.migration_rules) == 1
        assert migration_manager.migration_rules[0].rule_id == "rule_001"

        # Verify file was created
        migration_rules_file = migration_manager.config_dir / "migration_rules.yml"
        assert migration_rules_file.exists()

    def test_create_migration_guide_patch_version(self, migration_manager):
        """Test creating migration guide for patch version."""
        guide = migration_manager.create_migration_guide("1.0.0", "1.0.1")

        assert guide.from_version == "1.0.0"
        assert guide.to_version == "1.0.1"
        assert guide.estimated_effort == "Low"
        assert "Patch upgrade" in guide.overview
        assert len(guide.migration_steps) > 0

    def test_create_migration_guide_minor_version(self, migration_manager):
        """Test creating migration guide for minor version."""
        guide = migration_manager.create_migration_guide("1.0.0", "1.1.0")

        assert guide.from_version == "1.0.0"
        assert guide.to_version == "1.1.0"
        assert guide.estimated_effort == "Medium"
        assert "Minor version upgrade" in guide.overview

    def test_create_migration_guide_major_version(self, migration_manager):
        """Test creating migration guide for major version."""
        guide = migration_manager.create_migration_guide("1.0.0", "2.0.0")

        assert guide.from_version == "1.0.0"
        assert guide.to_version == "2.0.0"
        assert guide.estimated_effort == "High"
        assert "Major version upgrade" in guide.overview

    def test_create_migration_guide_with_breaking_changes(self, migration_manager, sample_breaking_change):
        """Test creating migration guide with breaking changes."""
        # Add breaking change that applies to this range
        migration_manager.add_breaking_change(sample_breaking_change)

        guide = migration_manager.create_migration_guide("1.0.0", "2.0.0")

        assert len(guide.breaking_changes) == 1
        assert guide.breaking_changes[0].change_id == "bc_001"

    def test_create_migration_guide_invalid_version(self, migration_manager):
        """Test creating migration guide with invalid version format."""
        with pytest.raises(ValueError, match="Invalid version format"):
            migration_manager.create_migration_guide("invalid", "1.0.0")

    def test_validate_backward_compatibility_no_issues(self, migration_manager):
        """Test backward compatibility validation with no issues."""
        is_compatible, issues = migration_manager.validate_backward_compatibility("1.0.0")

        assert is_compatible is True
        assert len(issues) == 0

    def test_validate_backward_compatibility_with_critical_change(self, migration_manager):
        """Test backward compatibility with critical breaking change."""
        critical_change = BreakingChange(
            change_id="bc_critical",
            title="Critical API Change",
            description="Critical change",
            introduced_in="1.0.0",
            affects=["api"],
            migration_steps=["Fix API calls"],
            severity="critical"
        )
        migration_manager.add_breaking_change(critical_change)

        is_compatible, issues = migration_manager.validate_backward_compatibility("1.5.0")

        assert is_compatible is False
        assert len(issues) > 0
        assert any("Critical breaking change" in issue for issue in issues)

    def test_generate_deprecation_warnings(self, migration_manager, sample_deprecation):
        """Test generating deprecation warnings."""
        migration_manager.add_deprecation_notice(sample_deprecation)

        warnings = migration_manager.generate_deprecation_warnings("1.6.0")

        assert len(warnings) > 0
        assert warnings[0]['id'] == "dep_001"
        assert warnings[0]['urgency'] in ['low', 'medium', 'high']

    def test_generate_deprecation_warnings_urgency_calculation(self, migration_manager):
        """Test deprecation warning urgency calculation."""
        # Same major version removal = high urgency
        deprecation = DeprecationNotice(
            notice_id="dep_urgent",
            title="Urgent Deprecation",
            description="Will be removed soon",
            deprecated_in="1.0.0",
            removal_planned="1.5.0"
        )
        migration_manager.add_deprecation_notice(deprecation)

        warnings = migration_manager.generate_deprecation_warnings("1.2.0")

        assert len(warnings) == 1
        assert warnings[0]['urgency'] == 'high'

    def test_create_migration_checklist(self, migration_manager):
        """Test creating migration checklist."""
        checklist = migration_manager.create_migration_checklist("1.0.0", "2.0.0")

        assert isinstance(checklist, list)
        assert len(checklist) > 0

        # Check for required categories
        categories = [item['category'] for item in checklist]
        assert 'Pre-Migration' in categories
        assert 'Testing' in categories
        assert 'Post-Migration' in categories

    def test_create_migration_checklist_with_breaking_changes(self, migration_manager, sample_breaking_change):
        """Test migration checklist includes breaking changes."""
        migration_manager.add_breaking_change(sample_breaking_change)

        checklist = migration_manager.create_migration_checklist("1.0.0", "2.0.0")

        categories = [item['category'] for item in checklist]
        assert 'Breaking Changes' in categories

    def test_apply_migration_rules_dry_run(self, migration_manager, sample_migration_rule):
        """Test applying migration rules in dry run mode."""
        migration_manager.add_migration_rule(sample_migration_rule)

        results = migration_manager.apply_migration_rules("1.0.0", "2.0.0", dry_run=True)

        assert results['dry_run'] is True
        assert isinstance(results['applied_rules'], list)
        assert isinstance(results['failed_rules'], list)

    def test_load_migration_config_from_files(self, temp_migration_dir):
        """Test loading migration configuration from existing files."""
        # Create config files
        migration_dir = temp_migration_dir / "docs" / "migration"
        migration_dir.mkdir(parents=True)

        # Create breaking changes file
        breaking_changes_data = {
            'breaking_changes': [{
                'change_id': 'bc_load',
                'title': 'Loaded Change',
                'description': 'Test',
                'introduced_in': '1.0.0',
                'affects': ['api'],
                'migration_steps': ['Step 1'],
                'workaround': None,
                'severity': 'high'
            }]
        }

        with open(migration_dir / "breaking_changes.yml", 'w') as f:
            yaml.dump(breaking_changes_data, f)

        # Initialize manager - should load config
        manager = MigrationManager(temp_migration_dir)

        assert len(manager.breaking_changes) == 1
        assert manager.breaking_changes[0].change_id == 'bc_load'

    def test_save_migration_guide_to_file(self, migration_manager, tmp_path):
        """Test saving migration guide to file."""
        output_path = tmp_path / "migration_guide.md"

        guide = migration_manager.create_migration_guide(
            "1.0.0", "2.0.0",
            output_path=output_path
        )

        assert output_path.exists()
        content = output_path.read_text()

        assert guide.title in content
        assert "1.0.0" in content
        assert "2.0.0" in content
        assert "Migration Steps" in content

    def test_migration_rule_conditions(self, migration_manager):
        """Test migration rule with conditions."""
        rule = MigrationRule(
            rule_id="rule_conditional",
            name="Conditional Rule",
            description="Rule with conditions",
            from_version="1.0.0",
            to_version="2.0.0",
            rule_type="content",
            action="transform",
            source_path="docs/test.md",
            conditions=["file_exists:docs/test.md"]
        )

        migration_manager.add_migration_rule(rule)

        # Test rule applicability with conditions
        is_applicable = migration_manager._is_rule_applicable(rule, "1.0.0", "2.0.0")

        # Should return a boolean
        assert isinstance(is_applicable, bool)

    def test_generate_testing_checklist(self, migration_manager):
        """Test generating testing checklist."""
        checklist = migration_manager._generate_testing_checklist("1.0.0", "2.0.0")

        assert isinstance(checklist, list)
        assert len(checklist) > 0
        assert any("Documentation builds" in item for item in checklist)
        assert any("links" in item.lower() for item in checklist)


class TestMigrationDataClasses:
    """Test migration data classes."""

    def test_migration_rule_creation(self):
        """Test MigrationRule creation."""
        rule = MigrationRule(
            rule_id="test_rule",
            name="Test Rule",
            description="Test description",
            from_version="1.0.0",
            to_version="2.0.0",
            rule_type="content",
            action="copy",
            source_path="src/test.md",
            target_path="dst/test.md"
        )

        assert rule.rule_id == "test_rule"
        assert rule.action == "copy"
        assert rule.is_breaking is False

    def test_breaking_change_creation(self):
        """Test BreakingChange creation."""
        change = BreakingChange(
            change_id="bc_test",
            title="Test Change",
            description="Test",
            introduced_in="2.0.0",
            affects=["api", "ui"],
            migration_steps=["Step 1", "Step 2"]
        )

        assert change.change_id == "bc_test"
        assert len(change.affects) == 2
        assert change.severity == "high"  # Default value

    def test_deprecation_notice_creation(self):
        """Test DeprecationNotice creation."""
        notice = DeprecationNotice(
            notice_id="dep_test",
            title="Test Deprecation",
            description="Test",
            deprecated_in="1.5.0",
            removal_planned="2.0.0"
        )

        assert notice.notice_id == "dep_test"
        assert notice.removal_planned == "2.0.0"

    def test_migration_guide_creation(self):
        """Test MigrationGuide creation."""
        guide = MigrationGuide(
            from_version="1.0.0",
            to_version="2.0.0",
            title="Migration Guide",
            overview="Test overview"
        )

        assert guide.from_version == "1.0.0"
        assert guide.to_version == "2.0.0"
        assert guide.estimated_effort == "Medium"  # Default value
        assert len(guide.breaking_changes) == 0  # Default empty list
