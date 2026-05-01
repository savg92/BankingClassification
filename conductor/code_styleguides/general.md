# General Code Style Principles

This document outlines general coding principles that apply across all languages and frameworks used in this project.

## Readability

- Code should be easy to read and understand by humans.
- Avoid overly clever or obscure constructs.

## Consistency

- Follow existing patterns in the codebase.
- Maintain consistent formatting, naming, and structure.

## Simplicity

- Prefer simple solutions over complex ones.
- Break down complex problems into smaller, manageable parts.

## Maintainability

- Write code that is easy to modify and extend.
- Minimize dependencies and coupling.

## Documentation

- Document _why_ something is done, not just _what_.
- Keep documentation up-to-date with code changes.

## Monorepo Import Conventions

- **Absolute Imports**: Use absolute package-based imports for cross-package references.
  - Python: `from apps.backend.models import BankingModel`
  - TypeScript: `import { AnalysisTable } from '@/components/AnalysisTable'`
- **Never Use**: Relative imports with multiple `../`. They obscure actual dependencies and are fragile.
- **Path Aliases**: Configure in `tsconfig.json` (frontend) and `PYTHONPATH` (backend) for consistency.
- **Data File Paths**: Use environment-based discovery for artifact directories (e.g., training models, datasets).

## Error Handling Standards

- **Custom Exceptions**: Create domain-specific exception classes (e.g., `EmbeddingError`, `InferenceError`, `ValidationError`).
- **Error Context**: Always include:
  - What operation failed (e.g., "Failed to fetch embedding")
  - Why it failed (e.g., "LiteLLM returned 503 Service Unavailable")
  - Input context (e.g., text length, user ID if applicable)
  - Suggested recovery action if recoverable
- **Logging**: Use proper logging levels:
  - `DEBUG`: Verbose internal state (e.g., loop iterations, cache hits)
  - `INFO`: Key operations (e.g., "Model loaded successfully")
  - `WARNING`: Recoverable issues (e.g., "Retrying LiteLLM after timeout")
  - `ERROR`: Unrecoverable failures (e.g., "Model file not found")
  - `CRITICAL`: System-level failures (e.g., "Database connection failed")
- **No Print()**: Never use `print()` in production code. Use the logging module exclusively.
- **Exception Chaining**: Preserve original exception context using `raise ... from e` (Python) or `.cause` (JavaScript).

## Testing Standards

- **Coverage**: Target >80% code coverage for all new code.
- **Test Naming**: Use clear, descriptive names that explain what is being tested and the expected outcome.
- **Isolation**: Tests must be independent. No test should depend on another test's side effects.
- **Mocking**: Mock all external dependencies (APIs, databases, file systems) in unit tests.
- **Assertions**: Use specific, descriptive assertions with helpful failure messages.
