import { CssBaseline, ThemeProvider } from '@mui/material';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { type PropsWithChildren, useState } from 'react';
import { DependencyProvider } from '@/app/providers/dependencies';
import { theme } from '@/config/theme';
export function AppProviders({ children }: PropsWithChildren) { const [queryClient] = useState(() => new QueryClient()); return <QueryClientProvider client={queryClient}><DependencyProvider><ThemeProvider theme={theme}><CssBaseline />{children}</ThemeProvider></DependencyProvider></QueryClientProvider>; }
