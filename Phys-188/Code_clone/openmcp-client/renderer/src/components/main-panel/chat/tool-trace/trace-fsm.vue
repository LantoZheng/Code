<template>
    <el-scrollbar class="trace-fsm-container">
        <div ref="svgContainer" class="fsm-container"></div>
        
        <!-- 节点详情弹窗 -->
        <el-dialog 
            v-model="nodeDetailVisible" 
            :title="selectedNodeData?.name || t('tool-details')" 
            width="600px"
            :before-close="handleDialogClose"
        >
            <div v-if="selectedNodeData">
                <el-descriptions :column="1" border>
                    <el-descriptions-item v-if="selectedNodeData.type" :label="t('type')">{{ selectedNodeData.type }}</el-descriptions-item>
                    <el-descriptions-item v-if="selectedNodeData.content" :label="t('content')">
                        <pre class="content-pre">{{ selectedNodeData.content }}</pre>
                    </el-descriptions-item>
                    <el-descriptions-item v-if="selectedNodeData.duration" :label="t('duration-ms')">{{ selectedNodeData.duration }}</el-descriptions-item>
                    <el-descriptions-item v-if="selectedNodeData.tokens" :label="t('total-token')">{{ selectedNodeData.tokens }}</el-descriptions-item>
                    <el-descriptions-item v-if="selectedNodeData.cacheHitRate" :label="t('cache-hit-ratio')">{{ selectedNodeData.cacheHitRate }}</el-descriptions-item>
                    <el-descriptions-item :label="t('status')">
                        <el-tag :type="getNodeStatusType(selectedNodeData.status)">
                            {{ selectedNodeData.status }}
                        </el-tag>
                    </el-descriptions-item>
                </el-descriptions>
            </div>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="nodeDetailVisible = false">{{ t('close') }}</el-button>
                </span>
            </template>
        </el-dialog>
    </el-scrollbar>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, reactive, watch } from 'vue';
import * as d3 from 'd3';
import ELK from 'elkjs/lib/elk.bundled.js';
import type { IRenderMessage } from '../chat-box/chat';
import { useI18n } from 'vue-i18n';
import { mcpClientAdapter } from '@/views/connect/core';

// 全局常量定义
const NODE_WIDTH = 200;
const NODE_HEIGHT = 50; // 减小节点高度
const NODE_RADIUS = 8; // 减小圆角
const LABEL_Y = 30; // 调整标签垂直位置
const DURATION_X = NODE_WIDTH - 10;
const DURATION_Y = 16; // 调整耗时文本位置

const { t } = useI18n();

const props = defineProps<{
    renderMessages: IRenderMessage[];
}>();

const svgContainer = ref<HTMLDivElement | null>(null);
let prevNodes: any[] = [];
let prevEdges: any[] = [];

// 节点数据映射
const nodeDataMap = new Map<string, any>();

const state = reactive({
    nodes: [] as any[],
    edges: [] as any[],
});

// 节点详情弹窗相关
const nodeDetailVisible = ref(false);
const selectedNodeData = ref<any>(null);

const handleDialogClose = () => {
    nodeDetailVisible.value = false;
    selectedNodeData.value = null;
};

// 根据状态获取标签类型
function getNodeStatusType(status: string | undefined) {
    switch (status) {
        case 'success':
            return 'success';
        case 'error':
        case 'failed':
            return 'danger';
        case 'running':
            return 'warning';
        default:
            return 'info';
    }
}

// 获取所有工具
const getAllTools = async () => {
    const items: any[] = [];
    for (const client of mcpClientAdapter.clients) {
        const clientTools = await client.getTools();
        items.push(...clientTools.values());
    }
    return items;
};

