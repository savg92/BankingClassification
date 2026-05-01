export interface PredictionItem {
	label: string;
	probability: number;
}

export interface ModelResponse {
	top_5: PredictionItem[];
	warning: boolean;
}

export interface AnalyzeResponse {
	embedding: number[];
	intent: ModelResponse;
	sentiment: ModelResponse;
}

export type AnalysisTab = 'analyze' | 'history';
