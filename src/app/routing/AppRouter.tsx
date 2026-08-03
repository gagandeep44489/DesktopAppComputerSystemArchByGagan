import { lazy, Suspense } from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { LoadingState } from '@/presentation/components/feedback/StateViews';
import { MainLayout } from '@/presentation/layouts/MainLayout';
const HomePage = lazy(() => import('@/presentation/features/home/pages/HomePage'));
const CoachPage = lazy(() => import('@/presentation/features/coach/pages/CoachPage'));
const TrainingPage = lazy(() => import('@/presentation/features/training/pages/TrainingPage'));
const BookingPage = lazy(() => import('@/presentation/features/booking/pages/BookingPage'));
const GalleryPage = lazy(() => import('@/presentation/features/gallery/pages/GalleryPage'));
const TestimonialsPage = lazy(() => import('@/presentation/features/testimonials/pages/TestimonialsPage'));
const BlogPage = lazy(() => import('@/presentation/features/blog/pages/BlogPage'));
const FaqPage = lazy(() => import('@/presentation/features/faq/pages/FaqPage'));
const ContactPage = lazy(() => import('@/presentation/features/contact/pages/ContactPage'));
const NotFoundPage = lazy(() => import('@/presentation/features/not-found/pages/NotFoundPage'));
const router = createBrowserRouter([{ element: <MainLayout />, children: [{ path: '/', element: <HomePage /> }, { path: '/coach', element: <CoachPage /> }, { path: '/training', element: <TrainingPage /> }, { path: '/booking', element: <BookingPage /> }, { path: '/gallery', element: <GalleryPage /> }, { path: '/testimonials', element: <TestimonialsPage /> }, { path: '/blog', element: <BlogPage /> }, { path: '/faq', element: <FaqPage /> }, { path: '/contact', element: <ContactPage /> }, { path: '*', element: <NotFoundPage /> }] }]);
export function AppRouter() { return <Suspense fallback={<LoadingState />}><RouterProvider router={router} /></Suspense>; }
