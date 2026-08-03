import { describe, expect, it } from 'vitest';
import { CoachApi } from '@/infrastructure/api/apis';
import { CoachService } from '@/infrastructure/repositories/repositoryAdapters';
describe('CoachService', () => { it('loads coach through api abstraction', async () => { const service = new CoachService(new CoachApi()); await expect(service.getCoach()).resolves.toMatchObject({ name: 'Gagan Sharma' }); }); });
