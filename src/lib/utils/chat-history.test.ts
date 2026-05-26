import { describe, expect, it } from 'vitest';

import { createMessagesList } from './index';

describe('createMessagesList', () => {
	it('returns an empty list when the current message is missing', () => {
		expect(
			createMessagesList(
				{
					currentId: 'missing',
					messages: {
						'user-1': { id: 'user-1', parentId: null, childrenIds: [] }
					}
				},
				'missing'
			)
		).toEqual([]);
	});

	it('keeps the reachable message when its parent link is broken', () => {
		const orphanedChild = { id: 'assistant-1', parentId: 'missing-parent', childrenIds: [] };

		expect(
			createMessagesList(
				{
					currentId: 'assistant-1',
					messages: {
						'assistant-1': orphanedChild
					}
				},
				'assistant-1'
			)
		).toEqual([orphanedChild]);
	});

	it('stops at cycles instead of recursing forever', () => {
		const userMessage = { id: 'user-1', parentId: 'assistant-1', childrenIds: ['assistant-1'] };
		const assistantMessage = { id: 'assistant-1', parentId: 'user-1', childrenIds: ['user-1'] };

		expect(
			createMessagesList(
				{
					currentId: 'assistant-1',
					messages: {
						'user-1': userMessage,
						'assistant-1': assistantMessage
					}
				},
				'assistant-1'
			)
		).toEqual([userMessage, assistantMessage]);
	});
});
