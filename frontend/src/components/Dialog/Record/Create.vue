<!-- eslint-disable vue/no-mutating-props -->
<template>
  <DialogBase>
    <h3 class="text-lg font-bold pb-2">
      记录创建
    </h3>
    <div class="my-1">
      记录类型：<select v-model="data.type">
        <option v-for="r_type in RECORD_TYPES" :key="r_type" :value="r_type">
          {{ r_type }}
        </option>
      </select>
    </div>
    <div class="my-1">
      名称：<input v-model="data.name" type="text" class="px-2 border outline-none">
    </div>
    <div class="my-1">
      内容：<input v-model="data.value" type="text" class="px-2 border outline-none">
    </div>
    <div class="my-1">
      TTL：<input v-model.number="data.ttl" type="text" class="px-2 border outline-none">
    </div>
    <div class="pt-2">
      <button
        class="px-4 py-1 mr-2 bg-blue-500 text-white hover:bg-blue-400 border rounded-lg transition-all"
        @click="$emit('submit', 'create')"
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
import { RECORD_TYPES } from '@/config'

defineProps<{
  data: {
    type: String
    name: String
    value: String
    ttl: Number
  }
}>()
defineEmits(['submit', 'close'])
</script>
