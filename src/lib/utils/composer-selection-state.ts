export const hasEffectivePersistedSelectionState = (ids: unknown, touched: unknown) => {
	if (Boolean(touched)) {
		return true;
	}

	if (!Array.isArray(ids)) {
		return false;
	}

	return ids.some((id) => String(id ?? '').trim() !== '');
};
