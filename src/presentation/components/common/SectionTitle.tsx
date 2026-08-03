import { Box, Chip, Typography } from '@mui/material';
interface SectionTitleProps { eyebrow: string; title: string; subtitle?: string; }
export function SectionTitle({ eyebrow, title, subtitle }: SectionTitleProps) { return <Box sx={{ mb: 4, textAlign: 'center' }}><Chip color="secondary" label={eyebrow} sx={{ mb: 1 }} /><Typography component="h2" variant="h3">{title}</Typography>{subtitle ? <Typography color="text.secondary" sx={{ mx: 'auto', mt: 1, maxWidth: 720 }}>{subtitle}</Typography> : null}</Box>; }
