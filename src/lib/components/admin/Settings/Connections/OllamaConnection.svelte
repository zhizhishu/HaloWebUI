<script lang="ts">
	import { getContext } from 'svelte';
	import type { Writable } from 'svelte/store';
	import type { i18n as i18nType } from 'i18next';

	const i18n = getContext('i18n') as Writable<i18nType>;

	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import LetterAvatar from '$lib/components/common/LetterAvatar.svelte';
	import ModelIcon from '$lib/components/common/ModelIcon.svelte';
	import AddConnectionModal from '$lib/components/AddConnectionModal.svelte';
	import ConfirmDialog from '$lib/components/common/ConfirmDialog.svelte';

	import Cog6 from '$lib/components/icons/Cog6.svelte';
	import ManageOllamaModal from './ManageOllamaModal.svelte';
	import Download from '$lib/components/icons/Download.svelte';
	import { submitProviderConnectionEdit } from '$lib/utils/provider-connections';

	type ConnectionConfig = {
		enable?: boolean;
		remark?: string;
		tags?: Array<{ name: string }>;
		icon?: string;
		key?: string;
	};
	type Connection = {
		url: string;
		key: string;
		config: ConnectionConfig;
	};

	export let onDelete: () => void | Promise<void> = () => {};
	export let onSubmit: (connection: Connection) => void | Promise<void> = async () => {};

	export let url = '';
	export let idx = 0;
	export let config: ConnectionConfig = {};

	let showManageModal = false;
	let showConfigModal = false;
	let showDeleteConfirmDialog = false;

	$: isEnabled = config?.enable ?? true;
	$: displayName = config?.remark || url;
	$: tags = config?.tags ?? [];

	const handleSubmit = async (connection: Connection) => {
		await submitProviderConnectionEdit(
			{ url, key: config?.key ?? '', config },
			connection,
			(nextConnection) => {
				url = nextConnection.url;
				config = { ...nextConnection.config, key: nextConnection.key };
			},
			onSubmit
		);
	};
</script>

<AddConnectionModal
	ollama
	edit
	bind:show={showConfigModal}
	connection={{
		url,
		key: config?.key ?? '',
		config: config
	}}
	onDelete={() => {
		showDeleteConfirmDialog = true;
	}}
	onSubmit={handleSubmit}
/>

<ConfirmDialog
	bind:show={showDeleteConfirmDialog}
	closeOnConfirm={false}
	onConfirm={async () => {
		await onDelete();
		showConfigModal = false;
	}}
/>

<ManageOllamaModal bind:show={showManageModal} urlIdx={idx} />

<button
	type="button"
	class="w-full bg-white dark:bg-gray-900 rounded-lg px-4 py-3 border border-gray-100 dark:border-gray-800 hover:border-gray-200 dark:hover:border-gray-700 transition cursor-pointer text-left {!isEnabled
		? 'opacity-60'
		: ''}"
	on:click={() => {
		showConfigModal = true;
	}}
>
	<div class="flex items-center justify-between gap-3">
		<div class="flex items-center gap-3 flex-1 min-w-0">
			{#if config?.icon}
				<ModelIcon src={config.icon} alt="avatar" className="rounded-xl size-8 shrink-0" />
			{:else}
				<LetterAvatar name={displayName} size="size-8" />
			{/if}
			<div class="flex-1 min-w-0">
				<div class="flex items-center gap-2 flex-wrap">
					<div class="text-sm font-medium text-gray-800 dark:text-gray-100 truncate">
						{displayName}
					</div>
					{#if !isEnabled}
						<span
							class="text-xs px-1.5 py-0.5 bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 rounded"
						>
							{$i18n.t('Disabled')}
						</span>
					{/if}
					{#each tags as tag}
						<span
							class="text-xs px-1.5 py-0.5 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded"
						>
							{tag.name}
						</span>
					{/each}
				</div>
				{#if config?.remark && url}
					<div class="text-xs text-gray-400 dark:text-gray-500 truncate mt-0.5">
						{url}
					</div>
				{/if}
			</div>
		</div>
		<div class="flex-shrink-0 flex items-center gap-1">
			<Tooltip content={$i18n.t('Manage Models')}>
				<button
					class="p-1.5 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition"
					on:click|stopPropagation={() => {
						showManageModal = true;
					}}
					type="button"
				>
					<Download className="size-4 text-gray-400 dark:text-gray-500" />
				</button>
			</Tooltip>
			<Cog6 className="size-4 text-gray-400 dark:text-gray-500" />
		</div>
	</div>
</button>