// 处理消息数据，生成节点和边
async function processMessages() {
    const nodes: any[] = [];
    const edges: any[] = [];
    const addedEdges = new Set<string>(); // 用于避免重复边
    nodeDataMap.clear();
    
    // 创建所有工具节点
    const allTools = await getAllTools();
    const toolNodesMap = new Map<string, any>();
    
    allTools.forEach((tool, index) => {
        const nodeId = `tool-${tool.name}`;
        const node = {
            id: nodeId,
            width: NODE_WIDTH,
            height: NODE_HEIGHT,
            labels: [{ text: tool.name }],
            type: 'tool'
        };
        nodes.push(node);
        toolNodesMap.set(tool.name, node);
        
        // 保存节点详细信息
        nodeDataMap.set(nodeId, {
            id: nodeId,
            name: tool.name,
            type: 'Tool',
            content: JSON.stringify(tool.inputSchema, null, 2),
            status: 'default'
        });
    });
    
    // 创建 user-input 和 assistant 节点
    props.renderMessages.forEach((message, messageIndex) => {
        if (message.role === 'user') {
            const nodeId = `user-${messageIndex}`;
            const node = {
                id: nodeId,
                width: NODE_WIDTH,
                height: NODE_HEIGHT,
                labels: [{ text: t('user-input') }],
                type: 'user'
            };
            nodes.push(node);
            
            // 保存节点详细信息
            nodeDataMap.set(nodeId, {
                id: nodeId,
                name: t('user-input'),
                type: t('user-input'),
                content: message.content,
                status: message.extraInfo?.state === 'success' ? 'success' : message.extraInfo?.state || 'default'
            });
        } else if (message.role === 'assistant/content') {
            const nodeId = `assistant-${messageIndex}`;
            // 计算耗时（当前节点与上一个节点的时间差）
            let duration = '';
            if (messageIndex > 0 && props.renderMessages[messageIndex - 1].extraInfo?.created && message.extraInfo?.created) {
                const prevMessage = props.renderMessages[messageIndex - 1];
                duration = (message.extraInfo.created - prevMessage.extraInfo.created) + ' ms';
            }
            
            // Token信息
            let tokens = '';
            let cacheHitRate = '';
            const usage = message.extraInfo?.usage;
            if (usage) {
                tokens = `Input: ${usage.prompt_tokens || 0}, Output: ${usage.completion_tokens || 0}, Total: ${usage.total_tokens || 0}`;
                const cacheHitTokens = usage.prompt_tokens_details?.cached_tokens || 0;
                const inputTokens = usage.prompt_tokens || 0;
                if (inputTokens > 0) {
                    cacheHitRate = Math.round((cacheHitTokens / inputTokens) * 100) + '%';
                }
            }
            
            const node = {
                id: nodeId,
                width: NODE_WIDTH,
                height: NODE_HEIGHT,
                labels: [{ text: t('assistant-output') }],
                type: 'assistant',
                duration // 添加耗时信息
            };
            nodes.push(node);

            // 保存节点详细信息
            nodeDataMap.set(nodeId, {
                id: nodeId,
                name: 'Assistant Message',
                type: 'Assistant Output',
                content: message.content,
                duration,
                tokens,
                cacheHitRate,
                status: message.extraInfo?.state === 'success' ? 'success' : message.extraInfo?.state || 'default'
            });
        }
    });
    
    // 创建工具调用的边
    props.renderMessages.forEach((message, messageIndex) => {
        if (message.role === 'assistant/tool_calls' && 'tool_calls' in message) {
            const toolCalls = message.tool_calls || [];
            
            toolCalls.forEach(toolCall => {
                const toolName = toolCall.function?.name;
                if (toolName && toolNodesMap.has(toolName)) {
                    // 找到前一个节点
                    let prevNodeId = null;
                    for (let i = messageIndex - 1; i >= 0; i--) {
                        const prevMessage = props.renderMessages[i];
                        if (prevMessage.role === 'user') {
                            prevNodeId = `user-${i}`;
                            break;
                        } else if (prevMessage.role === 'assistant/content') {
                            prevNodeId = `assistant-${i}`;
                            break;
                        } else if (prevMessage.role === 'assistant/tool_calls') {
                            // 找到前一个工具调用中的第一个工具
                            const prevToolCalls = prevMessage.tool_calls || [];
                            if (prevToolCalls.length > 0) {
                                const prevToolName = prevToolCalls[0].function?.name;
                                if (prevToolName) {
                                    prevNodeId = `tool-${prevToolName}`;
                                    break;
                                }
                            }
                        }
                    }
                    
                    // 如果没有找到前一个节点，则使用特殊节点
                    if (!prevNodeId) {
                        prevNodeId = 'start';
                    }
                    
                    // 创建从前一个节点到当前工具节点的边
                    const currentToolNodeId = `tool-${toolName}`;
                    const edgeId = `edge-${prevNodeId}-${currentToolNodeId}`;
                    
                    // 避免重复边
                    if (!addedEdges.has(edgeId)) {
                        edges.push({
                            id: edgeId,
                            sources: [prevNodeId],
                            targets: [currentToolNodeId]
                        });
                        addedEdges.add(edgeId);
                    }
                    
                    // 更新工具节点状态
                    const nodeData = nodeDataMap.get(currentToolNodeId);
                    if (nodeData) {
                        nodeData.status = message.extraInfo?.state === 'success' ? 'success' : message.extraInfo?.state || 'default';
                        nodeData.content = toolCall.function?.arguments;
                    }
                }
            });
            
            // 创建从最后一个工具调用到下一个节点的边
            if (toolCalls.length > 0) {
                const lastToolName = toolCalls[toolCalls.length - 1].function?.name;
                if (lastToolName && toolNodesMap.has(lastToolName)) {
                    // 找到下一个节点
                    let nextNodeId = null;
                    for (let i = messageIndex + 1; i < props.renderMessages.length; i++) {
                        const nextMessage = props.renderMessages[i];
                        if (nextMessage.role === 'user') {
                            nextNodeId = `user-${i}`;
                            break;
                        } else if (nextMessage.role === 'assistant/content') {
                            nextNodeId = `assistant-${i}`;
                            break;
                        }
                    }
                    
                    if (nextNodeId) {
                        const lastToolNodeId = `tool-${lastToolName}`;
                        const edgeId = `edge-${lastToolNodeId}-${nextNodeId}`;
                        
                        // 避免重复边
                        if (!addedEdges.has(edgeId)) {
                            edges.push({
                                id: edgeId,
                                sources: [lastToolNodeId],
                                targets: [nextNodeId]
                            });
                            addedEdges.add(edgeId);
                        }
                    }
                }
            }
        }
    });
    
    // 添加 user 和 assistant 节点之间的连接
    const userAndAssistantNodes = nodes.filter(n => n.type === 'user' || n.type === 'assistant');
    userAndAssistantNodes.forEach((node, index) => {
        if (index > 0) {
            const prevNode = userAndAssistantNodes[index - 1];
            const edgeId = `edge-${prevNode.id}-${node.id}`;
            
            // 避免重复边
            if (!addedEdges.has(edgeId)) {
                edges.push({
                    id: edgeId,
                    sources: [prevNode.id],
                    targets: [node.id]
                });
                addedEdges.add(edgeId);
            }
        }
    });

    state.nodes = nodes;
    state.edges = edges;
}

