import { describe, expect, it } from 'vitest';

import { hasEffectivePersistedSelectionState } from './composer-selection-state';

describe('composer selection state', () => {
	it('does not treat an untouched empty persisted selection as effective', () => {
		expect(hasEffectivePersistedSelectionState([], false)).toBe(false);
	});

	it('treats selected ids as effective even when the user has not manually touched the picker', () => {
		expect(hasEffectivePersistedSelectionState(['tool-a'], false)).toBe(true);
	});

	it('treats an explicitly touched empty selection as effective', () => {
		expect(hasEffectivePersistedSelectionState([], true)).toBe(true);
	});

	it('ignores missing and blank selection arrays unless touched', () => {
		expect(hasEffectivePersistedSelectionState(undefined, false)).toBe(false);
		expect(hasEffectivePersistedSelectionState(['', null, '  '], false)).toBe(false);
	});
});
