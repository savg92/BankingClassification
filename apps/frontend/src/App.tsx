import { useEffect } from 'react';
import { AnalysisTabPanel } from './components/AnalysisTabPanel';
import { PredictionCard } from './components/PredictionCard';
import { StepGuide } from './components/StepGuide';
import { useInferenceStore } from './store/useInferenceStore';
import './App.css';

export default function App() {
	const {
		activeTab,
		inputText,
		loading,
		result,
		history,
		setInputText,
		setActiveTab,
		submitAnalysis,
		hydrateHistory,
	} = useInferenceStore();

	useEffect(() => {
		hydrateHistory();
	}, [hydrateHistory]);

	const handleSubmit = async () => {
		await submitAnalysis();
	};

	return (
		<main className='app-shell'>
			<header className='app-header'>
				<h1>Banking Classification Dashboard</h1>
				<p>
					Dual-prediction intent and sentiment analysis with confidence
					warnings.
				</p>
			</header>

			<nav
				className='tabs'
				aria-label='Dashboard tabs'
			>
				<button
					type='button'
					className='tab-button'
					aria-selected={activeTab === 'analyze'}
					onClick={() => setActiveTab('analyze')}
				>
					Analyze
				</button>
				<button
					type='button'
					className='tab-button'
					aria-selected={activeTab === 'history'}
					onClick={() => setActiveTab('history')}
				>
					History
				</button>
			</nav>

			<div className='content'>
				<AnalysisTabPanel
					active={activeTab === 'analyze'}
					id='analyze-tab'
				>
					<StepGuide />

					<div className='analysis-grid'>
						<section
							className='panel input-area'
							aria-label='Text analyzer'
						>
							<h2>Analyze customer text</h2>
							<textarea
								value={inputText}
								onChange={(event) => setInputText(event.target.value)}
								placeholder='Type or paste a banking message here...'
								aria-label='Input text for analysis'
							/>
							<div className='input-actions'>
								<span className='metric'>{inputText.length} characters</span>
								<button
									type='button'
									className='primary-button'
									onClick={handleSubmit}
									disabled={loading}
									aria-label='Analyze text'
								>
									{loading ? 'Analyzing…' : 'Analyze'}
								</button>
							</div>
						</section>

						<section
							className='panel'
							aria-label='Prediction summary'
						>
							<h2>Live summary</h2>
							<p>
								Warning threshold: if the top prediction falls below 30%, the UI
								displays a destructive alert.
							</p>
							{result ? (
								<div className='history-item'>
									<strong>Last embedding size:</strong>{' '}
									{result.embedding.length}
								</div>
							) : (
								<p>No analysis submitted yet.</p>
							)}
						</section>
					</div>

					<div className='results-grid'>
						<PredictionCard
							title='Intent Top 5'
							model={result?.intent ?? null}
							warningLabel='Warning: I am not sure about this Intent!'
						/>
						<PredictionCard
							title='Sentiment Top 5'
							model={result?.sentiment ?? null}
							warningLabel='Warning: I am not sure about this Sentiment!'
						/>
					</div>
				</AnalysisTabPanel>

				<AnalysisTabPanel
					active={activeTab === 'history'}
					id='history-tab'
				>
					<section className='panel'>
						<h2>Recent analyses</h2>
						<div className='history-list'>
							{history.length ? (
								history.map((entry, index) => (
									<article
										className='history-item'
										key={`${index}-${entry.embedding.length}`}
									>
										<h3>Analysis #{index + 1}</h3>
										<p>
											Intent warning:{' '}
											<strong>{entry.intent.warning ? 'Yes' : 'No'}</strong> ·
											Sentiment warning:{' '}
											<strong>{entry.sentiment.warning ? 'Yes' : 'No'}</strong>
										</p>
										<p>Embedding length: {entry.embedding.length}</p>
									</article>
								))
							) : (
								<p>No cached results yet.</p>
							)}
						</div>
					</section>
				</AnalysisTabPanel>
			</div>
		</main>
	);
}
