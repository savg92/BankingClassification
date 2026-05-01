# Implementation Plan: Frontend UI (Vite + Bun + Shadcn)

## Phase 1: Dashboard Foundation & Layout

- [ ] Task: Initialize Project and Tabbed Navigation
  - [ ] Write Vitest tests to verify tab switching and layout existence
  - [ ] Setup initial Vite + React structure in `/apps/frontend`
  - [ ] Implement the tabbed navigation system (e.g., using Shadcn Tabs)
  - [ ] Verify tests pass
- [ ] Task: Implement Instructional Guide and Input Area
  - [ ] Write tests for the 3-step guide visibility and input button interaction
  - [ ] Build the Top 3-step guide component
  - [ ] Create the central text input area with the "Analyze" button
  - [ ] Verify tests pass
- [ ] **Task: Conductor - User Manual Verification 'Phase 1: Foundation'**
  - [ ] Follow phase completion verification protocol in workflow.md
  - [ ] Run dev server and verify dashboard renders without errors
  - [ ] Manually verify tabbed navigation works
  - [ ] Verify 3-step instructional guide is visible and clear

## Phase 2: State Management & API Integration

- [ ] Task: Setup Zustand Store for Inference Data
  - [ ] Write unit tests for the Zustand store (updating results, handling flags)
  - [ ] Implement the `useInferenceStore` with actions for fetching and storing results
  - [ ] Verify tests pass
- [ ] Task: Integrate Backend API Service
  - [ ] Write integration tests for API calls (mocking FastAPI responses)
  - [ ] Implement the service layer to call POST `/analyze`
  - [ ] Connect the "Analyze" button to the store and API
  - [ ] Verify tests pass
- [ ] **Task: Conductor - User Manual Verification 'Phase 2: Data Flow'**
  - [ ] Follow phase completion verification protocol in workflow.md
  - [ ] Verify Zustand store updates correctly when API returns results
  - [ ] Test "Analyze" button triggers API call with entered text
  - [ ] Verify loading state is shown while fetching results

## Phase 3: Result Visualization & Alerts

- [ ] Task: Build Analysis Result Tables
  - [ ] Write tests for data rendering in side-by-side tables
  - [ ] Create the Shadcn Card components for Banking and Sentiment tables
  - [ ] Implement the Top 5 list view with probabilities
  - [ ] Verify tests pass
- [ ] **Task: Conductor - User Manual Verification 'Phase 3: Visualization'**
  - [ ] Follow phase completion verification protocol in workflow.md
  - [ ] Verify top 5 tables render with correct data and probabilities
  - [ ] Test alert renders only when warning flag is true
  - [ ] Verify mandatory warning strings are displayed correctly
  - [ ] Write tests for the destructive Alert visibility based on the `warning` flag
  - [ ] Integrate the Shadcn Alert component with mandatory warning strings
  - [ ] Verify tests pass
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Visualization' (Protocol in workflow.md)

## Phase 4: Branding, Styling & A11y

- [ ] Task: Apply Banking Theme Overrides
  - [ ] Write visual/CSS-aware tests for blue/white color presence
  - [ ] Configure Tailwind theme overrides for the Banking professional look
  - [ ] Verify tests pass
- [ ] **Task: Conductor - User Manual Verification 'Phase 4: Styling & A11y'**
  - [ ] Follow phase completion verification protocol in workflow.md
  - [ ] Run accessibility scan (axe-core) and verify no critical issues
  - [ ] Verify blue/white Banking theme is applied consistently
  - [ ] Verify high contrast ratios (WCAG AA) for all text
  - [ ] Write automated accessibility tests (using axe-core or similar)
  - [ ] Refine contrast ratios and ARIA labels for tables and alerts
  - [ ] Verify tests pass
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Styling & A11y' (Protocol in workflow.md)
