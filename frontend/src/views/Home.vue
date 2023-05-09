<template>
  <div>
    <!-- <h1 class="text-5xl font-thin pb-3 select-none">
      DNS Helper
    </h1> -->
    <h2 class="text-2xl font-bold py-2">
      域名列表
      <button class="p-1 mx-1 hover:bg-slate-400/30 border rounded-lg transition-all">
        <IconRefresh class="w-4 h-4" @click="refreshData" />
      </button>
    </h2>
    <IndicatorLoading v-if="domains.length === 0" />
    <div
      v-for="domain in domains" :key="domain.id"
      class="px-2 py-2 hover:pl-4 hover:bg-slate-400/30 rounded-lg transition-all cursor-pointer"
      @click="$router.push(`/domain/${domain.id}`)"
    >
      {{ domain.name }}
      <span
        class="text-xs py-0.5 px-1 rounded-md ml-2" :style="{
          backgroundColor: providerConfig[domain.provider].bandageColor,
          color: providerConfig[domain.provider].bandageTextColor,
        }"
      >{{ providerConfig[domain.provider].displayName }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useToast } from 'vue-toastification'
import { providerConfig } from '@/config'
import { useStore } from '@/store'
import { domainList } from '@/utils/api'

interface Domain {
  id: string
  name: string
  provider: string
  service: string
  status: boolean
}

const toast = useToast()
const store = useStore()

const domains = ref([] as Domain[])

onMounted(() => {
  fetchData()
})

function fetchData() {
  domains.value = []
  domainList(store.token)
    .then(res => res.json())
    .then((data) => {
      if (data.success === true)
        domains.value = data.data
      else toast.error(data.msg)
    })
    .catch(err => toast.error(err.message))
}

function refreshData() {
  domains.value = []
  domainList(store.token, true)
    .then(res => res.json())
    .then((data) => {
      if (data.success === true)
        domains.value = data.data
      else toast.error(data.msg)
    })
    .catch(err => toast.error(err.message))
}
</script>
