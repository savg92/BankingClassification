# Google Python Style Guide Summary

This document summarizes key rules and best practices from the Google Python Style Guide.

## 1. Python Language Rules

- **Linting:** Run `pylint` on your code to catch bugs and style issues.
- **Imports:** Use `import x` for packages/modules. Use `from x import y` only when `y` is a submodule.
- **Exceptions:** Use built-in exception classes. Do not use bare `except:` clauses.
- **Global State:** Avoid mutable global state. Module-level constants are okay and should be `ALL_CAPS_WITH_UNDERSCORES`.
- **Comprehensions:** Use for simple cases. Avoid for complex logic where a full loop is more readable.
- **Default Argument Values:** Do not use mutable objects (like `[]` or `{}`) as default values.
- **True/False Evaluations:** Use implicit false (e.g., `if not my_list:`). Use `if foo is None:` to check for `None`.
- **Type Annotations:** Strongly encouraged for all public APIs.

## 2. Python Style Rules

- **Line Length:** Maximum 80 characters.
- **Indentation:** 4 spaces per indentation level. Never use tabs.
- **Blank Lines:** Two blank lines between top-level definitions (classes, functions). One blank line between method definitions.
- **Whitespace:** Avoid extraneous whitespace. Surround binary operators with single spaces.
- **Docstrings:** Use `"""triple double quotes"""`. Every public module, function, class, and method must have a docstring.
  - **Format:** Start with a one-line summary. Include `Args:`, `Returns:`, and `Raises:` sections.
- **Strings:** Use f-strings for formatting. Be consistent with single (`'`) or double (`"`) quotes.
- **`TODO` Comments:** Use `TODO(username): Fix this.` format.
- **Imports Formatting:** Imports should be on separate lines and grouped: standard library, third-party, and your own application's imports.

## 3. Naming

- **General:** `snake_case` for modules, functions, methods, and variables.
- **Classes:** `PascalCase`.
- **Constants:** `ALL_CAPS_WITH_UNDERSCORES`.
- **Internal Use:** Use a single leading underscore (`_internal_variable`) for internal module/class members.

## 4. Main

- All executable files should have a `main()` function that contains the main logic, called from a `if __name__ == '__main__':` block.

## 5. Testing & Pytest Conventions

- **Test File Naming**: Use `test_<module_name>.py` for unit tests. Place in same directory or `/tests` folder.
- **Test Function Naming**: `test_<function_or_class>_<scenario>` (e.g., `test_inference_service_with_valid_embedding`).
- **Fixtures**: Use `@pytest.fixture` for setup/teardown. Define in conftest.py for shared fixtures.
- **Mocking**: Use `pytest-mock` to intercept external calls (LiteLLM, file I/O).
  - Example: `mocker.patch('litellm.embedding', return_value=mock_vector)`
- **Assertions**: Use descriptive assertion messages. For example:
  ```python
  assert result['probability'] > 0.3, f"Expected probability > 0.3, got {result['probability']}"
  ```
- **Coverage**: Run with `pytest --cov=app --cov-report=html`. Target >80% for new code.
- **CI Integration**: Use `CI=true pytest` for non-interactive, single-pass execution.

## 6. Monorepo Import Conventions

- **Internal Imports**: Use absolute paths with package root as base.

  ```python
  # ✅ Good
  from apps.backend.models import BankingModel
  from apps.backend.utils import embed_text

  # ❌ Avoid
  from ..models import BankingModel
  ```

- **Data Files**: Use `pathlib.Path` with environment-based root discovery:
  ```python
  from pathlib import Path
  PROJECT_ROOT = Path(__file__).parent.parent.parent
  MODELS_DIR = PROJECT_ROOT / "training" / "artifacts"
  ```

## 7. Error Handling & Logging

- **Custom Exceptions**: Create domain-specific exceptions (e.g., `EmbeddingError`, `InferenceError`).
- **Error Context**: Always include what operation failed and why.
  ```python
  logger.error(f"Failed to fetch embedding for text (len={len(text)}): {str(e)}", exc_info=True)
  ```
- **Logging Levels**: WARN for recoverable (e.g., LiteLLM retry), ERROR for unrecoverable (e.g., model load failure).
- **No Print()**: Use `logging` module exclusively.

## 8. FastAPI Conventions

- **Response Models**: Use Pydantic models for all responses. No dict return types.
- **Status Codes**: Use explicit status codes (422 for validation, 504 for gateway timeout, 500 for model failure).
- **CORS**: Always validate CORS origins. Never use `allow_origins=["*"]` in production.

**BE CONSISTENT.** When editing code, match the existing style.

_Source: [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)_
