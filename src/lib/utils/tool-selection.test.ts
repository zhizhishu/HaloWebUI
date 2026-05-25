import { describe, expect, it } from 'vitest';

import { filterAvailableToolIds, normalizeToolIds } from './tool-selection';

describe('tool selection state', () => {
	it('normalizes persisted tool ids without duplicates', () => {
		expect(normalizeToolIds([' tool-a ', '', null, 'mcp:0', 'tool-a'])).toEqual([
			'tool-a',
			'mcp:0'
		]);
	});

	it('keeps persisted ids unchanged until the current tool list is loaded', () => {
		expect(filterAvailableToolIds(['tool-a', 'mcp:9'], null)).toEqual(['tool-a', 'mcp:9']);
	});

	it('drops deleted workspace and MCP tool ids after tools are loaded', () => {
		const tools = [{ id: 'tool-a' }, { id: 'mcp:0' }];

		expect(filterAvailableToolIds(['tool-a', 'mcp:9', 'deleted-tool', 'mcp:0'], tools)).toEqual([
			'tool-a',
			'mcp:0'
		]);
	});

	it('keeps stable local server tool ids after tools are loaded', () => {
		const tools = [{ id: 'tool-a' }, { id: 'mcp_id:admin-mcp-1' }, { id: 'server_id:openapi-1' }];

		expect(
			filterAvailableToolIds(
				['mcp_id:admin-mcp-1', 'server_id:openapi-1', 'mcp_id:missing'],
				tools
			)
		).toEqual(['mcp_id:admin-mcp-1', 'server_id:openapi-1']);
	});

	it('drops stale legacy local server indexes when stable ids are exposed', () => {
		const tools = [{ id: 'mcp_id:admin-mcp-1' }, { id: 'server_id:openapi-1' }];

		expect(filterAvailableToolIds(['mcp:0', 'server:0'], tools)).toEqual([]);
	});

	it('clears stale ids when the user currently has no available tools', () => {
		expect(filterAvailableToolIds(['mcp:0', 'tool-a'], [])).toEqual([]);
	});
});
