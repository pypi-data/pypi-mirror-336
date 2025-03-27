import json
from pathlib import Path
import pytest
from src.lunar_snippets import Check
import semver


class TestCheck():
    @pytest.fixture(autouse=True)
    def setup_lunar_bundle(self, monkeypatch):
        monkeypatch.setenv(
            'LUNAR_BUNDLE_PATH',
            str(Path(__file__).parent / "sample.json")
        )
        yield

    def test_description_check(self, capsys):
        with Check("test", "description") as c:
            c.assert_true(True)

        captured = capsys.readouterr()
        result = json.loads(captured.out)

        assert result["description"] == "description"

    def test_description_not_in_check(self, capsys):
        with Check("test") as c:
            c.assert_true(True)

        captured = capsys.readouterr()
        result = json.loads(captured.out)

        assert "description" not in result

    def test_paths_in_check(self, capsys):
        with Check("test") as c:
            v = c.get(".const_false")
            c.assert_false(v)
            c.assert_true(".const_true")

        captured = capsys.readouterr()
        result = json.loads(captured.out)

        assert result["paths"] == [".const_false", ".const_true"]

    def test_paths_not_in_check(self, capsys):
        with Check("test") as c:
            c.assert_true(True)

        captured = capsys.readouterr()
        result = json.loads(captured.out)

        assert "paths" not in result

    def test_simple_value_check(self, capsys):
        with Check("test") as c:
            c.assert_true(True)

        captured = capsys.readouterr()
        result = json.loads(captured.out)["assertions"][0]

        assert result["op"] == "true"
        assert result["args"] == ["True"]
        assert result["result"] == "pass"
        assert "failure_message" not in result

    def test_simple_path_check(self, capsys):
        with Check("test") as c:
            c.assert_true(".const_true")

        captured = capsys.readouterr()
        result = json.loads(captured.out)["assertions"][0]

        assert result["op"] == "true"
        assert result["args"] == ["True"]
        assert result["result"] == "pass"
        assert "failure_message" not in result

    def test_multiple_assertions_in_check(self, capsys):
        with Check("test") as c:
            c.assert_true(True)
            c.assert_true(".const_true")

        captured = capsys.readouterr()
        results = json.loads(captured.out)["assertions"]
        assert all(result["result"] == "pass" for result in results)

    def test_all_value_assertions_in_check(self, capsys):
        with Check("test") as c:
            c.assert_true(True)
            c.assert_false(False)
            c.assert_equals(1, 1)
            c.assert_greater(2, 1)
            c.assert_greater_or_equal(2, 1)
            c.assert_greater_or_equal(1, 1)
            c.assert_less(1, 2)
            c.assert_less_or_equal(1, 1)
            c.assert_contains("hello", "e")
            c.assert_match("hello", ".*ell.*")
            c.assert_exists(".const_true")
            c.assert_missing(".not.a.path")

        captured = capsys.readouterr()
        results = json.loads(captured.out)["assertions"]
        assert all(result["result"] == "pass" for result in results)

    def test_semver_comparison(self, capsys):
        with Check("test") as c:
            v1 = semver.Version.parse("1.0.0")
            v2 = semver.Version.parse("2.0.0")

            c.assert_greater_or_equal(v2, v1)
            c.assert_less_or_equal(v1, v2)

        captured = capsys.readouterr()
        results = json.loads(captured.out)["assertions"]
        assert all(result["result"] == "pass" for result in results)

    def test_cannot_report_no_data(self, capsys):
        with Check("test") as c:
            c.assert_missing(".not.a.path")
            c.assert_missing(".const_true")
            c.assert_exists(".const_true")
            c.assert_exists(".not.a.path")

        captured = capsys.readouterr()
        results = json.loads(captured.out)["assertions"]
        assert all(result["result"] != "no_data" for result in results)

    def test_can_report_no_data(self, capsys):
        with Check("test") as c:
            c.assert_true(".not.a.path")
            c.assert_false(".not.a.path")
            c.assert_equals(".not.a.path", 1)
            c.assert_greater(".not.a.path", 1)
            c.assert_greater_or_equal(".not.a.path", 1)
            c.assert_greater_or_equal(".not.a.path", 1)
            c.assert_less(".not.a.path", 1)
            c.assert_less_or_equal(".not.a.path", 1)
            c.assert_contains(".not.a.path", "arg")
            c.assert_match(".not.a.path", "arg")

        captured = capsys.readouterr()
        results = json.loads(captured.out)["assertions"]
        assert all(result["result"] == "no_data" for result in results)
