<template>
    <div class="swim-pool">
        <transition-group name="lane-move" tag="div">
            <div v-for="(lane, laneIdx) in lanes" :key="lane.id" class="swim-lane" @dragover.prevent
                @drop="onDrop(laneIdx)">
                <div class="lane-title">Group {{ laneIdx + 1 }}</div>
                <div v-for="tool in lane.tools" :key="tool.name" class="tool-card" draggable="true"
                    @dragstart="onDragStart(tool, laneIdx)">
                    {{ tool.name }}
                </div>
            </div>
        </transition-group>
    </div>
</template>

<script setup lang="ts">
import type { ToolItem } from '@/hook/type';
import { mcpClientAdapter } from '@/views/connect/core';
import { ref, onMounted } from 'vue';

// 工具类型
interface Tool {
    id: string;
    name: string;
}

interface Lane {
    id: string;
    tools: ToolItem[];
}

// 工具列表
const tools = ref<ToolItem[]>([]);

// 泳道列表
const lanes = ref<Lane[]>([]);

// 获取所有工具
const getAllTools = async () => {
    const items = [];
    for (const client of mcpClientAdapter.clients) {
        const clientTools = await client.getTools();
        items.push(...clientTools.values());
    }
    return items;
};

// 初始化
onMounted(async () => {
    tools.value = await getAllTools();
    console.log(tools.value);
    
    lanes.value = tools.value.map((tool, idx) => ({
        id: `lane-${idx}`,
        tools: [tool]
    }));
});

// 拖拽信息
let dragInfo: { tool: ToolItem | null; fromLane: number } = { tool: null, fromLane: -1 };

// 拖拽开始
function onDragStart(tool: ToolItem, fromLane: number) {
    dragInfo = { tool, fromLane };
}

// 拖拽释放
function onDrop(toLane: number) {
    if (dragInfo.tool && dragInfo.fromLane !== -1 && dragInfo.fromLane !== toLane) {
        // 从原泳道移除
        lanes.value[dragInfo.fromLane].tools = lanes.value[dragInfo.fromLane].tools.filter(
            t => t.name !== dragInfo.tool!.name
        );
        // 加入新泳道
        lanes.value[toLane].tools.push(dragInfo.tool);

        // 如果原泳道已空，删除该泳道
        if (lanes.value[dragInfo.fromLane].tools.length === 0) {
            lanes.value.splice(dragInfo.fromLane, 1);
        }

        // 重新排序，确保泳道顺序和索引一致
        lanes.value = lanes.value.map((lane, idx) => ({
            ...lane,
            // 可选：如果你希望泳道 id 也随序号变化
            id: `lane-${idx}`
        }));
    }
    dragInfo = { tool: null, fromLane: -1 };
}
</script>

<style scoped>
.swim-pool {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.swim-lane {
    border: 1px solid var(--sidebar);
    min-height: 60px;
    margin-bottom: 10px;
    padding: 8px;
    border-radius: 8px;
    transition: box-shadow 0.3s;
    box-shadow: 0 2px 8px 0 rgba(0,0,0,0.08);
}

.lane-title {
    font-weight: bold;
    margin-bottom: 6px;
}

.tool-card {
    border: 1px solid var(--main-color);
    border-radius: 4px;
    padding: 4px 12px;
    margin-bottom: 4px;
    cursor: grab;
    user-select: none;
}

/* 动画样式 */
.lane-move-move {
    transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>