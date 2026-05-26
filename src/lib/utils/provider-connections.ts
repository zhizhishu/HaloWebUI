export type IndexedProviderConnections<TConfig = any> = {
	urls: string[];
	keys?: string[];
	configs?: Record<string | number, TConfig> | null;
};

export type RemoveIndexedProviderConnectionResult<TConfig = any> = IndexedProviderConnections<TConfig> & {
	removed: boolean;
};

export const submitProviderConnectionEdit = async <TConnection>(
	previous: TConnection,
	next: TConnection,
	apply: (connection: TConnection) => void,
	save: (connection: TConnection) => void | Promise<void>
) => {
	apply(next);

	try {
		await save(next);
	} catch (error) {
		apply(previous);
		throw error;
	}
};

export const cloneIndexedProviderConnections = <TConfig = any>(
	connections: IndexedProviderConnections<TConfig>
): IndexedProviderConnections<TConfig> => ({
	urls: [...(connections.urls ?? [])],
	keys: connections.keys ? [...connections.keys] : undefined,
	configs: { ...(connections.configs ?? {}) }
});

export const removeIndexedProviderConnection = <TConfig = any>(
	connections: IndexedProviderConnections<TConfig>,
	index: number,
	expectedUrl?: string
): RemoveIndexedProviderConnectionResult<TConfig> => {
	const urls = [...(connections.urls ?? [])];
	const keys = connections.keys ? [...connections.keys] : undefined;
	const configs = connections.configs ?? {};

	if (index < 0 || index >= urls.length) {
		return {
			urls,
			keys,
			configs: { ...configs },
			removed: false
		};
	}

	if (expectedUrl !== undefined && urls[index] !== expectedUrl) {
		return {
			urls,
			keys,
			configs: { ...configs },
			removed: false
		};
	}

	const nextUrls = urls.filter((_, urlIdx) => urlIdx !== index);
	const nextKeys = keys?.filter((_, keyIdx) => keyIdx !== index);
	const nextConfigs: Record<number, TConfig> = {};

	nextUrls.forEach((_, nextIdx) => {
		const sourceIdx = nextIdx < index ? nextIdx : nextIdx + 1;
		if (Object.prototype.hasOwnProperty.call(configs, sourceIdx)) {
			nextConfigs[nextIdx] = configs[sourceIdx];
		}
	});

	return {
		urls: nextUrls,
		keys: nextKeys,
		configs: nextConfigs,
		removed: true
	};
};
