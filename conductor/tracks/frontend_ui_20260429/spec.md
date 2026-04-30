# Specification: Frontend UI (Vite + Bun + Shadcn)

## Overview
This track involves developing the interactive React dashboard for the "Dual-Prediction Hybrid Text Classification System". The dashboard will allow users to input text and visualize real-time predictions for Banking Intent and User Sentiment, with a strong focus on uncertainty management and accessibility.

## Functional Requirements
- **Dashboard Layout**: 
  - Implement a **Tabbed Layout** to organize different analysis views and instructional content.
  - Top section: A clear 3-step instructional guide for users.
  - Middle section: Large text input area with an explicit **"Analyze"** button.
- **Data Visualization**:
  - Side-by-side **Shadcn Card** components containing tables for the Top 5 Banking Intents and Top 5 Sentiments.
  - Each table must display the category and its associated probability.
- **Uncertainty Handling**:
  - Conditionally render a **destructive Shadcn Alert** above each table if the `warning: true` flag is present in the API response.
  - Alert String: "Warning: I am not sure about this [Intent/Sentiment]!"
- **State Management**: Use **Zustand** for efficient, lightweight state management of inference results and UI transitions.
- **Styling & Branding**:
  - Follow **Shadcn Defaults** for component structure.
  - Apply **Banking Theme Overrides** (Blue/White color palette) as per product guidelines.
  - Ensure **High Contrast (A11y)** for all text and data visualizations.

## Non-Functional Requirements
- **Responsive Design**: The dashboard must be fully functional and aesthetically pleasing on both desktop and mobile devices.
- **Performance**: UI updates and transition animations should be fluid and low-latency.
- **Input Validation**: Handle empty or excessively long text inputs gracefully.

## Acceptance Criteria
- [ ] React dashboard successfully connects to the FastAPI backend.
- [ ] Tabbed navigation functions correctly.
- [ ] "Analyze" button triggers the full dual-prediction flow.
- [ ] Side-by-side tables display accurate Top 5 results.
- [ ] Destructive alerts render correctly when confidence is < 30%.
- [ ] UI follows the Banking Blue/White theme with high contrast.

## Out of Scope
- Backend inference logic (Phase 2).
- Model training or artifact generation (Phase 1).
- Long-term data persistence or history views.
