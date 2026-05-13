export type ResourceInheritanceSelectionKey = 'admin_model_ids' | 'admin_mcp_server_ids';
export type ResourceInheritanceScope = 'all' | 'specified';

export type ResourceInheritanceSettings = {
	admin_models: boolean;
	admin_model_ids: string[] | null;
	admin_mcp_servers: boolean;
	admin_mcp_server_ids: string[] | null;
};

export const DEFAULT_RESOURCE_INHERITANCE: ResourceInheritanceSettings = {
	admin_models: true,
	admin_model_ids: null,
	admin_mcp_servers: true,
	admin_mcp_server_ids: null
};

export const normalizeResourceInheritance = (settings: any = {}): ResourceInheritanceSettings => ({
	...DEFAULT_RESOURCE_INHERITANCE,
	...(settings?.resource_inheritance ?? {})
});

export const getResourceInheritanceScope = (
	settings: ResourceInheritanceSettings,
	key: ResourceInheritanceSelectionKey
): ResourceInheritanceScope => (Array.isArray(settings[key]) ? 'specified' : 'all');

export const isAllResourceInherited = (
	settings: ResourceInheritanceSettings,
	key: ResourceInheritanceSelectionKey
) => getResourceInheritanceScope(settings, key) === 'all';

export const getSelectedResourceIds = (
	settings: ResourceInheritanceSettings,
	key: ResourceInheritanceSelectionKey,
	optionIds: string[]
) => {
	const value = settings[key];
	return Array.isArray(value) ? value : optionIds;
};

export const countSelectedResourceIds = (
	settings: ResourceInheritanceSettings,
	key: ResourceInheritanceSelectionKey,
	optionIds: string[]
) => {
	const optionSet = new Set(optionIds);
	return getSelectedResourceIds(settings, key, optionIds).filter((id) => optionSet.has(id)).length;
};

export const setResourceInheritanceScope = (
	settings: ResourceInheritanceSettings,
	key: ResourceInheritanceSelectionKey,
	scope: ResourceInheritanceScope,
	optionIds: string[] = []
): ResourceInheritanceSettings => {
	if (scope === 'all') {
		return {
			...settings,
			[key]: null
		};
	}

	const currentValue = settings[key];
	const nextValue = Array.isArray(currentValue)
		? currentValue.filter((id) => optionIds.length === 0 || optionIds.includes(id))
		: [...optionIds];

	return {
		...settings,
		[key]: nextValue
	};
};

export const toggleSelectedResourceId = (
	settings: ResourceInheritanceSettings,
	key: ResourceInheritanceSelectionKey,
	optionIds: string[],
	id: string
): ResourceInheritanceSettings => {
	const selected = new Set(getSelectedResourceIds(settings, key, optionIds));
	if (selected.has(id)) {
		selected.delete(id);
	} else {
		selected.add(id);
	}

	return {
		...settings,
		[key]: optionIds.filter((optionId) => selected.has(optionId))
	};
};
