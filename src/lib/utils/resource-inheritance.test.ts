import { describe, expect, it } from 'vitest';

import {
	DEFAULT_RESOURCE_INHERITANCE,
	countSelectedResourceIds,
	getResourceInheritanceScope,
	getSelectedResourceIds,
	normalizeResourceInheritance,
	setResourceInheritanceScope,
	toggleSelectedResourceId
} from './resource-inheritance';

describe('resource inheritance state', () => {
	it('normalizes missing settings to inherit all admin resources', () => {
		expect(normalizeResourceInheritance()).toEqual(DEFAULT_RESOURCE_INHERITANCE);
	});

	it('switches admin models from all to specified and back to all', () => {
		const optionIds = ['admin.gpt', 'admin.claude'];
		let settings = normalizeResourceInheritance();

		expect(getResourceInheritanceScope(settings, 'admin_model_ids')).toBe('all');

		settings = setResourceInheritanceScope(settings, 'admin_model_ids', 'specified', optionIds);
		expect(getResourceInheritanceScope(settings, 'admin_model_ids')).toBe('specified');
		expect(getSelectedResourceIds(settings, 'admin_model_ids', optionIds)).toEqual(optionIds);

		settings = setResourceInheritanceScope(settings, 'admin_model_ids', 'all', optionIds);
		expect(getResourceInheritanceScope(settings, 'admin_model_ids')).toBe('all');
		expect(settings.admin_model_ids).toBeNull();
	});

	it('switches admin MCP servers independently from model scope', () => {
		const modelIds = ['admin.gpt'];
		const mcpIds = ['admin-1:0', 'admin-1:1'];
		let settings = normalizeResourceInheritance();

		settings = setResourceInheritanceScope(settings, 'admin_model_ids', 'specified', modelIds);
		settings = setResourceInheritanceScope(settings, 'admin_mcp_server_ids', 'specified', mcpIds);
		expect(getResourceInheritanceScope(settings, 'admin_model_ids')).toBe('specified');
		expect(getResourceInheritanceScope(settings, 'admin_mcp_server_ids')).toBe('specified');

		settings = setResourceInheritanceScope(settings, 'admin_mcp_server_ids', 'all', mcpIds);
		expect(getResourceInheritanceScope(settings, 'admin_model_ids')).toBe('specified');
		expect(getResourceInheritanceScope(settings, 'admin_mcp_server_ids')).toBe('all');
		expect(settings.admin_model_ids).toEqual(modelIds);
		expect(settings.admin_mcp_server_ids).toBeNull();
	});

	it('keeps specified mode when all individual MCP servers are unchecked', () => {
		const mcpIds = ['admin-1:0', 'admin-1:1'];
		let settings = normalizeResourceInheritance();

		settings = setResourceInheritanceScope(settings, 'admin_mcp_server_ids', 'specified', mcpIds);
		settings = toggleSelectedResourceId(settings, 'admin_mcp_server_ids', mcpIds, 'admin-1:0');
		settings = toggleSelectedResourceId(settings, 'admin_mcp_server_ids', mcpIds, 'admin-1:1');

		expect(getResourceInheritanceScope(settings, 'admin_mcp_server_ids')).toBe('specified');
		expect(getSelectedResourceIds(settings, 'admin_mcp_server_ids', mcpIds)).toEqual([]);
		expect(countSelectedResourceIds(settings, 'admin_mcp_server_ids', mcpIds)).toBe(0);
	});

	it('turns inherited-all model selection into a specified payload when one model is unchecked', () => {
		const modelIds = ['admin.gpt', 'admin.claude'];
		let settings = normalizeResourceInheritance();

		settings = toggleSelectedResourceId(settings, 'admin_model_ids', modelIds, 'admin.gpt');

		expect(getResourceInheritanceScope(settings, 'admin_model_ids')).toBe('specified');
		expect(settings.admin_model_ids).toEqual(['admin.claude']);
	});

	it('keeps specified payload empty when there are no options yet', () => {
		let settings = normalizeResourceInheritance();

		settings = setResourceInheritanceScope(settings, 'admin_mcp_server_ids', 'specified', []);

		expect(getResourceInheritanceScope(settings, 'admin_mcp_server_ids')).toBe('specified');
		expect(settings.admin_mcp_server_ids).toEqual([]);
	});
});
