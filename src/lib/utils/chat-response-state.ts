type ChatHistoryLike = {
	currentId?: string | null;
	messages?: Record<string, any>;
};

export const hasActiveChatResponse = (
	history: ChatHistoryLike | null | undefined,
	taskIds: unknown
): boolean => {
	if (Array.isArray(taskIds) && taskIds.length > 0) {
		return true;
	}

	const currentId = history?.currentId;
	if (!currentId) {
		return false;
	}

	const currentMessage = history?.messages?.[currentId];
	if (!currentMessage) {
		return false;
	}

	if (currentMessage.role === 'assistant') {
		return currentMessage.done !== true;
	}

	return (currentMessage.childrenIds ?? []).some((messageId: string) => {
		const childMessage = history?.messages?.[messageId];
		return childMessage?.role === 'assistant' && childMessage.done !== true;
	});
};
