import { Marked } from 'marked';
import { describe, expect, it } from 'vitest';

import markedExtension from './extension';

const createParser = () => {
	const parser = new Marked();
	parser.use(markedExtension());
	return parser;
};

describe('marked details extension', () => {
	it('tokenizes standard inline details blocks', () => {
		const [token] = createParser().lexer(
			'<details><summary>Audit: original blocked response</summary>Original content</details>'
		) as any[];

		expect(token).toMatchObject({
			type: 'details',
			summary: 'Audit: original blocked response',
			text: 'Original content'
		});
	});

	it('tokenizes details blocks when summary has attributes', () => {
		const [token] = createParser().lexer(
			[
				'<details type="tool_calls" done="true">',
				'<summary class="text-xs">Tool Executed</summary>',
				'',
				'{"ok":true}',
				'</details>'
			].join('\n')
		) as any[];

		expect(token).toMatchObject({
			type: 'details',
			summary: 'Tool Executed',
			text: '{"ok":true}',
			attributes: {
				type: 'tool_calls',
				done: 'true'
			}
		});
	});
});
