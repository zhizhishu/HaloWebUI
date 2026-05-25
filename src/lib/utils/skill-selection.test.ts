import { describe, expect, it } from 'vitest';

import { filterAvailableSkillIds, normalizeSkillIds } from './skill-selection';

describe('skill selection state', () => {
	it('normalizes persisted skill ids without duplicates', () => {
		expect(normalizeSkillIds([' skill-a ', '', null, 'skill-b', 'skill-a'])).toEqual([
			'skill-a',
			'skill-b'
		]);
	});

	it('keeps persisted ids unchanged until the current skill list is loaded', () => {
		expect(filterAvailableSkillIds(['skill-a', 'deleted-skill'], null)).toEqual([
			'skill-a',
			'deleted-skill'
		]);
	});

	it('drops deleted skill ids after skills are loaded', () => {
		const skills = [{ id: 'skill-a' }, { id: 'skill-b' }];

		expect(filterAvailableSkillIds(['skill-a', 'deleted-skill', 'skill-b'], skills)).toEqual([
			'skill-a',
			'skill-b'
		]);
	});

	it('clears stale ids when the user currently has no visible skills', () => {
		expect(filterAvailableSkillIds(['skill-a', 'deleted-skill'], [])).toEqual([]);
	});
});
