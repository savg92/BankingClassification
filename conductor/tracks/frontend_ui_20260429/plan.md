# Implementation Plan: Frontend UI (Vite + Bun + Shadcn)

## Phase 1: Dashboard Foundation & Layout

- [x] Task: Initialize Project and Tabbed Navigation
  - [x] Write Vitest tests to verify tab switching and layout existence
  - [x] Setup initial Vite + React structure in `/apps/frontend`
  - [x] Implement the tabbed navigation system (e.g., using Shadcn Tabs)
  - [x] Verify tests pass
- [x] Task: Implement Instructional Guide and Input Area
  - [x] Write tests for the 3-step guide visibility and input button interaction
  - [x] Build the Top 3-step guide component
  - [x] Create the central text input area with the "Analyze" button
  - [x] Verify tests pass
- [x] **Task: Conductor - User Manual Verification 'Phase 1: Foundation'**
  - [x] Follow phase completion verification protocol in workflow.md
  - [x] Run dev server and verify dashboard renders without errors
  - [x] Manually verify tabbed navigation works
  - [x] Verify 3-step instructional guide is visible and clear

## Phase 2: State Management & API Integration

- [x] Task: Setup Zustand Store for Inference Data
  - [x] Write unit tests for the Zustand store (updating results, handling flags)
  - [x] Implement the `useInferenceStore` with actions for fetching and storing results
  - [x] Verify tests pass
- [x] Task: Integrate Backend API Service
  - [x] Write integration tests for API calls (mocking FastAPI responses)
  - [x] Implement the service layer to call POST `/analyze`
  - [x] Connect the "Analyze" button to the store and API
  - [x] Verify tests pass
- [x] **Task: Conductor - User Manual Verification 'Phase 2: Data Flow'**
  - [x] Follow phase completion verification protocol in workflow.md
  - [x] Verify Zustand store updates correctly when API returns results
  - [x] Test "Analyze" button triggers API call with entered text
  - [x] Verify loading state is shown while fetching results

## Phase 3: Result Visualization & Alerts

- [x] Task: Build Analysis Result Tables
  - [x] Write tests for data rendering in side-by-side tables
  - [x] Create the Shadcn Card components for Banking and Sentiment tables
  - [x] Implement the Top 5 list view with probabilities
  - [x] Verify tests pass
- [x] **Task: Conductor - User Manual Verification 'Phase 3: Visualization'**
  - [x] Follow phase completion verification protocol in workflow.md
  - [x] Verify top 5 tables render with correct data and probabilities
  - [x] Test alert renders only when warning flag is true
  - [x] Verify mandatory warning strings are displayed correctly
  - [x] Write tests for the destructive Alert visibility based on the `warning` flag
  - [x] Integrate the Shadcn Alert component with mandatory warning strings
  - [x] Verify tests pass
- [x] Task: Conductor - User Manual Verification 'Phase 3: Visualization' (Protocol in workflow.md)

## Phase 4: Branding, Styling & A11y

- [x] Task: Apply Banking Theme Overrides
  - [x] Write visual/CSS-aware tests for blue/white color presence
  - [x] Configure Tailwind theme overrides for the Banking professional look
  - [x] Verify tests pass
- [x] **Task: Conductor - User Manual Verification 'Phase 4: Styling & A11y'**
  - [x] Follow phase completion verification protocol in workflow.md
  - [x] Run accessibility scan (axe-core) and verify no critical issues
  - [x] Verify blue/white Banking theme is applied consistently
  - [x] Verify high contrast ratios (WCAG AA) for all text
  - [x] Write automated accessibility tests (using axe-core or similar)
  - [x] Refine contrast ratios and ARIA labels for tables and alerts
  - [x] Verify tests pass
- [x] Task: Conductor - User Manual Verification 'Phase 4: Styling & A11y' (Protocol in workflow.md)
