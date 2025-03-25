import pytest
import kthutils.forms
import pathlib
import tempfile
import typer.testing
import kthutils.credentials
import os

config = kthutils.forms.typerconf
class FakeAppDirs:
  def __init__(self):
    self.tmpdir_data = tempfile.TemporaryDirectory()
    self.user_data_dir = pathlib.Path(self.tmpdir_data.name)
    self.tmpdir_config = tempfile.TemporaryDirectory()
    self.user_config_dir = pathlib.Path(self.tmpdir_config.name)

config.dirs = FakeAppDirs()
runner = typer.testing.CliRunner()
forms_cli = kthutils.forms.cli
added_forms = kthutils.forms.CONFIG_ADDED_FORMS
forms = kthutils.forms.FormsSession(*kthutils.credentials.get_credentials())
restlabb_url = "https://www.kth.se/form/admin/api/webform/64ec8baa917ea4c31c33267e/answer/export"

def test_add_form():
  result = runner.invoke(forms_cli, [
    "add", "restlabb", "https://..."
  ])
  assert result.exit_code == 0
  assert "restlabb" in config.get(added_forms)
def test_add_form_with_period():
  result = runner.invoke(forms_cli, [
    "add", "restlabb.2023",
    "https://..."
  ])
  assert result.exit_code != 0
  assert "restlabb.2023" not in config.get(added_forms)
def test_get_added_forms():
  config.set(f"{added_forms}.restlabb", "https://...")
  assert "restlabb" in kthutils.forms.get_added_forms()
  assert "restlabb" in kthutils.forms.get_added_forms("rest")
  assert "nonexisting" not in kthutils.forms.get_added_forms()
def test_get_data_by_url():
  data, content_type = forms.get_data_by_url(restlabb_url)
  assert content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
  assert data.startswith(b"PK")
def test_get_csv_by_url():
  csvdata = forms.get_csv_by_url(restlabb_url)
  assert "Svarsdatum" in csvdata[0] and "Kurs" in csvdata[0]
  assert "Svarsdatum" in csvdata[0] and "Kurs" in csvdata[0]
def test_cli_export_command():
  result = runner.invoke(forms_cli, [
    "add", "restlabb", restlabb_url
  ])
  assert result.exit_code == 0
  assert "restlabb" in config.get(added_forms)
  result = runner.invoke(forms_cli, [
    "export", "restlabb"
  ])
  assert result.exit_code == 0
  assert "Svarsdatum" in result.stdout
  assert "Bosk" in result.stdout
def test_export_function():
  result = runner.invoke(forms_cli, [
    "add", "restlabb", restlabb_url
  ])
  assert result.exit_code == 0
  assert "restlabb" in config.get(added_forms)
  csvdata = kthutils.forms.export("restlabb")
  assert "Svarsdatum" in csvdata[0]
def test_export_delimiter():
  result = runner.invoke(forms_cli, [
    "add", "restlabb", restlabb_url
  ])
  assert result.exit_code == 0
  assert "restlabb" in config.get(added_forms)
  result = runner.invoke(forms_cli, [
    "export", "restlabb", "--delimiter", ","
  ])
  assert result.exit_code == 0
  assert "Svarsdatum,Studentens namn" in result.stdout

  result = runner.invoke(forms_cli, [
    "export", "restlabb"
  ])
  assert result.exit_code == 0
  assert "Svarsdatum\tStudentens namn" in result.stdout
def test_next_command():
  config.dirs = FakeAppDirs()
  result = runner.invoke(forms_cli, [
    "add", "restlabb", restlabb_url
  ])
  assert result.exit_code == 0
  assert "restlabb" in config.get(added_forms)
  result = runner.invoke(forms_cli, [
    "add", "test",
    "https://www.kth.se/form/admin/api/webform/65bbb936dcba25abb5f696da/answer/export"
  ])
  result = runner.invoke(forms_cli, [
    "next", "restlabb"
  ])
  assert result.exit_code == 0
  assert "Svarsdatum" in result.stdout
  assert "Bosk" in result.stdout

  result = runner.invoke(forms_cli, [
    "next", "restlabb"
  ])
  assert result.exit_code == 0
  assert "Svarsdatum" not in result.stdout
  assert "Bosk" not in result.stdout

def test_next_function():
  config.dirs = FakeAppDirs()
  result = runner.invoke(forms_cli, [
    "add", "restlabb", restlabb_url
  ])
  assert result.exit_code == 0
  assert "restlabb" in config.get(added_forms)
  result = runner.invoke(forms_cli, [
    "add", "test",
    "https://www.kth.se/form/admin/api/webform/65bbb936dcba25abb5f696da/answer/export"
  ])
  csvdata = kthutils.forms.next("restlabb")
  assert "Svarsdatum" in csvdata[0]
  csvdata = kthutils.forms.next("restlabb")
  assert not csvdata
  csvdata = kthutils.forms.next("test")
  assert "Name" in csvdata[0] and "Daniel" in csvdata[1]
  csvdata = kthutils.forms.next("restlabb")
  assert not csvdata
  csvdata = kthutils.forms.next("test")
  assert not csvdata
