type ToolLike = {
	id?: unknown;
};

export const normalizeToolIds = (ids: unknown): string[] => {
	if (!Array.isArray(ids)) {
		return [];
	}

	const seen = new Set<string>();
	const normalized: string[] = [];

	for (const rawId of ids) {
		const id = String(rawId ?? '').trim();
		if (!id || seen.has(id)) {
			continue;
		}

		seen.add(id);
		normalized.push(id);
	}

	return normalized;
};

export const filterAvailableToolIds = (ids: unknown, tools: ToolLike[] | null | undefined) => {
	const normalized = normalizeToolIds(ids);
	if (!Array.isArray(tools)) {
		return normalized;
	}

	const availableIds = new Set(
		tools.map((tool) => String(tool?.id ?? '').trim()).filter((id) => id)
	);
	return normalized.filter((id) => availableIds.has(id));
};
