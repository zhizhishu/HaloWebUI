import { describe, expect, it } from 'vitest';

import {
	isKnownInlineHtmlFormatFragment,
	renderResponseHtmlFormat
} from './response-html-format';

describe('response-html-format', () => {
	it('renders markdown-like content as a Halo inline HTML fragment', () => {
		const html = renderResponseHtmlFormat('# Report\n\nSummary text\n\n- one\n- two');

		expect(html).toContain('data-halo-response-html-format="inline"');
		expect(html).toContain('Report');
		expect(html).toContain('Summary text');
		expect(html).toContain('<li');
	});

	it('escapes raw html from model output', () => {
		const html = renderResponseHtmlFormat('Hello <script>alert(1)</script>');

		expect(html).toContain('&lt;script&gt;alert(1)&lt;/script&gt;');
		expect(html).not.toContain('<script>');
	});

	it('does not emit unsafe markdown link hrefs', () => {
		const html = renderResponseHtmlFormat(
			'[bad](javascript:alert(1)) [ok](https://example.com)'
		);

		expect(html).not.toContain('href="javascript:');
		expect(html).toContain('href="https://example.com"');
	});

	it('removes internal reasoning details before rendering HTML cards', () => {
		const html = renderResponseHtmlFormat(`
<details type="reasoning" done="true" duration="0.8">
<summary>Thought for 0.8 seconds</summary>
This internal reasoning should not be visible.
</details>

# 北极熊为什么不吃企鹅？

北极熊和企鹅生活在不同地区。
`);

		expect(html).not.toContain('&lt;details');
		expect(html).not.toContain('Thought for 0.8 seconds');
		expect(html).not.toContain('internal reasoning');
		expect(html).toContain('北极熊为什么不吃企鹅？');
		expect(html).toContain('北极熊和企鹅生活在不同地区。');
	});

	it('keeps reasoning details when they are shown inside code fences', () => {
		const html = renderResponseHtmlFormat(`
# Example

\`\`\`html
<details type="reasoning">
<summary>Example only</summary>
</details>
\`\`\`
`);

		expect(html).toContain('&lt;details type=&quot;reasoning&quot;&gt;');
		expect(html).toContain('Example only');
	});

	it('passes through known inline html fragments for downstream sanitization', () => {
		const fragment = '<div data-html-render-mcp="inline"><b>Ready</b></div>';

		expect(isKnownInlineHtmlFormatFragment(fragment)).toBe(true);
		expect(renderResponseHtmlFormat(fragment)).toBe(fragment);
	});
});
