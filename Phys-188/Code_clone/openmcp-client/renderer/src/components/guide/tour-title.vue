<template>
    <div class="tour-title">
        <span class="openmcp-image tour-title-icon"></span>
        <slot></slot>
    </div>    
</template>

<script setup lang="ts">

</script>

<style>
.tour-title {
    display: flex;
    align-items: center;
    margin: 10px 0;
    font-size: 18px;
}

.tour-title-icon {
    height: 45px;
    width: 45px;
    margin-right: 5px;
}
</style>