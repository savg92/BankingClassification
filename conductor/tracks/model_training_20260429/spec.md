# Specification: Model Training and Artifact Generation (model_training_20260429)

## Overview
This track focuses on training two separate PyTorch neural networks to predict Banking Intent (using the Banking77 dataset) and User Sentiment (using the GoEmotions dataset). The models will utilize frozen embeddings generated via LiteLLM as their input features.

## Functional Requirements
- **Data Acquisition**: Fetch the Banking77 and GoEmotions datasets directly from Hugging Face.
- **Preprocessing**: 
    - Implement basic normalization (lowercasing, punctuation removal).
    - Normalize or remove emojis to ensure clean embedding extraction.
    - Truncate and pad all text inputs to a fixed sequence length of 128 tokens.
- **Embedding Extraction**: Use LiteLLM to generate 1D vector representations (e.g., 768-dim) for the text. Treat the LLM provider as a frozen base.
- **Hardware Agnostic Training**: Automatically detect and utilize available hardware (CPU, CUDA/GPU, or MPS for Apple Silicon).
- **Neural Architecture**:
    - Dual instances of a sequential model: GAP 1D -> Dense Hidden -> ReLU -> Dropout -> Dense Output (Softmax).
- **Training Logic**:
    - Perform a grid search for hyperparameters (Hidden Layer: 1024 vs 256; Dropout: 0.2 vs 0.3).
    - Use CrossEntropyLoss and Adam optimizer.
    - Implement Early Stopping based on validation loss to prevent overfitting.

## Non-Functional Requirements
- **Monitoring**: Track Accuracy, Loss, and Weighted F1-score for both training and validation sets.
- **Validation**: Strictly reserve 20% of data for validation.
- **Performance**: Ensure the training script is efficient enough to run on standard hardware within a reasonable timeframe.

## Acceptance Criteria
- [ ] Successful training of two PyTorch models (`banking_model.pth`, `emotion_model.pth`).
- [ ] Export of corresponding label maps (`banking_labels.json`, `emotion_labels.json`).
- [ ] Generation of Matplotlib charts showing Training/Validation Loss and Accuracy curves.
- [ ] A Markdown table summarizing the results of the hyperparameter grid search.

## Out of Scope
- Integration with the FastAPI backend (Phase 2).
- Implementation of the React dashboard (Phase 3).
- Real-time inference optimization.
