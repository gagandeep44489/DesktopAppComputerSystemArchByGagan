import StarIcon from '@mui/icons-material/Star';
import { Card, CardContent, Container, Grid, Rating, Typography } from '@mui/material';
import { SectionTitle } from '@/presentation/components/common/SectionTitle';
import { useTestimonials } from '@/presentation/features/testimonials/hooks';
export default function TestimonialsPage() { const { data } = useTestimonials(); return <Container sx={{ py: 6 }}><SectionTitle eyebrow="Testimonials" title="Player reviews, parent reviews, and success stories" /><Grid container spacing={3}>{data?.map((item) => <Grid key={item.id} size={{ xs: 12, md: 4 }}><Card><CardContent><Rating value={item.rating} readOnly icon={<StarIcon />} /><Typography sx={{ my: 2 }}>“{item.quote}”</Typography><Typography variant="h6">{item.author}</Typography><Typography color="text.secondary">{item.role}</Typography></CardContent></Card></Grid>)}</Grid></Container>; }
