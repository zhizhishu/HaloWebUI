import { afterEach, describe, expect, it, vi } from 'vitest';

import { importSkillFromRemoteZipUrl, importSkillFromZip } from './index';

describe('skills api', () => {
	afterEach(() => {
		vi.restoreAllMocks();
		vi.unstubAllGlobals();
	});

	it('adds fallback identifier when uploading catalog ZIP packages', async () => {
		const fetchMock = vi.fn(async () => new Response(JSON.stringify({ status: 'created' })));
		vi.stubGlobal('fetch', fetchMock);

		await importSkillFromZip(
			'token',
			new File(['skill'], 'anthropics-skills-pdf.zip', { type: 'application/zip' }),
			{ fallbackIdentifier: 'anthropics-skills-pdf' }
		);

		const body = fetchMock.mock.calls[0][1]?.body as FormData;
		expect(body.get('fallback_identifier')).toBe('anthropics-skills-pdf');
		expect((body.get('file') as File).name).toBe('anthropics-skills-pdf.zip');
	});

	it('passes fallback identifier through remote ZIP imports', async () => {
		const fetchMock = vi
			.fn()
			.mockResolvedValueOnce(new Response(new Blob(['skill archive'], { type: 'application/zip' })))
			.mockResolvedValueOnce(new Response(JSON.stringify({ status: 'created' })));
		vi.stubGlobal('fetch', fetchMock);

		await importSkillFromRemoteZipUrl(
			'token',
			'https://market.lobehub.com/api/v1/skills/anthropics-skills-pdf/download',
			'anthropics-skills-pdf.zip',
			{ fallbackIdentifier: 'anthropics-skills-pdf' }
		);

		const body = fetchMock.mock.calls[1][1]?.body as FormData;
		expect(body.get('fallback_identifier')).toBe('anthropics-skills-pdf');
		expect((body.get('file') as File).name).toBe('anthropics-skills-pdf.zip');
	});
});