const recomputeLayout = async () => {
    const elk = new ELK();
    const elkGraph = {
        id: 'root',
        layoutOptions: {
            'elk.direction': 'DOWN',
            'elk.spacing.nodeNode': '40',
            'elk.layered.spacing.nodeNodeBetweenLayers': '40'
        },
        children: state.nodes,
        edges: state.edges
    };
    const layout = await elk.layout(elkGraph) as unknown as any;

    state.nodes.forEach((n, i) => {
        const ln = layout.children?.find((c: any) => c.id === n.id);
        if (ln) {
            n.x = ln.x;
            n.y = ln.y;
            n.width = ln.width || NODE_WIDTH;
            n.height = ln.height || NODE_HEIGHT;
        }
    });
    state.edges = layout.edges || [];

    return layout;
};

function renderSvg() {
    const prevNodeMap = new Map(prevNodes.map(n => [n.id, n]));
    const prevEdgeMap = new Map(prevEdges.map(e => [e.id, e]));

    // 计算所有节点的最小x和最大x
    const xs = state.nodes.map(n => (n.x || 0));
    const minX = Math.min(...xs);
    const maxX = Math.max(...xs.map((x, i) => x + (state.nodes[i]?.width || NODE_WIDTH)));
    const contentWidth = maxX - minX;
    const svgWidth = Math.max(contentWidth + 120, 600); // 最小宽度600px
    const offsetX = (svgWidth - contentWidth) / 2 - minX;

    const height = Math.max(...state.nodes.map(n => (n.y || 0) + (n.height || NODE_HEIGHT)), 400) + 60;

    // 不再全量清空，只清空 svg 元素
    let svg = d3.select(svgContainer.value).select('svg');
    if (svg.empty()) {
        svg = d3
            .select(svgContainer.value)
            .append('svg')
            .attr('width', '100%')
            .attr('height', height)
            .attr('viewBox', `0 0 ${svgWidth} ${height}`)
            .style('user-select', 'none') as any;
    } else {
        svg.attr('width', '100%')
           .attr('height', height)
           .attr('viewBox', `0 0 ${svgWidth} ${height}`);
        svg.selectAll('defs').remove();
    }

    // Arrow marker
    svg
        .append('defs')
        .append('marker')
        .attr('id', 'arrow')
        .attr('viewBox', '0 0 8 8')
        .attr('refX', 6)
        .attr('refY', 4)
        .attr('markerWidth', 5)
        .attr('markerHeight', 5)
        .attr('orient', 'auto')
        .append('path')
        .attr('d', 'M 0 0 L 8 4 L 0 8 z')
        .attr('fill', 'var(--main-color)');

    // 1. 创建/获取 main group
    let mainGroup = svg.select('g.main-group');
    if (mainGroup.empty()) {
        mainGroup = svg.append('g').attr('class', 'main-group') as any;
    }
    mainGroup
        .attr('transform', `translate(${offsetX}, 0)`);

    // Draw edges
    const allSections: { id: string, section: any }[] = [];
    (state.edges || []).forEach(edge => {
        const sections = edge.sections || [];
        sections.forEach((section: any, idx: number) => {
            allSections.push({
                id: (edge.id || '') + '-' + (section.id || idx),
                section
            });
        });
    });

    const edgeSelection = mainGroup.selectAll<SVGPathElement, any>('.edge')
        .data(allSections, d => d.id);

    edgeSelection.exit().remove();

    const edgeEnter = edgeSelection.enter()
        .append('path')
        .attr('class', 'edge')
        .attr('d', d => {
            const prev = prevEdgeMap.get(d.id);
            if (prev && prev.sections && prev.sections[0]) {
                const startPoint = prev.sections[0].startPoint;
                const endPoint = prev.sections[0].endPoint;
                const controlPoint1 = { x: startPoint.x, y: startPoint.y + (endPoint.y - startPoint.y) / 2 };
                const controlPoint2 = { x: endPoint.x, y: endPoint.y - (endPoint.y - startPoint.y) / 2 };
                return `M ${startPoint.x} ${startPoint.y} C ${controlPoint1.x} ${controlPoint1.y}, ${controlPoint2.x} ${controlPoint2.y}, ${endPoint.x} ${endPoint.y}`;
            }
            
            const startPoint = d.section.startPoint;
            const endPoint = d.section.endPoint;
            const controlPoint1 = { x: startPoint.x, y: startPoint.y + (endPoint.y - startPoint.y) / 2 };
            const controlPoint2 = { x: endPoint.x, y: endPoint.y - (endPoint.y - startPoint.y) / 2 };
            return `M ${startPoint.x} ${startPoint.y} C ${controlPoint1.x} ${controlPoint1.y}, ${controlPoint2.x} ${controlPoint2.y}, ${endPoint.x} ${endPoint.y}`;
        })
        .attr('fill', 'none')
        .attr('stroke', 'var(--main-color)')
        .attr('stroke-width', 2.5)
        .attr('marker-end', 'url(#arrow)');

    edgeEnter
        .transition()
        .duration(600)
        .attr('d', d => {
            const startPoint = d.section.startPoint;
            const endPoint = d.section.endPoint;
            const controlPoint1 = { x: startPoint.x, y: startPoint.y + (endPoint.y - startPoint.y) / 2 };
            const controlPoint2 = { x: endPoint.x, y: endPoint.y - (endPoint.y - startPoint.y) / 2 };
            return `M ${startPoint.x} ${startPoint.y} C ${controlPoint1.x} ${controlPoint1.y}, ${controlPoint2.x} ${controlPoint2.y}, ${endPoint.x} ${endPoint.y}`;
        });

    // update
    edgeSelection.merge(edgeEnter)
        .transition()
        .duration(600)
        .ease(d3.easeCubicInOut)
        .attr('d', d => {
            const startPoint = d.section.startPoint;
            const endPoint = d.section.endPoint;
            const controlPoint1 = { x: startPoint.x, y: startPoint.y + (endPoint.y - startPoint.y) / 2 };
            const controlPoint2 = { x: endPoint.x, y: endPoint.y - (endPoint.y - startPoint.y) / 2 };
            return `M ${startPoint.x} ${startPoint.y} C ${controlPoint1.x} ${controlPoint1.y}, ${controlPoint2.x} ${controlPoint2.y}, ${endPoint.x} ${endPoint.y}`;
        });

    // --- 节点 ---
    const nodeGroup = mainGroup.selectAll<SVGGElement, any>('.node')
        .data(state.nodes, d => d.id);

    nodeGroup.exit().remove();

    // 节点 enter
    const nodeGroupEnter = nodeGroup.enter()
        .append('g')
        .attr('class', 'node')
        .attr('transform', d => {
            const prev = prevNodeMap.get(d.id);
            if (prev) {
                return `translate(${prev.x || 0}, ${prev.y || 0})`;
            }
            return `translate(${d.x || 0}, ${d.y || 0})`;
        })
        .style('cursor', 'pointer')
        .on('click', function (event, d) {
            // 显示节点详情弹窗
            const nodeData = nodeDataMap.get(d.id);
            if (nodeData) {
                selectedNodeData.value = nodeData;
                nodeDetailVisible.value = true;
            }
        });

    // 添加节点的矩形
    nodeGroupEnter
        .append('rect')
        .attr('width', (d: any) => d.width)
        .attr('height', (d: any) => d.height)
        .attr('rx', NODE_RADIUS)
        .attr('fill', 'var(--main-light-color-20)')
        .attr('stroke', 'var(--main-light-color-10)')
        .attr('stroke-width', 1);

    // 节点文字
    nodeGroupEnter.append('text')
        .attr('x', d => d.width / 2)
        .attr('y', LABEL_Y)
        .attr('text-anchor', 'middle')
        .attr('font-size', 14)
        .attr('fill', 'var(--main-color)')
        .attr('font-weight', 600)
        .text(d => d.labels?.[0]?.text || 'Node');

    // 耗时显示（User Message 不显示）
    nodeGroupEnter.append('text')
        .attr('class', 'node-duration')
        .attr('x', DURATION_X)
        .attr('y', DURATION_Y)
        .attr('text-anchor', 'end')
        .attr('font-size', 12)
        .attr('fill', '#666')
        .text(d => {
            // user-input 不显示耗时
            if (d.type === 'user') {
                return '';
            }            
            
            const nodeData = nodeDataMap.get(d.id);
            return nodeData?.duration || '';
        });


    // 节点 enter 动画
    nodeGroupEnter
        .transition()
        .duration(600)
        .attr('transform', d => `translate(${d.x || 0}, ${d.y || 0})`);

    // 节点 update 动画
    nodeGroup
        .transition()
        .duration(600)
        .ease(d3.easeCubicInOut)
        .attr('transform', d => `translate(${d.x || 0}, ${d.y || 0})`);

    // 更新耗时文本
    nodeGroup.select('.node-duration')
        .text(d => {
            // user-input 不显示耗时            
            if (d.type === 'user') {
                return '';
            }
            const nodeData = nodeDataMap.get(d.id);
            return nodeData?.duration || '';
        });

    // 渲染结束后保存当前快照
    prevNodes = state.nodes.map(n => ({ ...n }));
    prevEdges = (state.edges || []).map(e => ({ ...e, sections: e.sections ? e.sections.map((s: any) => ({ ...s })) : [] }));
}

// 绘制流程图
async function drawDiagram() {
    // 处理消息数据
    await processMessages();
    
    // 重新计算布局
    await recomputeLayout();

    // 绘制 svg
    renderSvg();
}

// 监听 renderMessages 变化
watch(() => props.renderMessages, () => {
    nextTick(drawDiagram);
}, { deep: true });

onMounted(() => {
    nextTick(drawDiagram);
});
</script>

<style scoped>
.trace-fsm-container {
    width: 100%;
    height: 100%;
}

.fsm-container {
    width: 100%;
    height: 100%;
    min-height: 400px;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    border-radius: 8px;
    padding: 24px 0;
}

.content-pre {
    white-space: pre-wrap;
    word-break: break-all;
    margin: 0;
    padding: 8px;
    background-color: var(--el-fill-color-light);
    border-radius: 4px;
    max-height: 200px;
    overflow-y: auto;
}

.dialog-footer {
    text-align: right;
}
</style>