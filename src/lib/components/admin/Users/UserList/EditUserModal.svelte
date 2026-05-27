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
	import {
		countSelectedResourceIds,
		getResourceInheritanceMode,
		getSelectedResourceIds as getSelectedInheritedResourceIds,
		isAllResourceInherited,
		normalizeResourceInheritance,
		setResourceInheritanceMode,
		toggleSelectedResourceId,
		type ResourceInheritanceMode,
		type ResourceInheritanceSelectionKey,
		type ResourceInheritanceSettings
	} from '$lib/utils/resource-inheritance';

	import Modal from '$lib/components/common/Modal.svelte';
	import LetterAvatar from '$lib/components/common/LetterAvatar.svelte';
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

	let inheritanceOptions: ResourceInheritanceOptions = {
		admin_models: [],
		admin_mcp_servers: []
	};
	let inheritanceOptionsLoading = false;
	let inheritanceOptionsLoaded = false;
	let inheritanceOptionsLoadPromise: Promise<boolean> | null = null;
	const pendingSelectCurrentOnLoad = new Set<ResourceInheritanceSelectionKey>();

	const getOptionsForKey = (
		key: ResourceInheritanceSelectionKey,
		options: ResourceInheritanceOptions = inheritanceOptions
	) => (key === 'admin_model_ids' ? options.admin_models : options.admin_mcp_servers);

	const getOptionIds = (options: ResourceInheritanceOption[]) => options.map((option) => option.id);

	const setResourceInheritance = (resource_inheritance: ResourceInheritanceSettings) => {
		_user = {
			..._user,
			settings: {
				..._user.settings,
				resource_inheritance
			}
		};
	};

	const setResourceInheritanceValue = (key: ResourceInheritanceSelectionKey, value: string[]) => {
		setResourceInheritance({
			..._user.settings.resource_inheritance,
			[key]: value
		});
	};

	const loadInheritanceOptions = async (): Promise<boolean> => {
		if (selectedUser?.role === 'admin' || inheritanceOptionsLoaded) {
			return true;
		}
		if (inheritanceOptionsLoadPromise) {
			return inheritanceOptionsLoadPromise;
		}

		inheritanceOptionsLoading = true;
		inheritanceOptionsLoadPromise = (async () => {
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
				return true;
			}
			return false;
		})();

		const loaded = await inheritanceOptionsLoadPromise;
		inheritanceOptionsLoading = false;
		inheritanceOptionsLoadPromise = null;
		return loaded;
	};

	const getModeFromEvent = (event: Event): ResourceInheritanceMode => {
		const value = (event.currentTarget as HTMLSelectElement).value;
		return value === 'specified' || value === 'disabled' ? value : 'all';
	};

	const getCurrentResourceMode = (key: ResourceInheritanceSelectionKey) =>
		getResourceInheritanceMode(_user.settings.resource_inheritance, key);

	const isSpecifiedMode = (key: ResourceInheritanceSelectionKey) =>
		getCurrentResourceMode(key) === 'specified';

	const isAllInherited = (key: ResourceInheritanceSelectionKey) =>
		isAllResourceInherited(_user.settings.resource_inheritance, key);

	const getSelectedResourceIds = (
		key: ResourceInheritanceSelectionKey,
		options: ResourceInheritanceOption[]
	) =>
		getSelectedInheritedResourceIds(
			_user.settings.resource_inheritance,
			key,
			getOptionIds(options)
		);

	const setResourceMode = (
		key: ResourceInheritanceSelectionKey,
		mode: ResourceInheritanceMode,
		options: ResourceInheritanceOption[]
	) => {
		if (mode === 'all' || mode === 'disabled') {
			pendingSelectCurrentOnLoad.delete(key);
		} else if (!inheritanceOptionsLoaded && options.length === 0) {
			pendingSelectCurrentOnLoad.add(key);
			void loadInheritanceOptions();
		}

		setResourceInheritance(
			setResourceInheritanceMode(
				_user.settings.resource_inheritance,
				key,
				mode,
				getOptionIds(options)
			)
		);
	};

	const toggleInheritedResource = (
		key: ResourceInheritanceSelectionKey,
		options: ResourceInheritanceOption[],
		id: string
	) => {
		setResourceInheritance(
			toggleSelectedResourceId(_user.settings.resource_inheritance, key, getOptionIds(options), id)
		);
	};

	const getSelectedResourceCount = (
		key: ResourceInheritanceSelectionKey,
		options: ResourceInheritanceOption[]
	) => countSelectedResourceIds(_user.settings.resource_inheritance, key, getOptionIds(options));

	const selectedUserNeedsInheritanceOptions = () =>
		selectedUser?.role !== 'admin' &&
		(isSpecifiedMode('admin_model_ids') || isSpecifiedMode('admin_mcp_server_ids'));

	const canSaveUser = () =>
		!inheritanceOptionsLoading ||
		!selectedUserNeedsInheritanceOptions() ||
		inheritanceOptionsLoaded;

	const createEditableUser = (user: any) => ({
		id: user?.id ?? '',
		profile_image_url: user?.profile_image_url ?? '',
		name: user?.name ?? '',
		email: user?.email ?? '',
		password: '',
		note: user?.note ?? '',
		settings: {
			resource_inheritance: normalizeResourceInheritance(user?.settings)
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
		if (selectedUserNeedsInheritanceOptions() && !inheritanceOptionsLoaded) {
			const loaded = await loadInheritanceOptions();
			if (!loaded) {
				toast.error($i18n.t('Load resource inheritance options before saving.'));
				return;
			}
		}

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

						<div class="rounded-xl border border-gray-100/80 dark:border-gray-800/80 p-3">
							<div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
								<div class="min-w-0">
									<div class="text-sm font-medium leading-5 text-gray-700 dark:text-gray-200">
										{$i18n.t('Inherit Admin Models')}
									</div>
									<div class="mt-1 text-xs leading-5 text-gray-400 dark:text-gray-500">
										{getCurrentResourceMode('admin_model_ids') === 'disabled'
											? $i18n.t('Disabled')
											: isAllInherited('admin_model_ids')
												? $i18n.t('Automatically include current and future admin models.')
												: $i18n.t('Only selected admin models are available to this user.')}
									</div>
								</div>
								{#key getCurrentResourceMode('admin_model_ids')}
									<select
										class="h-9 w-full shrink-0 rounded-lg border border-gray-200 bg-white px-2.5 text-xs font-medium leading-5 text-gray-700 outline-none transition focus:border-gray-400 sm:w-32 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-200"
										value={getCurrentResourceMode('admin_model_ids')}
										aria-label={$i18n.t('Model Inheritance Scope')}
										on:change={(event) =>
											setResourceMode(
												'admin_model_ids',
												getModeFromEvent(event),
												inheritanceOptions.admin_models
											)}
									>
										<option value="disabled">{$i18n.t('Disabled')}</option>
										<option value="all">{$i18n.t('All')}</option>
										<option value="specified">{$i18n.t('Specified')}</option>
									</select>
								{/key}
							</div>

							<div class="mt-3 flex items-center justify-between gap-3 text-[11px] leading-5">
								<span class="truncate text-gray-400 dark:text-gray-500">
									{$i18n.t('Available admin models')}
								</span>
								<span
									class="shrink-0 rounded-full bg-gray-100 px-2 py-0.5 font-medium text-gray-500 dark:bg-gray-800 dark:text-gray-300"
								>
									{getCurrentResourceMode('admin_model_ids') === 'disabled'
										? $i18n.t('Disabled')
										: isAllInherited('admin_model_ids')
											? $i18n.t('All current and future')
											: `${getSelectedResourceCount('admin_model_ids', inheritanceOptions.admin_models)}/${inheritanceOptions.admin_models.length} ${$i18n.t('selected')}`}
								</span>
							</div>

							{#if isSpecifiedMode('admin_model_ids')}
								<div class="mt-3 space-y-1 max-h-32 overflow-y-auto pr-1">
									{#if inheritanceOptionsLoading}
										<div class="text-xs leading-5 text-gray-400 dark:text-gray-500">
											{$i18n.t('Loading...')}
										</div>
									{:else if inheritanceOptions.admin_models.length === 0}
										<div class="text-xs leading-5 text-gray-400 dark:text-gray-500">
											{$i18n.t('No admin models available.')}
										</div>
									{:else}
										{#each inheritanceOptions.admin_models as option}
											<label
												class="flex items-start gap-2 rounded-lg px-2 py-1.5 leading-5 hover:bg-gray-50 dark:hover:bg-gray-800/40"
											>
												<input
													type="checkbox"
													class="mt-1"
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
														class="block truncate text-xs font-medium leading-5 text-gray-700 dark:text-gray-200"
													>
														{option.name}
													</span>
													<span
														class="block truncate text-[11px] leading-4 text-gray-400 dark:text-gray-500"
													>
														{option.owner_name
															? `${option.owner_name} - `
															: ''}{option.display_id ?? option.id}
													</span>
												</span>
											</label>
										{/each}
									{/if}
								</div>
							{/if}
						</div>

						<div class="rounded-xl border border-gray-100/80 dark:border-gray-800/80 p-3">
							<div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
								<div class="min-w-0">
									<div class="text-sm font-medium leading-5 text-gray-700 dark:text-gray-200">
										{$i18n.t('Inherit Admin MCP')}
									</div>
									<div class="mt-1 text-xs leading-5 text-gray-400 dark:text-gray-500">
										{getCurrentResourceMode('admin_mcp_server_ids') === 'disabled'
											? $i18n.t('Disabled')
											: isAllInherited('admin_mcp_server_ids')
												? $i18n.t('Automatically include current and future admin MCP servers.')
												: $i18n.t('Only selected admin MCP servers are available to this user.')}
									</div>
								</div>
								{#key getCurrentResourceMode('admin_mcp_server_ids')}
									<select
										class="h-9 w-full shrink-0 rounded-lg border border-gray-200 bg-white px-2.5 text-xs font-medium leading-5 text-gray-700 outline-none transition focus:border-gray-400 sm:w-32 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-200"
										value={getCurrentResourceMode('admin_mcp_server_ids')}
										aria-label={$i18n.t('MCP Inheritance Scope')}
										on:change={(event) =>
											setResourceMode(
												'admin_mcp_server_ids',
												getModeFromEvent(event),
												inheritanceOptions.admin_mcp_servers
											)}
									>
										<option value="disabled">{$i18n.t('Disabled')}</option>
										<option value="all">{$i18n.t('All')}</option>
										<option value="specified">{$i18n.t('Specified')}</option>
									</select>
								{/key}
							</div>

							<div class="mt-3 flex items-center justify-between gap-3 text-[11px] leading-5">
								<span class="truncate text-gray-400 dark:text-gray-500">
									{$i18n.t('Available admin MCP servers')}
								</span>
								<span
									class="shrink-0 rounded-full bg-gray-100 px-2 py-0.5 font-medium text-gray-500 dark:bg-gray-800 dark:text-gray-300"
								>
									{getCurrentResourceMode('admin_mcp_server_ids') === 'disabled'
										? $i18n.t('Disabled')
										: isAllInherited('admin_mcp_server_ids')
											? $i18n.t('All current and future')
											: `${getSelectedResourceCount('admin_mcp_server_ids', inheritanceOptions.admin_mcp_servers)}/${inheritanceOptions.admin_mcp_servers.length} ${$i18n.t('selected')}`}
								</span>
							</div>

							{#if isSpecifiedMode('admin_mcp_server_ids')}
								<div class="mt-3 space-y-1 max-h-32 overflow-y-auto pr-1">
									{#if inheritanceOptionsLoading}
										<div class="text-xs leading-5 text-gray-400 dark:text-gray-500">
											{$i18n.t('Loading...')}
										</div>
									{:else if inheritanceOptions.admin_mcp_servers.length === 0}
										<div class="text-xs leading-5 text-gray-400 dark:text-gray-500">
											{$i18n.t('No admin MCP servers available.')}
										</div>
									{:else}
										{#each inheritanceOptions.admin_mcp_servers as option}
											<label
												class="flex items-start gap-2 rounded-lg px-2 py-1.5 leading-5 hover:bg-gray-50 dark:hover:bg-gray-800/40"
											>
												<input
													type="checkbox"
													class="mt-1"
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
														class="block truncate text-xs font-medium leading-5 text-gray-700 dark:text-gray-200"
													>
														{option.name}
													</span>
													<span
														class="block truncate text-[11px] leading-4 text-gray-400 dark:text-gray-500"
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
					</div>
				{/if}
			</div>

			<div class="flex justify-end mt-5">
				<button
					class="inline-flex items-center gap-2 rounded-xl bg-gray-900 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-white dark:text-gray-900 dark:hover:bg-gray-100"
					type="submit"
					disabled={!canSaveUser()}
				>
					{$i18n.t('Save')}
				</button>
			</div>
		</form>
	</div>
</Modal>
