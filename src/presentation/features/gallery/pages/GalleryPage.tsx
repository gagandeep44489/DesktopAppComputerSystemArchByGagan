import PlayCircleIcon from '@mui/icons-material/PlayCircle';
import { Card, CardContent, CardMedia, Container, Grid, Typography } from '@mui/material';
import { SectionTitle } from '@/presentation/components/common/SectionTitle';
import { LoadingState } from '@/presentation/components/feedback/StateViews';
import { useGallery } from '@/presentation/features/gallery/hooks';
export default function GalleryPage() { const { data, isLoading } = useGallery(); if (isLoading) return <LoadingState />; return <Container sx={{ py: 6 }}><SectionTitle eyebrow="Gallery" title="Images, videos, and match highlights" /><Grid container spacing={3}>{data?.map((item) => <Grid key={item.id} size={{ xs: 12, sm: 6, md: 4 }}><Card><CardMedia component="img" image={item.url} alt={item.title} height="220" /><CardContent><Typography variant="h6">{item.type === 'video' ? <PlayCircleIcon fontSize="small" /> : null} {item.title}</Typography><Typography color="text.secondary">{item.category}</Typography></CardContent></Card></Grid>)}</Grid></Container>; }
