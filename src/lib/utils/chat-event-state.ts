export const getLatestEventMessage = <TMessage>(
	history: { messages?: Record<string, TMessage> } | null | undefined,
	messageId: string | null | undefined,
	fallbackMessage: TMessage
): TMessage => {
	if (!messageId) {
		return fallbackMessage;
	}

	return history?.messages?.[messageId] ?? fallbackMessage;
};
