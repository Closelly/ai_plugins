from __future__ import annotations

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

import importlib.util


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


validate_mod = load_module("validate", ROOT / "scripts" / "validate.py")
package_mod = load_module("package_release", ROOT / "scripts" / "package_release.py")
diagnose_mod = load_module("diagnose", ROOT / "skills" / "diagnose-plugin" / "scripts" / "diagnose.py")


def copy_repo(dst: Path) -> None:
    ignore = shutil.ignore_patterns(".git", "dist", "__pycache__", ".venv")
    shutil.copytree(ROOT, dst, ignore=ignore, dirs_exist_ok=True)


class RepoValidationTests(unittest.TestCase):
    def test_current_repo_is_valid(self) -> None:
        errors = validate_mod.validate(ROOT)
        self.assertEqual(errors, [])

    def test_required_manifests_exist(self) -> None:
        for relative in validate_mod.REQUIRED_FILES:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_identity_fields_match(self) -> None:
        canonical = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        for relative in validate_mod.IDENTITY_MANIFESTS:
            payload = json.loads((ROOT / relative).read_text(encoding="utf-8"))
            for field in ("name", "version", "description"):
                self.assertEqual(payload[field], canonical[field], f"{relative}:{field}")


class FailureModeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        copy_repo(self.tmp)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_version_mismatch_is_reported(self) -> None:
        path = self.tmp / ".claude-plugin" / "plugin.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["version"] = "9.9.9"
        path.write_text(json.dumps(payload), encoding="utf-8")
        errors = validate_mod.validate(self.tmp)
        self.assertTrue(any("version" in error and "9.9.9" in error for error in errors))

    def test_symlink_is_rejected(self) -> None:
        target = self.tmp / "skills" / "diagnose-plugin" / "SKILL.md"
        link = self.tmp / "skills" / "diagnose-plugin" / "COPY.md"
        os.symlink(target.name, link)
        errors = validate_mod.validate(self.tmp)
        self.assertTrue(any("Enlace simbólico" in error for error in errors))

    def test_secret_is_rejected(self) -> None:
        fake_key = "AKIA" + "IOSFODNN7EXAMPLE"
        (self.tmp / "leak.txt").write_text(f"token {fake_key} leaked\n", encoding="utf-8")
        errors = validate_mod.validate(self.tmp)
        self.assertTrue(any("aws-access-key" in error for error in errors))

    def test_active_mcp_file_is_rejected(self) -> None:
        (self.tmp / "mcp.json").write_text('{"mcpServers": {"x": {"type": "http", "url": "https://example.com"}}}', encoding="utf-8")
        errors = validate_mod.validate(self.tmp)
        self.assertTrue(any("MCP remoto" in error for error in errors))

    def test_duplicated_skills_dir_is_rejected(self) -> None:
        extra = self.tmp / ".claude-plugin" / "skills" / "other"
        extra.mkdir(parents=True)
        (extra / "SKILL.md").write_text("---\nname: other\ndescription: x\n---\n", encoding="utf-8")
        errors = validate_mod.validate(self.tmp)
        self.assertTrue(any("Skills duplicadas" in error for error in errors))

    def test_absolute_path_is_rejected(self) -> None:
        path = self.tmp / ".codex-plugin" / "plugin.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["skills"] = "/home/ubuntu/skills/"
        path.write_text(json.dumps(payload), encoding="utf-8")
        errors = validate_mod.validate(self.tmp)
        self.assertTrue(any("absolutas" in error or "skills" in error for error in errors))


