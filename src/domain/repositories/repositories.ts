import type { BlogPost, BookingConfirmation, BookingRequest, Coach, GalleryItem, Testimonial, TrainingProgram } from '@/domain/entities/models';
export interface CoachRepository { getCoach(): Promise<Coach>; getTestimonials(): Promise<Testimonial[]>; }
export interface ProgramRepository { getPrograms(): Promise<TrainingProgram[]>; }
export interface GalleryRepository { getGallery(): Promise<GalleryItem[]>; }
export interface BlogRepository { getPosts(): Promise<BlogPost[]>; }
export interface BookingRepository { createBooking(request: BookingRequest): Promise<BookingConfirmation>; }
