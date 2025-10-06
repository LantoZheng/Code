<template>
    <!-- STDIO 模式下的命令输入 -->
    <div class="connection-option" v-if="client.connectionArgs.connectionType === 'STDIO'">
        <span>{{ t('connect-sigature') }}</span>
        <span style="width: 310px;">
            <el-form :model="client.connectionArgs" :rules="rules" ref="stdioForm">
                <el-form-item prop="commandString">
                    <div class="input-with-label">
                        <span class="input-label">{{ t("command") }}</span>
                        <el-input v-model="client.connectionArgs.commandString" placeholder="mcp run <your script>"></el-input>
                    </div>
                </el-form-item>
                <el-form-item prop="cwd">
                    <div class="input-with-label">
                        <span class="input-label">{{ t('cwd') }}</span>
                        <el-input v-model="client.connectionArgs.cwd" placeholder="cwd, 可为空"></el-input>
                    </div>
                </el-form-item>
            </el-form>
        </span>
    </div>

    <!-- SSE 模式下的URL输入 -->
    <div class="connection-option" v-else>
        <span>{{ t('connect-sigature') }}</span>
        <span style="width: 310px;">
            <el-form :model="client.connectionArgs" :rules="rules" ref="urlForm">
                <el-form-item prop="url">
                    <div class="input-with-label">
                        <span class="input-label">URL</span>
                        <el-input v-model="client.connectionArgs.url" placeholder="http://"></el-input>
                    </div>
                </el-form-item>
                <el-form-item prop="oauth">
                    <div class="input-with-label">
                        <span class="input-label">OAuth</span>
                        <el-input v-model="client.connectionArgs.oauth" placeholder="认证签名, 可为空"></el-input>
                    </div>
                </el-form-item>
            </el-form>
        </span>
    </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { ElMessage } from 'element-plus';
import type { FormInstance, FormRules } from 'element-plus';
import { mcpClientAdapter } from './core';

const { t } = useI18n();

const props = defineProps({
	index: {
		type: Number,
		required: true
	}
});

const client = computed(() => mcpClientAdapter.clients[props.index]);

const stdioForm = ref<FormInstance>()
const urlForm = ref<FormInstance>()

// 验证规则
const rules = reactive<FormRules>({
    commandString: [
        { required: true, message: '命令不能为空', trigger: 'blur' }
    ],
    cwd: [
        { required: false, trigger: 'blur' }
    ],
    oauth: [
        { required: false, trigger: 'blur' }
    ],
    url: [
        { required: true, message: 'URL不能为空', trigger: 'blur' }
    ]
})

// 验证当前活动表单
const validateForm = async () => {
    try {
        if (client.value.connectionArgs.connectionType === 'STDIO') {
            await stdioForm.value?.validate()
        } else {
            await urlForm.value?.validate()
        }
        return true
    } catch (error) {
        ElMessage.error('请填写必填字段')
        return false
    }
}

</script>

<style scoped>
.input-with-label {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
    width: 100%;
}

.input-label {
    width: 80px;
    font-size: 14px;
    color: var(--el-text-color-regular);
}

.connection-option {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 16px;
    height: fit-content;
    background-color: var(--el-bg-color);
    border-radius: 4px;
    margin-bottom: 16px;
}

.connection-option .el-form-item {
    margin-bottom: 0;
}

</style>