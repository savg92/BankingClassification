# Google JavaScript Style Guide Summary

This document summarizes key rules and best practices from the Google JavaScript Style Guide.

## 1. Source File Basics

- **File Naming:** All lowercase, with underscores (`_`) or dashes (`-`). Extension must be `.js`.
- **File Encoding:** UTF-8.
- **Whitespace:** Use only ASCII horizontal spaces (0x20). Tabs are forbidden for indentation.

## 2. Source File Structure

- New files should be ES modules (`import`/`export`).
- **Exports:** Use named exports (`export {MyClass};`). **Do not use default exports.**
- **Imports:** Do not use line-wrapped imports. The `.js` extension in import paths is mandatory.

## 3. Formatting

- **Braces:** Required for all control structures (`if`, `for`, `while`, etc.), even single-line blocks. Use K&R style ("Egyptian brackets").
- **Indentation:** +2 spaces for each new block.
- **Semicolons:** Every statement must be terminated with a semicolon.
- **Column Limit:** 80 characters.
- **Line-wrapping:** Indent continuation lines at least +4 spaces.
- **Whitespace:** Use single blank lines between methods. No trailing whitespace.

## 4. Language Features

- **Variable Declarations:** Use `const` by default, `let` if reassignment is needed. **`var` is forbidden.**
- **Array Literals:** Use trailing commas. Do not use the `Array` constructor.
- **Object Literals:** Use trailing commas and shorthand properties. Do not use the `Object` constructor.
- **Classes:** Do not use JavaScript getter/setter properties (`get name()`). Provide ordinary methods instead.
- **Functions:** Prefer arrow functions for nested functions to preserve `this` context.
- **String Literals:** Use single quotes (`'`). Use template literals (`` ` ``) for multi-line strings or complex interpolation.
- **Control Structures:** Prefer `for-of` loops. `for-in` loops should only be used on dict-style objects.
- **`this`:** Only use `this` in class constructors, methods, or in arrow functions defined within them.
- **Equality Checks:** Always use identity operators (`===` / `!==`).

## 5. Disallowed Features

- `with` keyword.
- `eval()` or `Function(...string)`.
- Automatic Semicolon Insertion.
- Modifying builtin objects (`Array.prototype.foo = ...`).

## 6. Naming

- **Classes:** `UpperCamelCase`.
- **Methods & Functions:** `lowerCamelCase`.
- **Constants:** `CONSTANT_CASE` (all uppercase with underscores).
- **Non-constant Fields & Variables:** `lowerCamelCase`.

## 7. JSDoc

- JSDoc is used on all classes, fields, and methods.
- Use `@param`, `@return`, `@override`, `@deprecated`.
- Type annotations are enclosed in braces (e.g., `/** @param {string} userName */`).

## 8. React & TypeScript Conventions

- **Component Files**: Use `PascalCase` (e.g., `AnalysisTable.tsx`, `AlertBox.tsx`).
- **Component Structure**:

  ```tsx
  interface Props {
  	data: ResultData;
  	warning: boolean;
  }

  export function MyComponent({ data, warning }: Props): JSX.Element {
  	// Implementation
  }
  ```

- **Hooks**: Use custom hooks for reusable logic. Prefix with `use` (e.g., `useInferenceStore`, `useFetchAnalysis`).
- **State Management**: Use Zustand for global state. Keep actions simple and testable.
- **Styling**: Use Tailwind CSS classes. Configure theme overrides in `tailwind.config.ts`.
- **Components**: Import Shadcn UI components from `@/components/ui/`.
- **No Inline Styles**: Always use CSS/Tailwind. No `style={{}}` props.

## 9. Vitest Testing Conventions

- **Test File Naming**: `<component>.test.tsx` or `<hook>.test.ts` in same directory.
- **Test Function Naming**: `test('should [behavior] when [condition]')`.
- **Rendering**: Use `render()` from `@testing-library/react`. Query with `getByRole`, `getByText`, etc.
- **Mocks**: Use `vi.mock()` for modules and API calls.
- **Assertions**:
  ```tsx
  expect(screen.getByRole('alert')).toBeInTheDocument();
  expect(screen.getByText('Warning:')).toHaveClass('text-red-600');
  ```
- **Coverage**: Run `npm run test:coverage`. Target >80%.

## 10. Playwright E2E Testing

- **Test File Naming**: `<feature>.spec.ts` (e.g., `analysis-flow.spec.ts`).
- **Page Objects**: Create reusable page object classes for UI interactions:
  ```ts
  class AnalysisPage {
  	constructor(private page: Page) {}

  	async enterText(text: string): Promise<void> {
  		await this.page.fill('[data-testid="text-input"]', text);
  	}

  	async clickAnalyze(): Promise<void> {
  		await this.page.click('button:has-text("Analyze")');
  	}
  }
  ```
- **Waits**: Always wait for elements, not arbitrary timeouts. Use `waitForSelector`, `waitForNavigation`.
- **Test Structure**: Arrange-Act-Assert (AAA) pattern.
- **Visual Tests**: Capture screenshots for alert styling verification:
  ```ts
  await expect(page).toHaveScreenshot('alert-warning.png');
  ```

## 11. Monorepo Import Conventions (Frontend)

- **Absolute Paths**: Use path alias configured in `tsconfig.json`:
  ```tsx
  import { useInferenceStore } from '@/stores/inference';
  import { AnalysisTable } from '@/components/AnalysisTable';
  ```
- **Never Use**: Relative paths with `../../../`. Always use `@/` alias.

## 12. Error Handling & User Feedback

- **Validation Errors**: Show inline errors under fields (e.g., "Text must be 1-2000 characters").
- **API Errors**: Display toast notifications with clear messages:
  - Timeout: "Connection timed out. Please try again."
  - 500 Error: "Server error. Please refresh and try again."
- **Loading States**: Show spinner or disable button while fetching.
- **No Console Errors**: Use error boundary component for React errors.

_Source: [Google JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html)_
