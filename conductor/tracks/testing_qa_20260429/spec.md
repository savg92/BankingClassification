# Specification: Quality Assurance & Testing (testing_qa_20260429)

## Overview
This track focuses on the comprehensive verification of the "Dual-Prediction Hybrid Text Classification System". It ensures the backend correctly handles embedding-based inference and confidence flagging, while the frontend accurately renders alerts and visualizations based on that data.

## Functional Requirements
- **Backend Testing (Pytest)**:
    - Implement a mocking strategy using `pytest-mock` to intercept all `litellm.embedding` calls.
    - Verify the `/analyze` endpoint correctly sorts Top 5 probabilities for both Banking and Emotion models.
    - Validate the injection of the `warning: true` flag for Top 1 probabilities below 30%.
    - Test parallel inference execution to ensure no race conditions or deadlocks.
- **Frontend Testing (Vitest)**:
    - Verify that the side-by-side Shadcn Card components render the Top 5 results correctly from the Zustand store.
    - Confirm that the destructive Shadcn Alert is visible ONLY when the `warning: true` flag is present.
- **End-to-End Testing (Playwright)**:
    - **Vague Inputs**: Simulate a user entering highly ambiguous or extremely short sentences and assert the appearance of the warning alert.
    - **API Failure Modes**: Mock a 504 Gateway Timeout from the backend and verify the UI displays a graceful error message.
    - **Alert Visual Styling**: Assert that the warning alert uses the correct "destructive" variant and the mandatory warning string: "Warning: I am not sure about this [Intent/Sentiment]!".

## Non-Functional Requirements
- **Coverage Thresholds**: Ensure at least 80% code coverage for both the FastAPI backend and React frontend.
- **Concurrency Safety**: Confirm that simultaneous requests to the backend are handled safely.
- **Business Logic Accuracy**: Ensure the 30% threshold is applied consistently across all edge cases.

## Acceptance Criteria
- [ ] Backend test suite achieves >80% coverage with mocked LiteLLM calls.
- [ ] Frontend unit tests confirm conditional alert rendering logic.
- [ ] Playwright E2E tests successfully pass for "Vague Inputs" and "API Failure" scenarios.
- [ ] Visual verification of the mandatory warning strings in the UI.

## Out of Scope
- Training of new models (Phase 1).
- Feature enhancements to the dashboard (Phase 3).
- Deployment automation (Phase 5).
