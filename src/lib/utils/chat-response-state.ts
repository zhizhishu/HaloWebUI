type ChatHistoryLike = {
	currentId?: string | null;
	messages?: Record<string, any>;
};

const isTerminalAssistantMessage = (message: any): boolean => {
	if (!message || message.role !== 'assistant') {
		return false;
	}

	return (
		message.done === true ||
		message.stopped === true ||
		message.stoppedByUser === true ||
		Boolean(message.error) ||
		Boolean(message.completedAt)
	);
};

const isActiveAssistantMessage = (message: any): boolean =>
	message?.role === 'assistant' && !isTerminalAssistantMessage(message);

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
		return isActiveAssistantMessage(currentMessage);
	}

	return (currentMessage.childrenIds ?? []).some((messageId: string) => {
		const childMessage = history?.messages?.[messageId];
		return isActiveAssistantMessage(childMessage);
	});
};
