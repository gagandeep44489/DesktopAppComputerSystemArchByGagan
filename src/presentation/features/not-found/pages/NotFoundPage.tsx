import { Button, Container, Typography } from '@mui/material';
import { Link } from 'react-router-dom';
export default function NotFoundPage() { return <Container sx={{ py: 10, textAlign: 'center' }}><Typography variant="h1">404</Typography><Typography variant="h5" sx={{ mb: 3 }}>This page is outside the boundary rope.</Typography><Button component={Link} to="/" variant="contained">Back home</Button></Container>; }
