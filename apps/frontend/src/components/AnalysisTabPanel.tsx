import type { ReactNode } from 'react';

interface AnalysisTabPanelProps {
	active: boolean;
	children: ReactNode;
	id: string;
}

export function AnalysisTabPanel({
	active,
	children,
	id,
}: AnalysisTabPanelProps) {
	if (!active) {
		return null;
	}

	return (
		<section
			id={id}
			className='panel'
			aria-live='polite'
		>
			{children}
		</section>
	);
}
