type SkillLike = {
	id?: unknown;
};

export const normalizeSkillIds = (ids: unknown): string[] => {
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

export const filterAvailableSkillIds = (
	ids: unknown,
	skills: SkillLike[] | null | undefined
) => {
	const normalized = normalizeSkillIds(ids);
	if (!Array.isArray(skills)) {
		return normalized;
	}

	const availableIds = new Set(
		skills.map((skill) => String(skill?.id ?? '').trim()).filter((id) => id)
	);
	return normalized.filter((id) => availableIds.has(id));
};
