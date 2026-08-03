import type { BookingConfirmation, BookingRequest } from '@/domain/entities/models';
import { coach, gallery, posts, programs, testimonials } from '@/infrastructure/api/mockData';
const wait = async () => new Promise((resolve) => setTimeout(resolve, 20));
export class CoachApi { async getCoach() { await wait(); return coach; } async getTestimonials() { await wait(); return testimonials; } }
export class BookingApi { async createBooking(request: BookingRequest): Promise<BookingConfirmation> { await wait(); return { id: crypto.randomUUID(), status: 'confirmed', summary: `Session booked for ${request.fullName} on ${request.preferredDate}` }; } }
export class BlogApi { async getPosts() { await wait(); return posts; } }
export class GalleryApi { async getGallery() { await wait(); return gallery; } }
export class ProgramApi { async getPrograms() { await wait(); return programs; } }
