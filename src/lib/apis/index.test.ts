import { afterEach, describe, expect, it, vi } from 'vitest';

import { getBackendConfig } from './index';

const stubLocalStorage = (token = '') => {
	const storage = {
		token,
		clear: vi.fn(() => {
			storage.token = '';
		})
	};
	vi.stubGlobal('localStorage', storage);
	return storage;
};

describe('backend config api', () => {
	afterEach(() => {
		vi.restoreAllMocks();
		vi.unstubAllGlobals();
	});

	it('uses the stored token when refreshing config without an explicit token', async () => {
		stubLocalStorage('stored-token');
		const fetchMock = vi.fn(async () => new Response(JSON.stringify({ status: true })));
		vi.stubGlobal('fetch', fetchMock);

		await expect(getBackendConfig()).resolves.toEqual({ status: true });

		expect(fetchMock).toHaveBeenCalledTimes(1);
		expect(fetchMock.mock.calls[0][1]?.headers).toMatchObject({
			authorization: 'Bearer stored-token'
		});
	});

	it('lets callers explicitly request public config with an empty token', async () => {
		stubLocalStorage('stored-token');
		const fetchMock = vi.fn(async () => new Response(JSON.stringify({ status: true })));
		vi.stubGlobal('fetch', fetchMock);

		await expect(getBackendConfig('')).resolves.toEqual({ status: true });

		expect(fetchMock.mock.calls[0][1]?.headers).not.toHaveProperty('authorization');
	});
});
