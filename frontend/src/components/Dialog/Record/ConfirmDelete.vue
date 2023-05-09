<template>
  <DialogBase>
    <h3 class="text-lg font-bold pb-2">
      记录删除
    </h3>
    <p>确认删除记录 {{ `${data.name} (${data.id})` }} ？</p>
    <div class="pt-2">
      <button
        class="px-4 py-1 mr-2 bg-blue-500 text-white hover:bg-blue-400 border rounded-lg transition-all"
        @click="$emit('submit', 'confirm-delete')"
      >
        确认
      </button>
      <button
        class="px-4 py-1 mr-2 hover:bg-slate-400/30  border rounded-lg transition-all"
        @click="$emit('close')"
      >
        取消
      </button>
    </div>
  </DialogBase>
</template>

<script setup lang="ts">
defineProps<{
  data: {
    id: String
    type: String
    name: String
    value: String
    ttl: Number
  }
}>()
defineEmits(['submit', 'close'])
</script>
