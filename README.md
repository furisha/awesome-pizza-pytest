# 🍕 Awesome Pizza — Pytest + Playwright Test Framework

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-9.x-orange?logo=pytest&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-1.44%2B-2EAD33?logo=playwright&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blue?logo=githubactions&logoColor=white)

End-to-end UI test framework for the Awesome Pizza application, built with **Pytest** and **Playwright** following the **Page Object Model** pattern. Supports multi-environment execution, parallel runs, and rich failure artifacts (screenshots, videos, traces).

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Tech Stack](#-tech-stack)
- [Folder Structure](#-folder-structure)
- [Installation](#-installation)
- [How to Run Tests](#-how-to-run-tests)
- [Environment Configuration](#-environment-configuration)
- [Reporting](#-reporting)
- [Debugging](#-debugging)
- [Trace Viewer](#-trace-viewer)
- [Screenshots & Video](#-screenshots--video)
- [GitHub Actions / CI](#-github-actions--ci)
- [Best Practices](#-best-practices)
- [Common Commands](#-common-commands)
- [Contribution Guidelines](#-contribution-guidelines)

---

## 🧾 Project Overview

This framework automates end-to-end testing of the Awesome Pizza web application. It covers:

- Menu display and item management
- Cart operations (add, remove, quantity adjustments)
- Order placement and confirmation
- Order lookup and status transitions (RECEIVED → DELIVERING → DELIVERED)
- Theme switching (dark / light mode)

Tests are organized by feature, use a shared `PageManager` for clean page access, and are designed to run reliably in CI pipelines with automatic trace capture on failure.

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| [Python 3.11+](https://www.python.org/) | Language |
| [Pytest 9.x](https://docs.pytest.org/) | Test runner and assertions |
| [Playwright 1.44+](https://playwright.dev/python/) | Browser automation |
| [pytest-playwright](https://playwright.dev/python/docs/test-runners) | Playwright fixtures for pytest |
| [pytest-xdist](https://pytest-xdist.readthedocs.io/) | Parallel test execution |
| [pytest-html](https://pytest-html.readthedocs.io/) | HTML test reports |

---

## 📁 Folder Structure

```
awesome-pizza-pytest/
├── .github/
│   └── workflows/
│       └── tests.yml          # GitHub Actions CI pipeline
├── config/
│   ├── dev.env                # Dev environment variables
│   ├── staging.env            # Staging environment variables
│   └── production.env         # Production environment variables
├── pages/
│   ├── base_page.py           # Shared navigation and wait helpers
│   ├── home_page.py           # Menu and item interactions
│   ├── order_page.py          # Cart, checkout, and order lookup
│   ├── navigation_page.py     # Header, notifications, theme toggle
│   └── page_manager.py        # Single entry point to all page objects
├── testdata/
│   └── pizza_data.py          # Test data models and fixtures
├── tests/
│   └── test_pizza_ordering.py # All E2E test cases
├── utils/
│   └── helpers.py             # Reusable utility functions
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python dependencies
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-org/awesome-pizza-pytest.git
cd awesome-pizza-pytest
```

### 2. Create and activate a virtual environment

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell)**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers

```bash
playwright install
```

To install only a specific browser:
```bash
playwright install chromium
playwright install firefox
playwright install webkit
```

---

## ▶️ How to Run Tests

### Run all tests

```bash
pytest
```

### Run a specific test file

```bash
pytest tests/test_pizza_ordering.py
```

### Run a specific test class or test

```bash
pytest tests/test_pizza_ordering.py::TestCart
pytest tests/test_pizza_ordering.py::TestCart::test_add_item_increments_cart_total
```

### Run by marker

```bash
pytest -m smoke
pytest -m "regression and not slow"
```

### Run in headed mode (visible browser)

```bash
pytest --headed
```

### Run in parallel

```bash
# Run with 4 workers
pytest -n 4

# Auto-detect CPU count
pytest -n auto
```

### Run against a specific browser

```bash
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
```

### Run with slow motion (useful for debugging)

```bash
pytest --headed --slowmo 500
```

---

## 🌍 Environment Configuration

The target URL is set in [pytest.ini](pytest.ini):

```ini
[pytest]
base_url = http://localhost:3000
addopts = --tracing=retain-on-failure
testpaths = tests
```

Override `base_url` at runtime to point at any environment:

```bash
# Staging
pytest --base-url https://staging.awesome-pizza.com

# Production
pytest --base-url https://awesome-pizza.com
```

### Example `.env` file

Create a `config/dev.env` for local development:

```env
BASE_URL=http://localhost:3000
API_BASE_URL=http://localhost:3001
BROWSER=chromium
HEADLESS=true
SLOW_MO=0
```

Load it before running tests:

```bash
# macOS / Linux
export $(cat config/dev.env | xargs) && pytest

# Windows PowerShell
Get-Content config\dev.env | ForEach-Object { $k, $v = $_ -split '=', 2; [System.Environment]::SetEnvironmentVariable($k, $v) }; pytest
```

---

## 📊 Reporting

### Terminal output

By default, pytest prints results to the terminal. For verbose output:

```bash
pytest -v
```

### HTML report

Generate a self-contained HTML report:

```bash
pytest --html=reports/report.html --self-contained-html
```

Open `reports/report.html` in any browser after the run.

### JUnit XML (for CI)

```bash
pytest --junitxml=reports/junit.xml
```

---

## 🐛 Debugging

### Print page content on failure

Add `--capture=no` to see stdout during the run:

```bash
pytest -s
```

### Drop into Playwright inspector

Set `PWDEBUG=1` to pause execution and open the inspector:

```bash
# macOS / Linux
PWDEBUG=1 pytest --headed tests/test_pizza_ordering.py::TestCart::test_add_item_increments_cart_total

# Windows PowerShell
$env:PWDEBUG=1; pytest --headed tests/test_pizza_ordering.py::TestCart::test_add_item_increments_cart_total
```

### Run in headed mode with slowmo

```bash
pytest --headed --slowmo 1000 -k "test_place_order"
```

---

## 🔍 Trace Viewer

Traces are captured automatically on failure (`--tracing=retain-on-failure` is set in `pytest.ini`).

After a failing run, open the trace:

```bash
playwright show-trace test-results/<test-name>/trace.zip
```

Or open any `.zip` trace via the online viewer:
[trace.playwright.dev](https://trace.playwright.dev)

To always capture traces (regardless of pass/fail):

```bash
pytest --tracing=on
```

---

## 📸 Screenshots & Video

### Screenshots on failure

```bash
pytest --screenshot=only-on-failure
```

Screenshots are saved to `test-results/` with the test name as the filename.

### Screenshots always

```bash
pytest --screenshot=on
```

### Video recording

```bash
# Record only on failure
pytest --video=retain-on-failure

# Record all tests
pytest --video=on
```

Videos are saved to `test-results/<test-name>/video.webm`.

### Full failure artifacts (recommended for CI)

```bash
pytest --screenshot=only-on-failure --video=retain-on-failure --tracing=retain-on-failure
```

---

## 🚀 GitHub Actions / CI

Create `.github/workflows/tests.yml`:

```yaml
name: E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        browser: [chromium, firefox, webkit]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Install Playwright browsers
        run: playwright install --with-deps ${{ matrix.browser }}

      - name: Run tests
        run: |
          pytest \
            --browser ${{ matrix.browser }} \
            --screenshot=only-on-failure \
            --video=retain-on-failure \
            --tracing=retain-on-failure \
            --html=reports/report-${{ matrix.browser }}.html \
            --self-contained-html \
            -n auto

      - name: Upload test artifacts
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: test-results-${{ matrix.browser }}
          path: |
            test-results/
            reports/
          retention-days: 7
```

---

## ✅ Best Practices

- **Page Object Model** — all selectors and interactions live in `/pages`, never in test files.
- **`PageManager`** — use it as the single access point to page objects; avoids direct page instantiation in tests.
- **No hard `sleep` calls** — use Playwright's built-in auto-waiting or explicit `wait_for` methods.
- **Isolated tests** — each test starts from a clean state; no shared mutable state between tests.
- **Descriptive test names** — test names should read like sentences describing the expected behavior.
- **Markers** — tag tests with `@pytest.mark.smoke`, `@pytest.mark.regression`, etc., to allow targeted runs.
- **Fixtures over setup/teardown** — use pytest fixtures for reusable test setup and dependency injection.
- **Retain artifacts on failure only** — avoids filling disk on large parallel runs.

---

## 💻 Common Commands

```bash
# Install everything from scratch
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && playwright install

# Run all tests headlessly (default)
pytest

# Run all tests headed with verbose output
pytest --headed -v

# Run smoke suite in parallel on staging
pytest -m smoke -n auto --base-url https://staging.awesome-pizza.com

# Run a single test with full debug artifacts
pytest --headed --slowmo 500 --screenshot=on --video=on --tracing=on -k "test_place_order_shows_success_notification"

# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# View a trace file
playwright show-trace test-results/trace.zip

# Open Playwright inspector for a specific test
PWDEBUG=1 pytest --headed -k "test_theme_toggle"

# Update requirements after adding a package
pip freeze > requirements.txt
```

---

## 🤝 Contribution Guidelines

1. **Fork** the repository and create a feature branch from `main`.
2. Follow the existing **Page Object Model** structure — add new page classes to `/pages` and register them in `PageManager`.
3. Write **tests in `/tests`** — one file per feature area.
4. Use **pytest markers** to categorize new tests (`smoke`, `regression`, `slow`).
5. Ensure all tests **pass locally** before opening a PR:
   ```bash
   pytest -n auto
   ```
6. Keep PRs **focused** — one feature or fix per PR.
7. Update this README if you add new configuration options, environment variables, or test commands.

---

> Built with ❤️ and Playwright. Happy testing! 🍕
