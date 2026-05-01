import { create } from 'zustand';
import type { AnalyzeResponse, AnalysisTab } from '../types';
import { analyzeText } from '../api/analyze';

interface InferenceState {
	activeTab: AnalysisTab;
	inputText: string;
	loading: boolean;
	result: AnalyzeResponse | null;
	history: AnalyzeResponse[];
	setInputText: (value: string) => void;
	setActiveTab: (value: AnalysisTab) => void;
	submitAnalysis: () => Promise<void>;
	hydrateHistory: () => void;
}

const HISTORY_KEY = 'banking-classification-history';

function persistHistory(history: AnalyzeResponse[]) {
	localStorage.setItem(HISTORY_KEY, JSON.stringify(history.slice(0, 100)));
}

export const useInferenceStore = create<InferenceState>((set, get) => ({
	activeTab: 'analyze',
	inputText: '',
	loading: false,
	result: null,
	history: [],
	setInputText: (value) => set({ inputText: value }),
	setActiveTab: (value) => set({ activeTab: value }),
	hydrateHistory: () => {
		const raw = localStorage.getItem(HISTORY_KEY);
		if (!raw) {
			return;
		}
		try {
			const parsed = JSON.parse(raw) as AnalyzeResponse[];
			set({ history: parsed });
		} catch {
			set({ history: [] });
		}
	},
	submitAnalysis: async () => {
		const { inputText, history } = get();
		const trimmed = inputText.trim();
		if (!trimmed) {
			throw new Error('Please enter text to analyze.');
		}
		set({ loading: true });
		try {
			const result = await analyzeText(trimmed);
			const nextHistory = [result, ...history].slice(0, 100);
			set({
				result,
				history: nextHistory,
				loading: false,
				activeTab: 'analyze',
			});
			persistHistory(nextHistory);
		} catch (error) {
			set({ loading: false });
			throw error;
		}
	},
}));
