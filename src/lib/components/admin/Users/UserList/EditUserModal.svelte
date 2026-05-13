<script lang="ts">
	import { toast } from 'svelte-sonner';
	import dayjs from 'dayjs';
	import { createEventDispatcher } from 'svelte';
	import { getContext, onMount } from 'svelte';
	import type { Writable } from 'svelte/store';
	import type { i18n as i18nType } from 'i18next';

	import {
		getResourceInheritanceOptions,
		updateUserById,
		type ResourceInheritanceOption,
		type ResourceInheritanceOptions
	} from '$lib/apis/users';
	import { WEBUI_BASE_URL } from '$lib/constants';

	import Modal from '$lib/components/common/Modal.svelte';
	import LetterAvatar from '$lib/components/common/LetterAvatar.svelte';
	import Switch from '$lib/components/common/Switch.svelte';
	import localizedFormat from 'dayjs/plugin/localizedFormat';

	const i18n = getContext('i18n') as Writable<i18nType>;
	const dispatch = createEventDispatcher();
	dayjs.extend(localizedFormat);

	export let show = false;
	export let selectedUser;
	export let sessionUser;

	let _user: any = {
		id: '',
		profile_image_url: '',
		name: '',
		email: '',
		password: '',
		note: '',
		settings: {
			resource_inheritance: {
				admin_models: true,
				admin_model_ids: null,
				admin_mcp_servers: true,
				admin_mcp_server_ids: null
			}
		}
	};

	const DEFAULT_RESOURCE_INHERITANCE = {
		admin_models: true,
		admin_model_ids: null,
		admin_mcp_servers: true,
		admin_mcp_server_ids: null
	};

	const getResourceInheritance = (settings: any = {}) => ({
		...DEFAULT_RESOURCE_INHERITANCE,
		...(settings?.resource_inheritance ?? {})
	});

	let inheritanceOptions: ResourceInheritanceOptions = {
		admin_models: [],
		admin_mcp_servers: []
	};
	let inheritanceOptionsLoading = false;
	let inheritanceOptionsLoaded = false;
	type ResourceSelectionKey = 'admin_model_ids' | 'admin_mcp_server_ids';
	type ResourceInheritanceKey = ResourceSelectionKey | 'admin_models' | 'admin_mcp_servers';
	const pendingSelectCurrentOnLoad = new Set<ResourceSelectionKey>();

	const getOptionsForKey = (
		key: ResourceSelectionKey,
		options: ResourceInheritanceOptions = inheritanceOptions
	) => (key === 'admin_model_ids' ? options.admin_models : options.admin_mcp_servers);

	const setResourceInheritanceValue = (key: ResourceInheritanceKey, value: any) => {
		_user = {
			..._user,
			settings: {
				..._user.settings,
				resource_inheritance: {
					..._user.settings.resource_inheritance,
					[key]: value
				}
			}
		};
	};

	const loadInheritanceOptions = async () => {
		if (selectedUser?.role === 'admin' || inheritanceOptionsLoading) {
			return;
		}

		inheritanceOptionsLoading = true;
		const res = await getResourceInheritanceOptions(localStorage.token).catch((error) => {
			toast.error(`${error}`);
			return null;
		});
		if (res) {
			const nextOptions = {
				admin_models: res.admin_models ?? [],
				admin_mcp_servers: res.admin_mcp_servers ?? []
			};
			inheritanceOptions = nextOptions;
			inheritanceOptionsLoaded = true;

			for (const key of Array.from(pendingSelectCurrentOnLoad)) {
				const selectedValue = _user.settings.resource_inheritance[key];
				if (Array.isArray(selectedValue) && selectedValue.length === 0) {
					const ids = getOptionsForKey(key, nextOptions).map((option) => option.id);
					if (ids.length > 0) {
						setResourceInheritanceValue(key, ids);
					}
				}
				pendingSelectCurrentOnLoad.delete(key);
			}
		}
		inheritanceOptionsLoading = false;
	};

	const isAllInherited = (key: ResourceSelectionKey) =>
		_user.settings.resource_inheritance[key] === null ||
		_user.settings.resource_inheritance[key] === undefined;

	const getSelectedResourceIds = (
		key: ResourceSelectionKey,
		options: ResourceInheritanceOption[]
	) => {
		const value = _user.settings.resource_inheritance[key];
		if (Array.isArray(value)) {
			return value;
		}
		return options.map((option) => option.id);
	};

	const setAllInherited = (
		key: ResourceSelectionKey,
		all: boolean,
		options: ResourceInheritanceOption[]
	) => {
		if (all) {
			pendingSelectCurrentOnLoad.delete(key);
			setResourceInheritanceValue(key, null);
			return;
		}

		if (!inheritanceOptionsLoaded && options.length === 0) {
			pendingSelectCurrentOnLoad.add(key);
			void loadInheritanceOptions();
		}
		setResourceInheritanceValue(key, options.length > 0 ? options.map((option) => option.id) : []);
	};

	const toggleInheritedResource = (
		key: ResourceSelectionKey,
		options: ResourceInheritanceOption[],
		id: string
	) => {
		const selected = new Set(getSelectedResourceIds(key, options));
		if (selected.has(id)) {
			selected.delete(id);
		} else {
			selected.add(id);
		}
		setResourceInheritanceValue(
			key,
			options.map((option) => option.id).filter((optionId) => selected.has(optionId))
		);
	};

	const getSelectedResourceCount = (
		key: ResourceSelectionKey,
		options: ResourceInheritanceOption[]
	) =>
		getSelectedResourceIds(key, options).filter((id) => options.some((option) => option.id === id))
			.length;

	const getScopeButtonClasses = (active: boolean) =>
		`inline-flex min-w-[4.5rem] items-center justify-center rounded-lg px-3 py-1.5 text-center text-xs font-medium transition ${
			active
				? 'bg-white text-gray-900 shadow-sm dark:bg-gray-700 dark:text-gray-50'
				: 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
		}`;

	const createEditableUser = (user: any) => ({
		id: user?.id ?? '',
		profile_image_url: user?.profile_image_url ?? '',
		name: user?.name ?? '',
		email: user?.email ?? '',
		password: '',
		note: user?.note ?? '',
		settings: {
			resource_inheritance: getResourceInheritance(user?.settings)
		}
	});

	const hasCustomAvatar = (url: string) =>
		url &&
		(url.startsWith(WEBUI_BASE_URL) ||
			url.startsWith('https://www.gravatar.com/avatar/') ||
			url.startsWith('data:'));

	const getRoleClasses = (role: string) => {
		switch (role) {
			case 'admin':
				return 'border-blue-200 bg-blue-50 text-blue-700 dark:border-blue-900/50 dark:bg-blue-950/30 dark:text-blue-300';
			case 'user':
				return 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-900/50 dark:bg-emerald-950/30 dark:text-emerald-300';
			default:
				return 'border-gray-200 bg-gray-100 text-gray-700 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200';
		}
	};

	const submitHandler = async () => {
		const payload = selectedUser?.role === 'admin' ? { ..._user, settings: undefined } : _user;

		const res = await updateUserById(localStorage.token, selectedUser.id, payload).catch(
			(error) => {
				toast.error(`${error}`);
			}
		);

		if (res) {
			dispatch('save');
			show = false;
		}
	};

	onMount(() => {
		if (selectedUser) {
			_user = createEditableUser(selectedUser);
		}
		loadInheritanceOptions();
	});
