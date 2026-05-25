import { describe, expect, it } from 'vitest';
import {
	cloneIndexedProviderConnections,
	removeIndexedProviderConnection
} from './provider-connections';

describe('provider connection helpers', () => {
	it('removes one keyed provider connection and reindexes configs', () => {
		const result = removeIndexedProviderConnection(
			{
				urls: ['https://a.example/v1', 'https://b.example/v1', 'https://c.example/v1'],
				keys: ['key-a', 'key-b', 'key-c'],
				configs: {
					0: { name: 'a' },
					1: { name: 'b' },
					2: { name: 'c' }
				}
			},
			1,
			'https://b.example/v1'
		);

		expect(result).toEqual({
			urls: ['https://a.example/v1', 'https://c.example/v1'],
			keys: ['key-a', 'key-c'],
			configs: {
				0: { name: 'a' },
				1: { name: 'c' }
			},
			removed: true
		});
	});

	it('removes one keyless provider connection and reindexes configs', () => {
		const result = removeIndexedProviderConnection(
			{
				urls: ['http://localhost:11434', 'http://host.docker.internal:11434'],
				configs: {
					0: { enable: true },
					1: { enable: false }
				}
			},
			0,
			'http://localhost:11434'
		);

		expect(result).toEqual({
			urls: ['http://host.docker.internal:11434'],
			keys: undefined,
			configs: {
				0: { enable: false }
			},
			removed: true
		});
	});

	it('does not mutate or misalign state when the rendered url is stale', () => {
		const state = {
			urls: ['https://a.example/v1', 'https://b.example/v1'],
			keys: ['key-a', 'key-b'],
			configs: {
				0: { name: 'a' },
				1: { name: 'b' }
			}
		};

		const result = removeIndexedProviderConnection(state, 0, 'https://old.example/v1');

		expect(result).toEqual({
			...state,
			configs: {
				0: { name: 'a' },
				1: { name: 'b' }
			},
			removed: false
		});
		expect(state.urls).toEqual(['https://a.example/v1', 'https://b.example/v1']);
		expect(state.keys).toEqual(['key-a', 'key-b']);
	});

	it('clones arrays and configs for rollback snapshots', () => {
		const state = {
			urls: ['https://a.example/v1'],
			keys: ['key-a'],
			configs: {
				0: { name: 'a' }
			}
		};
		const snapshot = cloneIndexedProviderConnections(state);

		state.urls.push('https://b.example/v1');
		state.keys.push('key-b');
		state.configs[1] = { name: 'b' };

		expect(snapshot).toEqual({
			urls: ['https://a.example/v1'],
			keys: ['key-a'],
			configs: {
				0: { name: 'a' }
			}
		});
	});
});
