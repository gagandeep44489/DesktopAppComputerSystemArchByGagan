import { useMutation, useQuery } from '@tanstack/react-query';
import { useDependencies } from '@/app/providers/dependencies';
import type { BookingRequest } from '@/domain/entities/models';
export function useCoach() { const { coachRepository } = useDependencies(); return useQuery({ queryKey: ['coach'], queryFn: () => coachRepository.getCoach() }); }
export function usePrograms() { const { programRepository } = useDependencies(); return useQuery({ queryKey: ['programs'], queryFn: () => programRepository.getPrograms() }); }
export function useGallery() { const { galleryRepository } = useDependencies(); return useQuery({ queryKey: ['gallery'], queryFn: () => galleryRepository.getGallery() }); }
export function useTestimonials() { const { coachRepository } = useDependencies(); return useQuery({ queryKey: ['testimonials'], queryFn: () => coachRepository.getTestimonials() }); }
export function useBlog() { const { blogRepository } = useDependencies(); return useQuery({ queryKey: ['blog'], queryFn: () => blogRepository.getPosts() }); }
export function useBooking() { const { bookingRepository } = useDependencies(); return useMutation({ mutationFn: (request: BookingRequest) => bookingRepository.createBooking(request) }); }
