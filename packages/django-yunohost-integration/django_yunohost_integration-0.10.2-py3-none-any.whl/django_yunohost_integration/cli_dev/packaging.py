import logging

from cli_base.cli_tools.subprocess_utils import ToolsExecutor
from cli_base.cli_tools.verbosity import setup_logging
from cli_base.run_pip_audit import run_pip_audit
from cli_base.tyro_commands import TyroVerbosityArgType
from manageprojects.utilities.publish import publish_package

import django_yunohost_integration
from django_yunohost_integration.cli_dev import PACKAGE_ROOT, app
from django_yunohost_integration.local_test import run_django_test_cli


logger = logging.getLogger(__name__)


@app.command
def install():
    """
    Install requirements and 'django_yunohost_integration' via pip as editable.
    """
    tools_executor = ToolsExecutor(cwd=PACKAGE_ROOT)
    tools_executor.verbose_check_call('uv', 'sync')
    tools_executor.verbose_check_call('pip', 'install', '--no-deps', '-e', '.')


@app.command
def pip_audit(verbosity: TyroVerbosityArgType):
    """
    Run pip-audit check against current requirements files
    """
    setup_logging(verbosity=verbosity)
    run_pip_audit(base_path=PACKAGE_ROOT, verbosity=verbosity)


@app.command
def update(verbosity: TyroVerbosityArgType):
    """
    Update "requirements*.txt" dependencies files
    """
    setup_logging(verbosity=verbosity)

    tools_executor = ToolsExecutor(cwd=PACKAGE_ROOT)

    tools_executor.verbose_check_call('pip', 'install', '-U', 'pip')
    tools_executor.verbose_check_call('pip', 'install', '-U', 'uv')
    tools_executor.verbose_check_call('uv', 'lock', '--upgrade')

    run_pip_audit(base_path=PACKAGE_ROOT, verbosity=verbosity)

    # Install new dependencies in current .venv:
    tools_executor.verbose_check_call('uv', 'sync')

    # Update git pre-commit hooks:
    tools_executor.verbose_check_call('pre-commit', 'autoupdate')


@app.command
def publish():
    """
    Build and upload this project to PyPi
    """
    run_django_test_cli(exit_after_run=False)  # Don't publish a broken state

    publish_package(module=django_yunohost_integration, package_path=PACKAGE_ROOT)
