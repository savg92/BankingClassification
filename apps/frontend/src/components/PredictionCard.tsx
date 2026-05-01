import type { ModelResponse } from '../types';

interface PredictionCardProps {
	title: string;
	model: ModelResponse | null;
	warningLabel: string;
}

export function PredictionCard({
	title,
	model,
	warningLabel,
}: PredictionCardProps) {
	return (
		<article className='result-card'>
			<h2>{title}</h2>
			{model?.warning ? (
				<div
					className='alert danger'
					role='alert'
				>
					{warningLabel}
				</div>
			) : null}
			<table className='prediction-table'>
				<thead>
					<tr>
						<th>Category</th>
						<th>Probability</th>
					</tr>
				</thead>
				<tbody>
					{model?.top_5.length ? (
						model.top_5.map((item) => (
							<tr key={`${title}-${item.label}`}>
								<td>{item.label}</td>
								<td>{(item.probability * 100).toFixed(1)}%</td>
							</tr>
						))
					) : (
						<tr>
							<td colSpan={2}>No predictions yet.</td>
						</tr>
					)}
				</tbody>
			</table>
		</article>
	);
}
