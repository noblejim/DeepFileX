# DeepFileX Tests

This directory contains all test files for DeepFileX.

---

## 📋 Test Files

### `test_ad_banner.py`
Tests for the advertising banner system.
- Banner display functionality
- Ad loading and rendering
- Click tracking

### `test_webengine.py`
Tests for QWebEngineView integration.
- WebEngine initialization
- Page loading
- Navigation handling

### `test_search.py` (to be added)
Tests for the search functionality.
- Search query processing
- Result display
- Exception handling

---

## 🚀 Running Tests

### Run all tests
```bash
python -m pytest tests/
```

### Run specific test file
```bash
python tests/test_ad_banner.py
```

### Run with coverage
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

---

## 📝 Test Guidelines

1. **Naming Convention**: All test files must start with `test_`
2. **Test Functions**: All test functions must start with `test_`
3. **Documentation**: Add docstrings to all test functions
4. **Coverage**: Aim for >80% code coverage
5. **Independence**: Tests should not depend on each other

---

## 🐛 Bug Fix Tests

When fixing bugs, always add a test that:
1. Reproduces the bug
2. Verifies the fix
3. Prevents regression

Example: v1.4.1 search crash bug should have a test that:
- Loads an index
- Performs a search
- Verifies no crash occurs

---

**DeepFileX by QuantumLayer** 🔷
