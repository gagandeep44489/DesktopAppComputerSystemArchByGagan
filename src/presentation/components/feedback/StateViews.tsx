import { Alert, Box, CircularProgress, Skeleton } from '@mui/material';
export function LoadingState() { return <Box sx={{ display: 'grid', placeItems: 'center', py: 8 }}><CircularProgress aria-label="Loading content" /></Box>; }
export function ErrorState() { return <Alert severity="error">Something went wrong. Please try again.</Alert>; }
export function CardSkeleton() { return <Skeleton variant="rounded" height={180} />; }
