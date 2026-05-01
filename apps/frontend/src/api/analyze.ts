import type { AnalyzeResponse } from '../types';

const API_BASE_URL =
	import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

export async function analyzeText(text: string): Promise<AnalyzeResponse> {
	const response = await fetch(`${API_BASE_URL}/analyze`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ text }),
	});

	if (!response.ok) {
		const detail = await response.text();
		throw new Error(detail || 'Failed to analyze text');
	}

	return (await response.json()) as AnalyzeResponse;
}
