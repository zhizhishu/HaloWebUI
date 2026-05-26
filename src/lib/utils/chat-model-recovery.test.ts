import { describe, expect, it } from 'vitest';

import {
	getActiveAssistantMessagesByModelIndex,
	mergeRecoveredChatModelSelections,
	resolveAvailableChatModelSelectionValues,
	type ChatModelResolution
} from './chat-model-recovery';

const resolved = (value: string): ChatModelResolution => ({
	status: 'resolved',
	value,
	searchValue: value
});

describe('resolveAvailableChatModelSelectionValues', () => {
	it('drops stale persisted model ids instead of preserving unavailable selections', () => {
		const result = resolveAvailableChatModelSelectionValues(
			[
				{
					id: 'pipe_a.model_id_1',
					name: 'model_1',
					selection_id: 'modelref::pipe::function::id:pipe_a::model_id_1',
					model_id: 'model_id_1',
					model_ref: {
						provider: 'pipe',
						source: 'function',
						connection_id: 'pipe_a'
					}
				}
			],
			['modelref::pipe::function::id:old_pipe::model_id_1', 'pipe_a.model_id_1']
		);

		expect(result.values).toEqual(['modelref::pipe::function::id:pipe_a::model_id_1']);
		expect(result.droppedUnavailable).toBe(true);
		expect(result.resolutions.map((resolution) => resolution.status)).toEqual([
			'stale',
			'resolved'
		]);
	});

	it('recovers the model from the active assistant branch over stale chat metadata', () => {
		const selectedResolutions = [resolved('model-first')];
		const latestResolvedByIndex = new Map([[0, { resolution: resolved('model-latest'), timestamp: 20 }]]);
		const activeResolvedByIndex = new Map([[0, { resolution: resolved('model-active'), timestamp: 10 }]]);

		expect(
			mergeRecoveredChatModelSelections(
				selectedResolutions,
				latestResolvedByIndex,
				activeResolvedByIndex
			)
		).toEqual(['model-active']);
	});

	it('keeps persisted selections for inactive model slots', () => {
		const selectedResolutions = [resolved('model-a'), resolved('model-b')];
		const activeResolvedByIndex = new Map([[1, { resolution: resolved('model-c'), timestamp: 30 }]]);

		expect(
			mergeRecoveredChatModelSelections(selectedResolutions, new Map(), activeResolvedByIndex)
		).toEqual(['model-a', 'model-c']);
	});

	it('finds active assistant messages by walking the current branch', () => {
		const history = {
			currentId: 'assistant-active',
			messages: {
				'user-1': {
					id: 'user-1',
					role: 'user',
					parentId: null,
					childrenIds: ['assistant-first', 'assistant-active']
				},
				'assistant-first': {
					id: 'assistant-first',
					role: 'assistant',
					parentId: 'user-1',
					model: 'model-first',
					modelIdx: 0
				},
				'assistant-active': {
					id: 'assistant-active',
					role: 'assistant',
					parentId: 'user-1',
					model: 'model-active',
					modelIdx: 0
				}
			}
		};

		expect(
			Array.from(getActiveAssistantMessagesByModelIndex(history).entries()).map(
				([modelIdx, message]) => [modelIdx, message.model]
			)
		).toEqual([[0, 'model-active']]);
	});
});