class DiagnoseTests(unittest.TestCase):
    def test_report_from_full_repo(self) -> None:
        report = diagnose_mod.build_report(ROOT)
        self.assertIn("plugin.name=closelly-ai-plugins", report)
        self.assertIn("plugin.version=1.1.0", report)
        self.assertIn("identity.consistent=true", report)
        self.assertIn("mcp.remote.enabled=false", report)

    def test_equivalent_name_and_version_across_hosts(self) -> None:
        canonical = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        hosts = {
            "chatgpt-codex": [".codex-plugin/plugin.json"],
            "claude-code": [".claude-plugin/plugin.json"],
            "github-copilot-cli": ["plugin.json"],
        }
        reports: dict[str, str] = {}
        tmp_root = Path(tempfile.mkdtemp())
        try:
            for host, manifests in hosts.items():
                host_dir = tmp_root / host
                host_dir.mkdir()
                skills_src = ROOT / "skills"
                shutil.copytree(skills_src, host_dir / "skills")
                for relative in manifests:
                    src = ROOT / relative
                    dest = host_dir / relative
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dest)
                reports[host] = diagnose_mod.build_report(host_dir)
        finally:
            shutil.rmtree(tmp_root, ignore_errors=True)

        names = {line for report in reports.values() for line in report.splitlines() if line.startswith("plugin.name=")}
        versions = {line for report in reports.values() for line in report.splitlines() if line.startswith("plugin.version=")}
        self.assertEqual(names, {f"plugin.name={canonical['name']}"})
        self.assertEqual(versions, {f"plugin.version={canonical['version']}"})

    def test_host_env_does_not_change_identity(self) -> None:
        original = os.environ.get("CLAUDE_PLUGIN_ROOT")
        os.environ["CLAUDE_PLUGIN_ROOT"] = str(ROOT)
        try:
            report = diagnose_mod.build_report(ROOT)
        finally:
            if original is None:
                os.environ.pop("CLAUDE_PLUGIN_ROOT", None)
            else:
                os.environ["CLAUDE_PLUGIN_ROOT"] = original
        self.assertIn("plugin.name=closelly-ai-plugins", report)
        self.assertIn("plugin.version=1.1.0", report)
        self.assertIn("host=claude-code", report)


class PackageTests(unittest.TestCase):
    def test_zips_include_physical_skills_and_checksums(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        try:
            created = package_mod.package(ROOT, tmp)
            zips = [path for path in created if path.suffix == ".zip"]
            self.assertEqual(len(zips), 3)
            self.assertTrue((tmp / "SHA256SUMS").is_file())
            names = {path.name for path in zips}
            self.assertIn("closelly-ai-plugins-chatgpt-codex-1.1.0.zip", names)
            self.assertIn("closelly-ai-plugins-claude-code-1.1.0.zip", names)
            self.assertIn("closelly-ai-plugins-github-copilot-cli-1.1.0.zip", names)
            import zipfile

            for zip_path in zips:
                with zipfile.ZipFile(zip_path) as zf:
                    self.assertIn("skills/diagnose-plugin/SKILL.md", zf.namelist())
                    self.assertIn("skills/mcp-business/SKILL.md", zf.namelist())
                    self.assertIn("skills/mcp-business/references/tools-reference.md", zf.namelist())
                    self.assertIn("config/mcp.business.json", zf.namelist())
                    self.assertNotIn("mcp.json", zf.namelist())
                    self.assertNotIn(".mcp.json", zf.namelist())
                    self.assertFalse(any("__pycache__" in name or name.endswith(".pyc") for name in zf.namelist()))
                    info = zf.getinfo("skills/diagnose-plugin/SKILL.md")
                    self.assertFalse(stat_is_symlink(info.external_attr))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_tag_mismatch_fails(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        try:
            with self.assertRaises(ValueError):
                package_mod.package(ROOT, tmp, expected_version="v9.9.9")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


def stat_is_symlink(external_attr: int) -> bool:
    return ((external_attr >> 16) & 0o170000) == 0o120000


class McpBusinessTests(unittest.TestCase):
    def test_skill_documents_core_tools_and_oauth_url(self) -> None:
        skill = (ROOT / "skills" / "mcp-business" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: mcp-business", skill)
        self.assertIn("https://auth.closelly.com/mcp/business", skill)
        for tool in ("get_business", "list_courses", "search_students", "export_course_progress"):
            self.assertIn(f"`{tool}`", skill)

    def test_connector_config_is_oauth_without_secrets(self) -> None:
        payload = json.loads((ROOT / "config" / "mcp.business.json").read_text(encoding="utf-8"))
        server = payload["mcpServers"]["closelly-business"]
        self.assertEqual(server["url"], "https://auth.closelly.com/mcp/business")
        self.assertEqual(server["auth"]["type"], "oauth")
        self.assertNotIn("headers", server)
        blob = json.dumps(payload)
        self.assertNotIn("Bearer ", blob)
        plugin = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        business = plugin["extensions"]["com.closelly.mcp"]["business"]
        self.assertEqual(business["url"], server["url"])
        self.assertEqual(business["skill"], "mcp-business")
        self.assertIs(plugin["extensions"]["com.closelly.mcp"]["remote"]["enabled"], False)


if __name__ == "__main__":
    unittest.main()
