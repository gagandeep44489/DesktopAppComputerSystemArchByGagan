import MenuIcon from '@mui/icons-material/Menu';
import SportsCricketIcon from '@mui/icons-material/SportsCricket';
import { AppBar, Box, Button, Container, Drawer, IconButton, Stack, Toolbar, Typography } from '@mui/material';
import { useState } from 'react';
import { Link, Outlet } from 'react-router-dom';
const nav = [['Home','/'],['Coach','/coach'],['Programs','/training'],['Booking','/booking'],['Gallery','/gallery'],['Testimonials','/testimonials'],['Blog','/blog'],['FAQ','/faq'],['Contact','/contact']] as const;
function NavLinks() { return <>{nav.map(([label, to]) => <Button key={to} color="inherit" component={Link} to={to}>{label}</Button>)}</>; }
export function MainLayout() { const [open, setOpen] = useState(false); return <><AppBar position="sticky"><Toolbar><SportsCricketIcon sx={{ mr: 1 }} /><Typography variant="h6" sx={{ flexGrow: 1 }}>Cricket Coach Pro</Typography><Box sx={{ display: { xs: 'none', md: 'block' } }}><NavLinks /></Box><IconButton aria-label="Open navigation" color="inherit" onClick={() => setOpen(true)} sx={{ display: { md: 'none' } }}><MenuIcon /></IconButton></Toolbar></AppBar><Drawer open={open} onClose={() => setOpen(false)}><Stack sx={{ p: 2, width: 240 }}><NavLinks /></Stack></Drawer><Outlet /><Box component="footer" sx={{ bgcolor: 'primary.main', color: 'white', mt: 8, py: 5 }}><Container><Typography variant="h6">Cricket Coach Pro</Typography><Typography>High-performance coaching for every stage of your cricket journey.</Typography></Container></Box></>; }