</script>

<Modal size="sm" bind:show>
	<div class="max-h-[85vh] overflow-y-auto">
		<!-- Header -->
		<div class="flex items-center justify-between px-5 pt-5 pb-3">
			<div class="text-base font-semibold text-gray-800 dark:text-gray-100">
				{$i18n.t('Edit User')}
			</div>
			<button
				class="rounded-lg p-1.5 text-gray-400 transition hover:bg-gray-100 hover:text-gray-600 dark:hover:bg-gray-800 dark:hover:text-gray-200"
				on:click={() => {
					show = false;
				}}
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 20 20"
					fill="currentColor"
					class="size-5"
				>
					<path
						d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
					/>
				</svg>
			</button>
		</div>

		<!-- User Card Header -->
		<div class="mx-5 mb-4 glass-item p-4">
			<div class="flex items-center gap-4">
				{#if hasCustomAvatar(selectedUser?.profile_image_url)}
					<img
						src={selectedUser.profile_image_url}
						class="size-14 rounded-2xl object-cover ring-1 ring-black/5 dark:ring-white/10"
						alt="User profile"
					/>
				{:else}
					<LetterAvatar
						name={selectedUser?.name ?? ''}
						size="size-14"
						className="rounded-2xl"
						textClass="text-xl"
					/>
				{/if}

				<div class="min-w-0 flex-1">
					<div class="flex items-center gap-2.5">
						<span class="truncate text-sm font-semibold text-gray-800 dark:text-gray-100"
							>{selectedUser?.name}</span
						>
						<span
							class={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-[11px] font-semibold ${getRoleClasses(selectedUser?.role)}`}
						>
							<span class="size-1.5 rounded-full bg-current opacity-80" />
							{$i18n.t(selectedUser?.role)}
						</span>
					</div>
					<div class="mt-1 truncate text-xs text-gray-400 dark:text-gray-500">
						{selectedUser?.email}
					</div>
					<div class="mt-0.5 text-[11px] text-gray-400 dark:text-gray-500">
						{$i18n.t('Created at')}
						{dayjs(selectedUser?.created_at * 1000).format('LL')}
					</div>
				</div>
			</div>
		</div>

		<!-- Form -->
		<form class="px-5 pb-5" on:submit|preventDefault={submitHandler}>
			<div class="space-y-3">
				<div class="glass-item p-4">
					<div class="text-xs font-medium text-gray-500 dark:text-gray-400 mb-1.5">
						{$i18n.t('Email')}
					</div>
					<input
						class="w-full py-2 px-3 text-sm dark:text-gray-300 glass-input disabled:text-gray-400 dark:disabled:text-gray-500 disabled:cursor-not-allowed"
						type="email"
						bind:value={_user.email}
						autocomplete="off"
						required
						disabled={_user.id == sessionUser.id}
					/>
				</div>

				<div class="glass-item p-4">
					<div class="text-xs font-medium text-gray-500 dark:text-gray-400 mb-1.5">
						{$i18n.t('Name')}
					</div>
					<input
						class="w-full py-2 px-3 text-sm dark:text-gray-300 glass-input"
						type="text"
						bind:value={_user.name}
						autocomplete="off"
						required
					/>
				</div>

				<div class="glass-item p-4">
					<div class="text-xs font-medium text-gray-500 dark:text-gray-400 mb-1.5">
						{$i18n.t('New Password')}
					</div>
					<input
						class="w-full py-2 px-3 text-sm dark:text-gray-300 glass-input"
						type="password"
						bind:value={_user.password}
						autocomplete="new-password"
						placeholder={$i18n.t('Leave empty to keep current')}
					/>
				</div>

				<div class="glass-item p-4">
					<div class="text-xs font-medium text-gray-500 dark:text-gray-400 mb-1.5">
						{$i18n.t('Admin Note')}
					</div>
					<textarea
						class="w-full py-2 px-3 text-sm dark:text-gray-300 glass-input resize-y"
						bind:value={_user.note}
						rows="3"
						placeholder={$i18n.t('Internal note visible only to admins')}
					/>
				</div>

				{#if selectedUser?.role !== 'admin'}
					<div class="glass-item p-4 space-y-3">
						<div>
							<div class="text-xs font-medium text-gray-500 dark:text-gray-400">
								{$i18n.t('Resource Inheritance')}
							</div>
							<div class="mt-1 text-xs text-gray-400 dark:text-gray-500">
								{$i18n.t('Control whether this user can inherit admin-managed resources.')}
							</div>
						</div>

						<div class="flex items-start justify-between gap-4">
							<div>
								<div class="text-sm font-medium text-gray-700 dark:text-gray-200">
									{$i18n.t('Inherit Admin Models')}
								</div>
								<div class="mt-1 text-xs text-gray-400 dark:text-gray-500">
									{$i18n.t('Allow this user to use models configured by admins.')}
								</div>
							</div>
							<Switch
								state={_user.settings.resource_inheritance.admin_models}
								on:change={(event) => setResourceInheritanceValue('admin_models', event.detail)}
							/>
						</div>

						{#if _user.settings.resource_inheritance.admin_models}
							<div class="rounded-xl border border-gray-100/80 dark:border-gray-800/80 p-3">
								<div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
									<div class="min-w-0">
										<div class="text-xs font-medium text-gray-600 dark:text-gray-300">
											{$i18n.t('Model Inheritance Scope')}
										</div>
										<div class="mt-1 text-[11px] text-gray-400 dark:text-gray-500">
											{isAllInherited('admin_model_ids')
												? $i18n.t('Automatically include current and future admin models.')
												: $i18n.t('Only selected admin models are available to this user.')}
										</div>
									</div>
									<div
										class="inline-flex shrink-0 rounded-xl border border-gray-100 bg-gray-50 p-1 dark:border-gray-800 dark:bg-gray-900"
										aria-label={$i18n.t('Model Inheritance Scope')}
									>
										<button
											type="button"
											aria-pressed={isAllInherited('admin_model_ids')}
											class={getScopeButtonClasses(isAllInherited('admin_model_ids'))}
											on:click={() =>
												setAllInherited('admin_model_ids', true, inheritanceOptions.admin_models)}
										>
											{$i18n.t('All')}
										</button>
										<button
											type="button"
											aria-pressed={!isAllInherited('admin_model_ids')}
											class={getScopeButtonClasses(!isAllInherited('admin_model_ids'))}
											on:click={() =>
												setAllInherited(
													'admin_model_ids',
													false,
													inheritanceOptions.admin_models
												)}
										>
											{$i18n.t('Specified')}
										</button>
									</div>
								</div>

								<div class="mt-3 flex items-center justify-between gap-3 text-[11px]">
									<span class="truncate text-gray-400 dark:text-gray-500">
										{$i18n.t('Available admin models')}
									</span>
									<span
										class="shrink-0 rounded-full bg-gray-100 px-2 py-0.5 font-medium text-gray-500 dark:bg-gray-800 dark:text-gray-300"
									>
										{isAllInherited('admin_model_ids')
											? $i18n.t('All current and future')
											: `${getSelectedResourceCount('admin_model_ids', inheritanceOptions.admin_models)}/${inheritanceOptions.admin_models.length} ${$i18n.t('selected')}`}
									</span>
								</div>

								{#if !isAllInherited('admin_model_ids')}
									<div class="mt-3 space-y-1 max-h-32 overflow-y-auto pr-1">
										{#if inheritanceOptionsLoading}
											<div class="text-xs text-gray-400 dark:text-gray-500">
												{$i18n.t('Loading...')}
											</div>
										{:else if inheritanceOptions.admin_models.length === 0}
											<div class="text-xs text-gray-400 dark:text-gray-500">
												{$i18n.t('No admin models available.')}
											</div>
										{:else}
											{#each inheritanceOptions.admin_models as option}
												<label
													class="flex items-start gap-2 rounded-lg px-2 py-1.5 hover:bg-gray-50 dark:hover:bg-gray-800/40"
												>
													<input
														type="checkbox"
														class="mt-0.5"
														checked={getSelectedResourceIds(
															'admin_model_ids',
															inheritanceOptions.admin_models
														).includes(option.id)}
														on:change={() =>
															toggleInheritedResource(
																'admin_model_ids',
																inheritanceOptions.admin_models,
																option.id
															)}
													/>
													<span class="min-w-0">
														<span
															class="block truncate text-xs font-medium text-gray-700 dark:text-gray-200"
														>
															{option.name}
														</span>
														<span
															class="block truncate text-[11px] text-gray-400 dark:text-gray-500"
														>
															{option.owner_name ? `${option.owner_name} - ` : ''}{option.id}
														</span>
													</span>
												</label>
											{/each}
										{/if}
									</div>
								{/if}
							</div>
						{/if}

						<div class="flex items-start justify-between gap-4">
							<div>
								<div class="text-sm font-medium text-gray-700 dark:text-gray-200">
									{$i18n.t('Inherit Admin MCP')}
								</div>
								<div class="mt-1 text-xs text-gray-400 dark:text-gray-500">
									{$i18n.t('Allow this user to use MCP servers configured by admins.')}
								</div>
							</div>
							<Switch
								state={_user.settings.resource_inheritance.admin_mcp_servers}
								on:change={(event) =>
									setResourceInheritanceValue('admin_mcp_servers', event.detail)}
							/>
						</div>

						{#if _user.settings.resource_inheritance.admin_mcp_servers}
							<div class="rounded-xl border border-gray-100/80 dark:border-gray-800/80 p-3">
								<div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
									<div class="min-w-0">
										<div class="text-xs font-medium text-gray-600 dark:text-gray-300">
											{$i18n.t('MCP Inheritance Scope')}
										</div>
										<div class="mt-1 text-[11px] text-gray-400 dark:text-gray-500">
											{isAllInherited('admin_mcp_server_ids')
												? $i18n.t('Automatically include current and future admin MCP servers.')
												: $i18n.t('Only selected admin MCP servers are available to this user.')}
										</div>
									</div>
									<div
										class="inline-flex shrink-0 rounded-xl border border-gray-100 bg-gray-50 p-1 dark:border-gray-800 dark:bg-gray-900"
										aria-label={$i18n.t('MCP Inheritance Scope')}
									>
										<button
											type="button"
											aria-pressed={isAllInherited('admin_mcp_server_ids')}
											class={getScopeButtonClasses(isAllInherited('admin_mcp_server_ids'))}
											on:click={() =>
												setAllInherited(
													'admin_mcp_server_ids',
													true,
													inheritanceOptions.admin_mcp_servers
												)}
										>
											{$i18n.t('All')}
										</button>
										<button
											type="button"
											aria-pressed={!isAllInherited('admin_mcp_server_ids')}
											class={getScopeButtonClasses(!isAllInherited('admin_mcp_server_ids'))}
											on:click={() =>
												setAllInherited(
													'admin_mcp_server_ids',
													false,
													inheritanceOptions.admin_mcp_servers
												)}
										>
											{$i18n.t('Specified')}
										</button>
									</div>
								</div>

								<div class="mt-3 flex items-center justify-between gap-3 text-[11px]">
									<span class="truncate text-gray-400 dark:text-gray-500">
										{$i18n.t('Available admin MCP servers')}
									</span>
									<span
										class="shrink-0 rounded-full bg-gray-100 px-2 py-0.5 font-medium text-gray-500 dark:bg-gray-800 dark:text-gray-300"
									>
										{isAllInherited('admin_mcp_server_ids')
											? $i18n.t('All current and future')
											: `${getSelectedResourceCount('admin_mcp_server_ids', inheritanceOptions.admin_mcp_servers)}/${inheritanceOptions.admin_mcp_servers.length} ${$i18n.t('selected')}`}
									</span>
								</div>

								{#if !isAllInherited('admin_mcp_server_ids')}
									<div class="mt-3 space-y-1 max-h-32 overflow-y-auto pr-1">
										{#if inheritanceOptionsLoading}
											<div class="text-xs text-gray-400 dark:text-gray-500">
												{$i18n.t('Loading...')}
											</div>
										{:else if inheritanceOptions.admin_mcp_servers.length === 0}
											<div class="text-xs text-gray-400 dark:text-gray-500">
												{$i18n.t('No admin MCP servers available.')}
											</div>
										{:else}
											{#each inheritanceOptions.admin_mcp_servers as option}
												<label
													class="flex items-start gap-2 rounded-lg px-2 py-1.5 hover:bg-gray-50 dark:hover:bg-gray-800/40"
												>
													<input
														type="checkbox"
														class="mt-0.5"
														checked={getSelectedResourceIds(
															'admin_mcp_server_ids',
															inheritanceOptions.admin_mcp_servers
														).includes(option.id)}
														on:change={() =>
															toggleInheritedResource(
																'admin_mcp_server_ids',
																inheritanceOptions.admin_mcp_servers,
																option.id
															)}
													/>
													<span class="min-w-0">
														<span
															class="block truncate text-xs font-medium text-gray-700 dark:text-gray-200"
														>
															{option.name}
														</span>
														<span
															class="block truncate text-[11px] text-gray-400 dark:text-gray-500"
														>
															{option.owner_name
																? `${option.owner_name} - `
																: ''}{option.transport_type?.toUpperCase?.() ??
																'HTTP'}{option.tool_count ? ` - ${option.tool_count} tools` : ''}
														</span>
													</span>
												</label>
											{/each}
										{/if}
									</div>
								{/if}
							</div>
						{/if}
					</div>
				{/if}
			</div>

			<div class="flex justify-end mt-5">
				<button
					class="inline-flex items-center gap-2 rounded-xl bg-gray-900 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-gray-800 dark:bg-white dark:text-gray-900 dark:hover:bg-gray-100"
					type="submit"
				>
					{$i18n.t('Save')}
				</button>
			</div>
		</form>
	</div>
</Modal>
