import { z } from 'zod';
export const bookingSchema = z.object({ fullName: z.string().min(2, 'Enter your full name'), email: z.email('Enter a valid email'), phone: z.string().min(10, 'Enter a valid phone number'), programId: z.string().min(1, 'Choose a training program'), preferredDate: z.string().min(1, 'Choose a preferred date'), slot: z.string().min(1, 'Choose a slot'), message: z.string().max(500).optional() });
export type BookingFormValues = z.infer<typeof bookingSchema>;
