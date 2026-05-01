const steps = [
	{
		title: '1. Enter text',
		description: 'Paste a customer message or banking query into the analyzer.',
	},
	{
		title: '2. Analyze',
		description:
			'Send the request to the FastAPI service for intent and sentiment scoring.',
	},
	{
		title: '3. Review results',
		description:
			'Inspect the top 5 predictions and any low-confidence warning flags.',
	},
];

export function StepGuide() {
	return (
		<section
			className='guide'
			aria-label='Three-step guide'
		>
			{steps.map((step) => (
				<article
					key={step.title}
					className='guide-card'
				>
					<h2>{step.title}</h2>
					<p>{step.description}</p>
				</article>
			))}
		</section>
	);
}
