<template>
    <el-dialog v-model="dialogVisible" title="请输入密码" :close-on-click-modal="false" :close-on-press-escape="false"
        :show-close="false" width="30%" top="20vh">
        <br>
        <el-input v-model="privilegeStatus.password"
            type="password"
            placeholder="请输入密码"
            @keyup.enter.prevent="handleSubmit"
        />
        <template #footer>
            <el-button type="primary" @click="handleSubmit">确认</el-button>
        </template>
    </el-dialog>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { privilegeStatus } from './status';
import { useMessageBridge } from '@/api/message-bridge';
import { initialise } from '@/views/connect';

const dialogVisible = ref(true);

const handleSubmit = async () => {
    const bridge = useMessageBridge();
    
    const ok = await bridge.setupWebSocket(import.meta.env.VITE_WEBSOCKET_URL + '?t=' + privilegeStatus.password);
    
    if (ok) {
        ElMessage.success('密码验证成功，欢迎回来锦恢');
        dialogVisible.value = false;

        initialise();

    } else {
        ElMessage.error('密码验证失败，请重新输入');
    }
};

onMounted(() => {
    dialogVisible.value = true;
});
</script>

<style scoped>
.el-dialog {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    margin: auto;
    z-index: 9999;
}
</style>