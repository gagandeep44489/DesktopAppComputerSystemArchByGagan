export interface Coach { id: string; name: string; title: string; bio: string; experienceYears: number; achievements: string[]; certifications: string[]; playingCareer: string; coachingCareer: string; imageUrl: string; }
export interface TrainingProgram { id: string; title: string; level: string; description: string; price: number; duration: string; highlights: string[]; }
export interface Testimonial { id: string; author: string; role: string; rating: number; quote: string; }
export interface GalleryItem { id: string; title: string; type: 'image' | 'video'; url: string; category: string; }
export interface BlogPost { id: string; title: string; category: string; excerpt: string; readMinutes: number; }
export interface BookingRequest { fullName: string; email: string; phone: string; programId: string; preferredDate: string; slot: string; message?: string; }
export interface BookingConfirmation { id: string; status: 'confirmed'; summary: string; }
