import { AppProviders } from '@/app/providers/AppProviders';
import { AppRouter } from '@/app/routing/AppRouter';
import { ErrorBoundary } from '@/presentation/components/feedback/ErrorBoundary';
export function App() { return <ErrorBoundary><AppProviders><AppRouter /></AppProviders></ErrorBoundary>; }
