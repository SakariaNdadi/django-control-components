"""Task sessions. Run ``uv run nox -l`` to list."""

from __future__ import annotations

import glob
import tempfile
import tomllib
from pathlib import Path

import nox

nox.options.default_venv_backend = "uv"
nox.options.reuse_existing_virtualenvs = True

PYTHONS = ["3.12", "3.13"]
DJANGOS = ["5.2", "6.1"]

SECURITY_CRITICAL = [
    "src/django_control_components/htmx.py",
    "src/django_control_components/core/attributes.py",
    "src/django_control_components/schemas/forms_bridge.py",
    "src/django_control_components/images/validators.py",
    "src/django_control_components/tables/query.py",
    "src/django_control_components/actions/registry.py",
]

# These generic rules cannot model DCC's escaped AttributeBag/SafeString
# boundary or Django templates. Dedicated security and invariant tests cover
# those contracts; all other community Django/security rules remain blocking.
SEMGREP_EXCLUDED_RULES = [
    "generic.html-templates.security.unquoted-attribute-var.unquoted-attribute-var",
    "generic.html-templates.security.var-in-href.var-in-href",
    "python.django.security.audit.avoid-mark-safe.avoid-mark-safe",
    "python.flask.security.xss.audit.template-unescaped-with-safe.template-unescaped-with-safe",
    "python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected",
]


def _install(session: nox.Session, *extra: str) -> None:
    session.run_install(
        "uv",
        "sync",
        "--no-default-groups",
        "--group",
        "dev",
        *extra,
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )


@nox.session(python=PYTHONS)
@nox.parametrize("django", DJANGOS)
def tests(session: nox.Session, django: str) -> None:
    _install(session)
    session.install(f"django~={django}.0")
    session.run("pytest", "-q", *session.posargs)


@nox.session
def e2e(session: nox.Session) -> None:
    """Playwright browser tests (tests/e2e). Needs outbound network for CDN assets."""
    session.run_install(
        "uv",
        "sync",
        "--no-default-groups",
        "--group",
        "dev",
        "--group",
        "e2e",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run("playwright", "install", "--with-deps", "chromium")
    session.run(
        "pytest", "-q", "-m", "e2e", "--ds=tests.e2e.settings", "tests/e2e", *session.posargs
    )


@nox.session
def lint(session: nox.Session) -> None:
    _install(session)
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")
    # a model field added without a migration ships broken and nothing else
    # catches it
    session.run(
        "python",
        "-m",
        "django",
        "makemigrations",
        "--check",
        "--dry-run",
        env={"DJANGO_SETTINGS_MODULE": "tests.settings"},
    )


@nox.session
def typecheck(session: nox.Session) -> None:
    _install(session)
    session.run("mypy")


@nox.session
def coverage(session: nox.Session) -> None:
    _install(session)
    session.run("pytest", "-q", "--cov", "--cov-report=term-missing", "--cov-report=xml")
    # Per-module 100% branch floor on the modules where a missed branch is a vuln.
    # (session.run returns str | bool | None, never 0 - the old `== 0` guard made
    # this list always empty and the floor never ran.)
    present = [p for p in SECURITY_CRITICAL if Path(p).is_file()]
    if present:
        session.run("coverage", "report", "--fail-under=100", "--include", ",".join(present))


@nox.session
def security(session: nox.Session) -> None:
    _install(session)
    session.install("semgrep", "pip-audit")
    session.run("ruff", "check", "--select", "S", ".")
    excluded = [item for rule in SEMGREP_EXCLUDED_RULES for item in ("--exclude-rule", rule)]
    session.run(
        "semgrep",
        "--error",
        "--config",
        "p/django",
        "--config",
        "p/security-audit",
        *excluded,
        "src/",
    )
    # Export only third-party runtime dependencies. Strict installed-env mode
    # treats the two unreleased editable workspace packages as collection
    # failures even with --skip-editable.
    requirements = Path(session.create_tmp()) / "audit-requirements.txt"
    session.run(
        "uv",
        "export",
        "--all-extras",
        "--no-dev",
        "--no-emit-workspace",
        "--format",
        "requirements.txt",
        "--output-file",
        str(requirements),
        external=True,
    )
    session.run("pip-audit", "--strict", "--requirement", str(requirements))
    session.run("pytest", "-q", "tests/test_security.py")


@nox.session
def packaging(session: nox.Session) -> None:
    _install(session)
    session.install("twine")
    session.run("uv", "build", "--all-packages", external=True)
    version = tomllib.loads(Path("pyproject.toml").read_text())["project"]["version"]
    artifacts = [Path(path).resolve() for path in glob.glob(f"dist/*-{version}*")]
    wheels = [path for path in artifacts if path.suffix == ".whl"]
    core = next(path for path in wheels if "studio" not in path.name)
    studio = next(path for path in wheels if "studio" in path.name)
    session.run("twine", "check", *(str(path) for path in artifacts))
    session.run(
        "python",
        "-c",
        "import zipfile,sys;"
        "core,studio=sys.argv[1:];"
        "cn=zipfile.ZipFile(core).namelist();"
        "sn=zipfile.ZipFile(studio).namelist();"
        "want=['django_control_components/templates/','django_control_components/static/dcc/dcc.css',"
        "'django_control_components/py.typed'];"
        "missing=[x for x in want if not any(e.startswith(x) or e==x for e in cn)];"
        "missing+=['studio/ leaked into core wheel'] if any('/studio/' in e for e in cn) else [];"
        "missing+=['studio wheel missing templates'] if not any('studio/templates/' in e for e in sn) else [];"
        "missing+=['studio wheel missing py.typed'] if 'django_control_components/studio/py.typed' not in sn else [];"
        "missing+=['studio wheel ships __init__.py'] if 'django_control_components/__init__.py' in sn else [];"
        "sys.exit('packaging check failed: '+str(missing) if missing else 0)",
        str(core),
        str(studio),
    )

    # Prove the artifacts as a consumer sees them: install both wheels in a
    # clean environment, run Django setup, and render through the public API.
    consumer_root = Path(tempfile.mkdtemp(prefix="wheel-consumer-", dir=session.create_tmp()))
    session.run("uv", "venv", str(consumer_root), external=True)
    consumer_python = consumer_root / "bin" / "python"
    session.run(
        "uv",
        "pip",
        "install",
        "--python",
        str(consumer_python),
        str(core),
        str(studio),
        external=True,
    )
    smoke = (
        "from django.conf import settings;"
        "settings.configure(SECRET_KEY='packaging-smoke',DEBUG=True,ROOT_URLCONF='django_control_components.urls',"
        "INSTALLED_APPS=['django.contrib.auth','django.contrib.contenttypes','django_cotton',"
        "'django_control_components','django_control_components.studio'],"
        "DATABASES={'default':{'ENGINE':'django.db.backends.sqlite3','NAME':':memory:'}},"
        "TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','APP_DIRS':True}],"
        "STATIC_URL='/static/');"
        "import django;django.setup();"
        "from django_control_components import __version__;"
        "from django_control_components.core import RenderContext;"
        "from django_control_components.ui import Button;"
        "assert __version__;assert '<button' in str(Button.make('Ready').render(RenderContext()))"
    )
    session.run(str(consumer_python), "-I", "-c", smoke, external=True)
