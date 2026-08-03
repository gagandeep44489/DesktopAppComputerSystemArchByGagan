import { Alert, Button, Container } from '@mui/material';
import { Component, type ErrorInfo, type ReactNode } from 'react';
interface Props { children: ReactNode; }
interface State { hasError: boolean; }
export class ErrorBoundary extends Component<Props, State> { state: State = { hasError: false }; static getDerivedStateFromError() { return { hasError: true }; } componentDidCatch(error: Error, info: ErrorInfo) { console.error(error, info); } render() { if (this.state.hasError) return <Container sx={{ py: 8 }}><Alert severity="error" action={<Button onClick={() => location.reload()}>Reload</Button>}>Unexpected application error.</Alert></Container>; return this.props.children; } }
