import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';

vi.mock('./api/analyze', () => ({
	analyzeText: vi.fn(async () => ({
		embedding: Array.from({ length: 768 }, (_, index) => index / 768),
		intent: {
			warning: true,
			top_5: [
				{ label: 'transfer_funds', probability: 0.18 },
				{ label: 'check_balance', probability: 0.16 },
			],
		},
		sentiment: {
			warning: false,
			top_5: [
				{ label: 'neutral', probability: 0.61 },
				{ label: 'joy', probability: 0.13 },
			],
		},
	})),
}));

test('renders dashboard tabs and instructional guide', () => {
	render(<App />);

	expect(
		screen.getByRole('heading', { name: 'Banking Classification Dashboard' }),
	).toBeInTheDocument();
	expect(screen.getByRole('button', { name: 'Analyze' })).toBeInTheDocument();
	expect(screen.getByText('1. Enter text')).toBeInTheDocument();
});

test('submits text and renders warning alert', async () => {
	const user = userEvent.setup();
	render(<App />);

	await user.type(
		screen.getByLabelText('Input text for analysis'),
		'Please investigate a suspicious card payment',
	);
	await user.click(screen.getByRole('button', { name: 'Analyze text' }));

	expect(
		await screen.findByText('Warning: I am not sure about this Intent!'),
	).toBeInTheDocument();
	expect(screen.getByText('transfer_funds')).toBeInTheDocument();
});
