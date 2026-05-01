import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';

vi.mock('./api/analyze', () => ({
	analyzeText: vi.fn(async () => ({
		embedding: Array.from({ length: 768 }, () => 0.1),
		intent: {
			warning: false,
			top_5: [
				{ label: 'cash_withdrawal', probability: 0.52 },
				{ label: 'check_balance', probability: 0.22 },
			],
		},
		sentiment: {
			warning: true,
			top_5: [
				{ label: 'sadness', probability: 0.11 },
				{ label: 'neutral', probability: 0.09 },
			],
		},
	})),
}));

test('switches tabs and surfaces the warning state', async () => {
	const user = userEvent.setup();
	render(<App />);

	await user.click(screen.getByRole('button', { name: 'History' }));
	expect(
		screen.getByRole('heading', { name: 'Recent analyses' }),
	).toBeInTheDocument();

	await user.click(screen.getByRole('button', { name: 'Analyze' }));
	await user.type(
		screen.getByLabelText('Input text for analysis'),
		'Need to cancel a wire transfer',
	);
	await user.click(screen.getByRole('button', { name: 'Analyze text' }));

	expect(
		await screen.findByText('Warning: I am not sure about this Sentiment!'),
	).toBeInTheDocument();
});
