<script lang="ts">
	import AdminConnections from '$lib/components/admin/Settings/Connections.svelte';
	import ConnectionsPreferences from '$lib/components/settings/ConnectionsPreferences.svelte';
	import { user } from '$lib/stores';
	import { getContext } from 'svelte';
	import type { UserSettingsContext } from '$lib/types/user-settings';

	const { saveSettings } = getContext<UserSettingsContext>('user-settings');
</script>

{#if $user?.role === 'admin'}
	<AdminConnections />
{:else}
	<ConnectionsPreferences {saveSettings} />
{/if}
