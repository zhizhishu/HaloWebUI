import { describe, expect, it } from 'vitest';
import { getLatestEventMessage } from './chat-event-state';

describe('getLatestEventMessage', () => {
	it('keeps a message updated by an async event handler instead of restoring a stale reference', () => {
		const history = {
			messages: {
				'assistant-1': {
					id: 'assistant-1',
					content: 'streamed content',
					done: true
				}
			}
		};
		const staleMessage = history.messages['assistant-1'];

		history.messages['assistant-1'] = {
			...staleMessage,
			content: 'FILTER_REPLACED: final assistant response was blocked'
		};

		expect(getLatestEventMessage(history, 'assistant-1', staleMessage)).toEqual(
			history.messages['assistant-1']
		);
	});

	it('falls back to the event message when the history entry is missing', () => {
		const fallbackMessage = {
			id: 'assistant-1',
			content: 'streamed content'
		};

		expect(getLatestEventMessage({ messages: {} }, 'assistant-1', fallbackMessage)).toBe(
			fallbackMessage
		);
	});
});
