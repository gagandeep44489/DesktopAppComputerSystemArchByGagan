import { createContext, useContext, type PropsWithChildren } from 'react';
import type { BlogRepository, BookingRepository, CoachRepository, GalleryRepository, ProgramRepository } from '@/domain/repositories/repositories';
import { BlogApi, BookingApi, CoachApi, GalleryApi, ProgramApi } from '@/infrastructure/api/apis';
import { BlogService, BookingService, CoachService, GalleryService, ProgramService } from '@/infrastructure/repositories/repositoryAdapters';
interface Dependencies { coachRepository: CoachRepository; programRepository: ProgramRepository; galleryRepository: GalleryRepository; blogRepository: BlogRepository; bookingRepository: BookingRepository; }
const dependencies: Dependencies = { coachRepository: new CoachService(new CoachApi()), programRepository: new ProgramService(new ProgramApi()), galleryRepository: new GalleryService(new GalleryApi()), blogRepository: new BlogService(new BlogApi()), bookingRepository: new BookingService(new BookingApi()) };
const DependencyContext = createContext<Dependencies | null>(null);
export function DependencyProvider({ children }: PropsWithChildren) { return <DependencyContext.Provider value={dependencies}>{children}</DependencyContext.Provider>; }
export function useDependencies(): Dependencies { const value = useContext(DependencyContext); if (!value) throw new Error('Dependencies unavailable'); return value; }
