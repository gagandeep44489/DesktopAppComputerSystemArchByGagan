import type { BlogRepository, BookingRepository, CoachRepository, GalleryRepository, ProgramRepository } from '@/domain/repositories/repositories';
import type { BookingRequest } from '@/domain/entities/models';
import { BlogApi, BookingApi, CoachApi, GalleryApi, ProgramApi } from '@/infrastructure/api/apis';
export class CoachService implements CoachRepository { constructor(private readonly api: CoachApi) {} getCoach() { return this.api.getCoach(); } getTestimonials() { return this.api.getTestimonials(); } }
export class ProgramService implements ProgramRepository { constructor(private readonly api: ProgramApi) {} getPrograms() { return this.api.getPrograms(); } }
export class GalleryService implements GalleryRepository { constructor(private readonly api: GalleryApi) {} getGallery() { return this.api.getGallery(); } }
export class BlogService implements BlogRepository { constructor(private readonly api: BlogApi) {} getPosts() { return this.api.getPosts(); } }
export class BookingService implements BookingRepository { constructor(private readonly api: BookingApi) {} createBooking(request: BookingRequest) { return this.api.createBooking(request); } }
