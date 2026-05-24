import { describe, expect, it } from 'vitest';

import {
	getApiKeyForRequest,
	getApiKeyPoolRequestConfig,
	getPrimaryApiKeyFromPool
} from './api-key-pool';

describe('api key pool request helpers', () => {
	it('uses the first enabled pool key when the legacy key is empty', () => {
		const pool = {
			keys: [
				{ id: 'a', label: 'A', key: '  sk-a  ', enabled: true },
				{ id: 'b', label: 'B', key: 'sk-b', enabled: true }
			],
			mode: 'round_robin'
		};

		expect(getApiKeyForRequest('', pool)).toBe('sk-a');
		expect(getPrimaryApiKeyFromPool(pool)).toBe('sk-a');
	});

	it('keeps disabled keys in the request config but does not use them as primary', () => {
		const pool = {
			keys: [
				{ id: 'a', label: 'A', key: 'sk-disabled', enabled: false },
				{ id: 'b', label: 'B', key: 'sk-enabled', enabled: true }
			]
		};

		expect(getApiKeyForRequest('', pool)).toBe('sk-enabled');
		expect(getApiKeyPoolRequestConfig(pool)?.keys).toEqual([
			{ id: 'a', label: 'A', key: 'sk-disabled', enabled: false },
			{ id: 'b', label: 'B', key: 'sk-enabled', enabled: true }
		]);
	});

	it('falls back to the legacy key when the pool has no usable key', () => {
		expect(
			getApiKeyForRequest(' sk-legacy ', {
				keys: [{ id: 'empty', label: 'Empty', key: ' ', enabled: true }]
			})
		).toBe('sk-legacy');
		expect(getApiKeyPoolRequestConfig({ keys: [{ key: ' ' }] })).toBeUndefined();
	});
});
