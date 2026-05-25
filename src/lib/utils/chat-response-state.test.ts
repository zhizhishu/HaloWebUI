import { describe, expect, it } from 'vitest';

import { hasActiveChatResponse } from './chat-response-state';

describe('chat response state', () => {
	it('does not treat a current user message as an active response', () => {
		const history = {
			currentId: 'user-1',
			messages: {
				'user-1': {
					id: 'user-1',
					role: 'user',
					childrenIds: []
				}
			}
		};

		expect(hasActiveChatResponse(history, null)).toBe(false);
	});

	it('treats unfinished assistant children as active responses', () => {
		const history = {
			currentId: 'user-1',
			messages: {
				'user-1': {
					id: 'user-1',
					role: 'user',
					childrenIds: ['assistant-1']
				},
				'assistant-1': {
					id: 'assistant-1',
					role: 'assistant',
					done: false
				}
			}
		};

		expect(hasActiveChatResponse(history, null)).toBe(true);
	});

	it('treats unfinished current assistant messages and task ids as active', () => {
		expect(
			hasActiveChatResponse(
				{
					currentId: 'assistant-1',
					messages: {
						'assistant-1': { id: 'assistant-1', role: 'assistant', done: false }
					}
				},
				null
			)
		).toBe(true);
		expect(hasActiveChatResponse({ currentId: null, messages: {} }, ['task-1'])).toBe(true);
	});

	it('ignores completed assistant responses', () => {
		expect(
			hasActiveChatResponse(
				{
					currentId: 'assistant-1',
					messages: {
						'assistant-1': { id: 'assistant-1', role: 'assistant', done: true }
					}
				},
				[]
			)
		).toBe(false);
	});
});
