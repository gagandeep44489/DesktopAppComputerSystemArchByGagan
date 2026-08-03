import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { SectionTitle } from '@/presentation/components/common/SectionTitle';
describe('SectionTitle', () => { it('renders title and subtitle', () => { render(<SectionTitle eyebrow="Test" title="Elite Coaching" subtitle="Train well" />); expect(screen.getByRole('heading', { name: 'Elite Coaching' })).toBeInTheDocument(); expect(screen.getByText('Train well')).toBeInTheDocument(); }); });
