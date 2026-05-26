// Helper function to find matching closing tag
function findMatchingClosingTag(src: string): number {
	const tagRegex = /<\/?details\b[^>]*>/gi;
	let depth = 0;
	let match: RegExpExecArray | null;

	while ((match = tagRegex.exec(src)) !== null) {
		if (match[0].startsWith('</')) {
			depth--;
			if (depth === 0) {
				return tagRegex.lastIndex;
			}
		} else {
			depth++;
		}
	}

	return -1;
}

// Function to parse attributes from tag
function parseAttributes(tag: string): { [key: string]: string } {
	const attributes: { [key: string]: string } = {};
	const attrRegex = /([\w:-]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?/g;
	let match;
	while ((match = attrRegex.exec(tag)) !== null) {
		attributes[match[1]] = match[2] ?? match[3] ?? match[4] ?? 'true';
	}
	return attributes;
}

function detailsTokenizer(src: string) {
	const detailsRegex = /^<details\b([^>]*)>/i;
	const summaryRegex = /^<summary\b[^>]*>([\s\S]*?)<\/summary>\s*/i;

	const detailsMatch = detailsRegex.exec(src);
	if (detailsMatch) {
		const endIndex = findMatchingClosingTag(src);
		if (endIndex === -1) return;

		const fullMatch = src.slice(0, endIndex);
		const detailsTag = detailsMatch[0];
		const attributes = parseAttributes(detailsMatch[1] ?? '');

		let content = fullMatch.slice(detailsTag.length, -10).trim(); // Remove <details> and </details>
		let summary = '';

		const summaryMatch = summaryRegex.exec(content);
		if (summaryMatch) {
			summary = summaryMatch[1].trim();
			content = content.slice(summaryMatch[0].length).trim();
		}

		return {
			type: 'details',
			raw: fullMatch,
			summary: summary,
			text: content,
			attributes: attributes // Include extracted attributes from <details>
		};
	}
}

function detailsStart(src: string) {
	// Support `<details>` and `<details ...>`; this is a "fast path" for marked.
	return src.match(/^<details\b/i) ? 0 : -1;
}

function detailsRenderer(token: any) {
	const attributesString = token.attributes
		? Object.entries(token.attributes)
				.map(([key, value]) => `${key}="${value}"`)
				.join(' ')
		: '';

	return `<details${attributesString ? ` ${attributesString}` : ''}>
  ${token.summary ? `<summary>${token.summary}</summary>` : ''}
  ${token.text}
  </details>`;
}

// Extension wrapper function
function detailsExtension(_options?: any) {
	return {
		name: 'details',
		level: 'block',
		start: detailsStart,
		tokenizer: detailsTokenizer,
		renderer: detailsRenderer
	};
}

export default function (options = {}) {
	return {
		extensions: [detailsExtension(options)]
	};
}
