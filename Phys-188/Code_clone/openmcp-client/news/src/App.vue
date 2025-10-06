<script setup lang="ts">
import OmHeader from './components/Header.vue';
import OmWhatNews from './components/WhatNews.vue';
import OmMoreFeature from './components/MoreFeature.vue';
import OmCoreFeature from './components/CoreFeature.vue';
import OmSponsor from './components/Sponsor.vue';
import OmResource from './components/Resource.vue';
import OmTroubleshoot from './components/Troubleshoot.vue';
import OmContributor from './components/Contributor.vue';

import data from './data.json';``

</script>

<template>
	<main class="openmcp-news-root">
		<om-header :version="data.version" />

		<!-- 1. 📣 What is news in OpenMCP -->
		<om-what-news :version="data.version" :changelogs="data.changelogs" />

		<!-- 2. 🐳 Learn more features -->
		<om-more-feature />

		<!-- 3. ✨ Core Features -->
		<om-core-feature />

		<!-- 4. ❤️ How to sponsor -->
		<om-sponsor />

		<!-- 5. 📚 Resources -->
		<om-resource />

		<!-- 6. 🔧 Troubleshooting -->
		<om-troubleshoot />

		<!-- 7. 👥 Contributors -->
		<om-contributor :contributors="data.contributors" />
	</main>
</template>

<style>
body {
	color: var(--foreground, #222);
	background: var(--background, #fff);
	font-size: var(--vscode-font-size);
	max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
	font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6;
}

.openmcp-news-root {
	color: var(--foreground, #222);
	background: var(--background, #fff);
	padding: 32px 0 64px 0;
	min-height: 100vh;
	box-sizing: border-box;
	max-width: 820px;
	margin: 0 auto;
}

.release-link {
	color: #B988D1;
	font-weight: 500;
	text-decoration: underline;
	margin-bottom: 8px;
	display: inline-block;
	transition: color 0.2s;
}

.release-link:hover {
	color: #8e5bbf;
}

.news-list {
	list-style: none;
	padding: 0;
	margin: 0;
}

.news-badge {
	display: inline-block;
	background: #B988D1;
	color: #fff;
	border-radius: 8px;
	font-size: 0.85em;
	padding: 2px 10px;
	margin-right: 10px;
	font-weight: 500;
	vertical-align: middle;
}

.openmcp-header {
	display: flex;
	justify-content: center;
	align-items: center;
	gap: 24px;
	margin: 0 0 32px 0;
	padding: 0 0 16px 0;
}

@media screen and (max-width: 600px) {
	.openmcp-header {
		flex-direction: column;
		align-items: center;
	}
	
}

.margin-bottom {
	margin-bottom: 32px;
}
</style>