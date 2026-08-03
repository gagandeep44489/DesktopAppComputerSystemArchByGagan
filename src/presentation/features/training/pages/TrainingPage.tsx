import { Button, Card, CardActions, CardContent, Container, Grid, Typography } from '@mui/material';
import { Link } from 'react-router-dom';
import { SectionTitle } from '@/presentation/components/common/SectionTitle';
import { LoadingState } from '@/presentation/components/feedback/StateViews';
import { usePrograms } from '@/presentation/features/training/hooks';
export default function TrainingPage() { const { data, isLoading } = usePrograms(); if (isLoading) return <LoadingState />; return <Container sx={{ py: 6 }}><SectionTitle eyebrow="Training" title="Programs for every cricketer" /><Grid container spacing={3}>{data?.map((program) => <Grid key={program.id} size={{ xs: 12, sm: 6, md: 3 }}><Card sx={{ height: '100%' }}><CardContent><Typography variant="h5">{program.title}</Typography><Typography color="secondary">{program.level}</Typography><Typography sx={{ my: 2 }}>{program.description}</Typography><Typography variant="h6">${program.price}</Typography><Typography>{program.duration}</Typography></CardContent><CardActions><Button component={Link} to="/booking">Book now</Button></CardActions></Card></Grid>)}</Grid></Container>; }
