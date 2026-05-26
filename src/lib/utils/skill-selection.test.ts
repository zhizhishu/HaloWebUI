import { describe, expect, it } from 'vitest';

import {
	extractSkillIdsFromText,
	filterAvailableSkillIds,
	normalizeSkillIds,
	normalizeSkillMessageTextForRequest,
	stripSkillTagsFromText
} from './skill-selection';

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

	it('extracts skill mentions from chat text', () => {
		expect(
			extractSkillIdsFromText('<$skill-a|Data Skill> analyze <$skill-b|Writer>')
		).toEqual(['skill-a', 'skill-b']);
	});

	it('strips skill mentions before sending text to the model', () => {
		expect(stripSkillTagsFromText('<$skill-a|Data Skill> analyze this')).toBe('analyze this');
		expect(stripSkillTagsFromText('Use <$skill-a|Data Skill> now')).toBe('Use now');
	});

	it('keeps skill-only user messages non-empty after stripping mentions', () => {
		expect(
			normalizeSkillMessageTextForRequest('<$skill-a|Data Skill> ', {
				ensureNonEmptySkillMention: true
			})
		).toBe('.');
	});

	it('does not add placeholders for ordinary blank messages', () => {
		expect(
			normalizeSkillMessageTextForRequest('   ', {
				ensureNonEmptySkillMention: true
			})
		).toBe('');
	});

	it('does not add placeholders when skill-only text is not a user message', () => {
		expect(
			normalizeSkillMessageTextForRequest('<$skill-a|Data Skill> ', {
				ensureNonEmptySkillMention: false
			})
		).toBe('');
	});
});
