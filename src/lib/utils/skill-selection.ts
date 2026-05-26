type SkillLike = {
	id?: unknown;
};

const SKILL_TAG_PATTERN = /<\$([\w.\-:/]+)(?:\|[^>]+)?>/g;
const SKILL_TAG_WITH_TRAILING_SPACE_PATTERN = /<\$([\w.\-:/]+)(?:\|[^>]+)?>\s*/g;

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

export const extractSkillIdsFromText = (text: unknown): string[] => {
	const matches = [...String(text ?? '').matchAll(SKILL_TAG_PATTERN)];
	return Array.from(
		new Set(matches.map((match) => String(match?.[1] ?? '').trim()).filter(Boolean))
	);
};

export const stripSkillTagsFromText = (text: unknown): string =>
	String(text ?? '').replace(SKILL_TAG_WITH_TRAILING_SPACE_PATTERN, '').trim();

export const normalizeSkillMessageTextForRequest = (
	text: unknown,
	{
		ensureNonEmptySkillMention = false,
		placeholder = '.'
	}: {
		ensureNonEmptySkillMention?: boolean;
		placeholder?: string;
	} = {}
): string => {
	const stripped = stripSkillTagsFromText(text);
	if (stripped || !ensureNonEmptySkillMention) {
		return stripped;
	}

	return extractSkillIdsFromText(text).length > 0 ? placeholder : stripped;
};
