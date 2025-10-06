<template>
    <el-tour v-model="openTour">
        <el-tour-step
            :next-button-props="{ children: t('begin') }"
            :show-close="false"
        >
            <template #header>
                <TourTitle>{{ t('introduction') }}</TourTitle>
            </template>
            <div style="display: flex; padding: 10px; padding-bottom: 20px;">
                <div class="tour-common-text">
                    {{ t('guide.1.1') }}

                    <br><br>

                    {{ t('guide.1.2') }}

                    <br><br>

                    {{ t('guide.1.3') }}
                </div>

            </div>
        </el-tour-step>

        <el-tour-step
            target="#connected-status-container"
            :prev-button-props="{ children: t('prev-step') }"
            :next-button-props="{ children: t('next-step') }"
            :show-close="false"
        >
            <template #header>
                <TourTitle>{{ t('guide') }}</TourTitle>
            </template>
            <div class="tour-common-text">
                {{ t('guide.2.1') }}


                <br><br>

                {{ t('guide.2.2') }}
            </div>
        </el-tour-step>


        <el-tour-step
            target="#sidebar-connect"
            :prev-button-props="{ children: t('prev-step') }"
            :next-button-props="{ children: t('next-step'), onClick: () => router.push(baseUrl + 'connect') }"
            :show-close="false"
        >
            <template #header>
                <TourTitle>{{ t("connect") }}</TourTitle>
            </template>
            <div class="tour-common-text">
                {{ t('guide.3.1') }}
            </div>
        </el-tour-step>

        <el-tour-step
            :target="mcpClientAdapter.clients[0].connectionSettingRef"
            :prev-button-props="{ children: t('prev-step') }"
            :next-button-props="{ children: t('next-step') }"
            :show-close="false"
            placement="right"
        >
            <template #header>
                <TourTitle>{{ t("connect") }}</TourTitle>
            </template>
            <div class="tour-common-text">
                {{ t('guide.4.1') }}

                <br><br>

                {{ t('guide.4.2') }}

                {{ t('guide.4.3') }}
            </div>
        </el-tour-step>

        <el-tour-step
            :target="mcpClientAdapter.clients[0].connectionLogRef"
            :prev-button-props="{ children: t('prev-step') }"
            :next-button-props="{ children: t('next-step') }"
            :show-close="false"
            placement="left"
        >
            <template #header>
                <TourTitle>{{ t("connect") }}</TourTitle>
            </template>
            <div class="tour-common-text">
                {{ t('guide.5.1') }}
            </div>
        </el-tour-step>

        <el-tour-step
            :target="mcpServerAddRef"
            :prev-button-props="{ children: t('prev-step') }"
            :next-button-props="{ children: t('next-step') }"
            :show-close="false"
        >
            <template #header>
                <TourTitle>{{ t("debug") }}</TourTitle>
            </template>
            <div class="tour-common-text">
                {{ t('guide.6.1') }}
            </div>
        </el-tour-step>

        <el-tour-step
            target="#sidebar-debug"
            :prev-button-props="{ children: t('prev-step') }"
            :next-button-props="{ children: t('next-step'), onClick: () => router.push(baseUrl + 'debug') }"
            :show-close="false"
        >
            <template #header>
                <TourTitle>{{ t("debug") }}</TourTitle>
            </template>
            <div class="tour-common-text">
                {{ t('guide.7.1') }}
            </div>
        </el-tour-step>

        <el-tour-step
            :target="welcomeRef"
            :prev-button-props="{ children: t('prev-step') }"
            :next-button-props="{ children: t('next-step') }"
            :show-close="false"
            placement="right"
        >
            <template #header>
                <TourTitle>{{ t("debug") }}</TourTitle>
            </template>
            <div class="tour-common-text">
                {{ t('guide.8.1') }}
            </div>
        </el-tour-step>

        <el-tour-step
            :target="welcomeRef"
            :prev-button-props="{ children: t('prev-step') }"
            :next-button-props="{ children: t('next-step') }"
            :show-close="false"
            placement="right"
        >
            <template #header>
                <TourTitle>{{ t("debug") }}</TourTitle>
            </template>
            <div class="tour-common-text">
                {{ t('guide.9.1') }}
            </div>
        </el-tour-step>

        <el-tour-step
            :target="welcomeRef"
            :prev-button-props="{ children: t('prev-step') }"
            :next-button-props="{ children: t('next-step') }"
            :show-close="false"
            placement="right"
        >
            <template #header>
                <TourTitle>{{ t("debug") }}</TourTitle>
            </template>
            <div class="tour-common-text">
                {{ t('guide.10.1') }}
            </div>
        </el-tour-step>

        <el-tour-step
            target="#sidebar-setting"
            :prev-button-props="{ children: t('prev-step'), onClick: () => router.push(baseUrl + 'debug') }"
            :next-button-props="{ children: t('next-step'), onClick: () => router.push(baseUrl + 'setting') }"
            :show-close="false"
        >
            <template #header>
                <TourTitle>{{ t("setting") }}</TourTitle>
            </template>
            <div class="tour-common-text">
                {{ t('guide.11.1') }}
            </div>
        </el-tour-step>


        <el-tour-step
            :target="llmSettingRef"
            :prev-button-props="{ children: t('prev-step') }"
            :next-button-props="{ children: t('next-step') }"
            :show-close="false"
            placement="right"
        >
            <template #header>
                <TourTitle>{{ t("setting") }}</TourTitle>
            </template>
            <div class="tour-common-text">
                {{ t('guide.12.1') }}
            </div>
        </el-tour-step>


        <el-tour-step
            target="#add-new-server-button"
            :prev-button-props="{ children: t('prev-step') }"
            :next-button-props="{ children: t('next-step') }"
            :show-close="false"
        >
            <template #header>
                <TourTitle>{{ t("setting") }}</TourTitle>
            </template>
            <div class="tour-common-text">
                {{ t('guide.13.1') }}
            </div>
        </el-tour-step>


        <el-tour-step
            target="#test-llm-button"
            :prev-button-props="{ children: t('prev-step') }"
            :next-button-props="{ children: t('next-step') }"
            :show-close="false"
        >
            <template #header>
                <TourTitle>{{ t("setting") }}</TourTitle>
            </template>
            <div class="tour-common-text">
                {{ t('guide.14.1') }}
            </div>
        </el-tour-step>


        <el-tour-step
            target="#save-llm-button"
            :prev-button-props="{ children: t('prev-step') }"
            :next-button-props="{ children: t('next-step') }"
            :show-close="false"
        >
            <template #header>
                <TourTitle>{{ t("setting") }}</TourTitle>
            </template>
            <div class="tour-common-text">
                {{ t('guide.15.1') }}
            </div>
        </el-tour-step>


        <el-tour-step
            :prev-button-props="{ children: t('prev-step'), onClick: () => router.push(baseUrl + 'setting') }"
            :next-button-props="{ children: t('next-step') }"
            :show-close="false"
        >
            <template #header>
                <TourTitle>🎉 {{ t('congratulation') }}</TourTitle>
            </template>
            <div class="tour-common-text">
                🎉 {{ t('guide.16.1') }}
                
                <br>
                <br>
                
                <a href="https://openmcp.kirigaya.cn/" target="_blank">{{ t("openmcp-document") }}</a>
                
                {{ t('guide.16.2') }}

                <br><br>

                {{ t('guide.16.3') }}
                {{ t('guide.16.4') }}
            </div>
        </el-tour-step>

        <el-tour-step
            :prev-button-props="{ children: t('prev-step'), onClick: () => router.push(baseUrl + 'setting') }"
            :next-button-props="{ children: t('finish'), onClick: () => finishTour() }"
            :show-close="false"
        >
            <template #header>
                <TourTitle>{{ t('maybe-end') }}</TourTitle>
            </template>
            <div class="tour-common-text">
                <pre><code style="color: unset !important; background-color: unset !important;"
                >(base) <span style="color: greenyellow">➜</span>  <span style="color: #6AC2CF">.openmcp</span> <span style="color: #6BC34B">cat</span> <span style="color: #D357DB">KEY</span>
直面恐惧，创造未来
Face your fears, create the future
恐怖に直面し、未来を創り出</code></pre>
            </div>
        </el-tour-step>
    </el-tour>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import TourTitle from './tour-title.vue';

import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import { welcomeRef } from '@/views/debug/welcome';
import { llmSettingRef } from '@/views/setting/api';
import { userHasReadGuide } from './tour';
import { setTour } from '@/hook/setting';
import { mcpClientAdapter } from '@/views/connect/core';
import { mcpServerAddRef } from '@/views/connect';

const openTour = ref(true);

const { t } = useI18n();

const router = useRouter();

const baseUrl = import.meta.env.BASE_URL;

function finishTour() {
    openTour.value = false;
    userHasReadGuide.value = true;
    setTour();
}

</script>

<style>
.tour-common-text {
    font-size: 1.0rem;
    padding: 10px;
    padding-bottom: 20px;
    line-height: 1.5;
}

.tour-warning {
    display: flex;
    background-color: rgba(230, 162, 60, 0.5);
    border-radius: .5em;
    padding: 5px;
    margin: 5px 0;
}

.tour-common-text code {
    color: unset!important;
    background-color: unset!important;
}
</style>