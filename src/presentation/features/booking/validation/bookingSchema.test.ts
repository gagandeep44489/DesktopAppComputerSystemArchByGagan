import { describe, expect, it } from 'vitest';
import { bookingSchema } from '@/presentation/features/booking/validation/bookingSchema';
describe('bookingSchema', () => { it('accepts valid booking data', () => { const result = bookingSchema.safeParse({ fullName: 'Alex Player', email: 'alex@example.com', phone: '5551234567', programId: 'program-1', preferredDate: '2026-08-10', slot: '09:00 AM' }); expect(result.success).toBe(true); }); });
