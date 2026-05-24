export type ApiKeyPoolMode = 'round_robin' | 'random' | 'priority';

const normalizeApiKeyPoolEntry = (entry: any, index: number) => {
	const key = (typeof entry === 'string' ? entry : (entry?.key ?? '')).toString().trim();
	if (!key) return null;

	if (typeof entry === 'string') {
		return {
			id: `key-${index + 1}`,
			label: `Key ${index + 1}`,
			key,
			enabled: true
		};
	}

	return {
		...entry,
		id: (entry?.id ?? `key-${index + 1}`).toString(),
		label: (entry?.label ?? `Key ${index + 1}`).toString(),
		key,
		enabled: entry?.enabled !== false
	};
};

export const getApiKeyPoolRequestConfig = (pool: any) => {
	if (!pool || !Array.isArray(pool?.keys)) return undefined;

	const keys = pool.keys
		.map((entry: any, index: number) => normalizeApiKeyPoolEntry(entry, index))
		.filter(Boolean);

	if (!keys.length) return undefined;

	return {
		...pool,
		keys
	};
};

export const getPrimaryApiKeyFromPool = (pool: any) => {
	const requestPool = getApiKeyPoolRequestConfig(pool);
	const primary = requestPool?.keys?.find((entry: any) => entry?.enabled !== false);
	return (primary?.key ?? '').toString().trim();
};

export const getApiKeyForRequest = (legacyKey = '', pool: any = undefined) =>
	getPrimaryApiKeyFromPool(pool) || (legacyKey ?? '').toString().trim();

export const getApiKeyPoolSummary = (config: any, legacyKey = '') => {
	const pool = config?.api_key_pool ?? {};
	const keys = Array.isArray(pool?.keys)
		? pool.keys.filter((entry: any) => (entry?.key ?? '').toString().trim())
		: legacyKey
			? [{ enabled: true }]
			: [];
	const enabled = keys.filter((entry: any) => entry?.enabled !== false);
	const mode: ApiKeyPoolMode = ['round_robin', 'random', 'priority'].includes(pool?.mode)
		? pool.mode
		: 'round_robin';

	return {
		total: keys.length,
		enabled: enabled.length,
		mode,
		retry: pool?.retry?.enabled !== false
	};
};

export const getApiKeyPoolModeLabel = (mode: ApiKeyPoolMode, t: (key: string) => string) => {
	if (mode === 'random') return t('Random');
	if (mode === 'priority') return t('Priority');
	return t('Round Robin');
};
