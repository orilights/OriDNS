<template>
  <div>
    <button
      class="px-2 py-1 hover:bg-slate-400/30 border border-black/20 rounded-lg transition-all"
      @click="$router.push('/')"
    >
      &lt;返回主页
    </button>
    <h2 class="text-2xl font-bold py-2">
      域名详情
    </h2>
    <IndicatorLoading v-if="domainInfo.id === 'loading'" />
    <div v-if="domainInfo.id !== 'loading'">
      <div class="font-bold text-lg mb-2">
        {{ domainInfo.name }}
      </div>
      <div><span class="font-bold">域名ID：</span>{{ domainInfo.id }}</div>
      <div><span class="font-bold">服务商：</span>{{ domainInfo.provider }}</div>
    </div>
    <h2 class="text-2xl font-bold py-2">
      记录列表
      <button
        class="p-1 mx-1 bg-blue-500 text-white hover:bg-blue-400 border rounded-lg transition-all"
        @click="modalData = newRecordTemplate; showModal = 'create'"
      >
        <IconPlus class="w-4 h-4" />
      </button>
      <button class="p-1 mx-1 hover:bg-slate-400/30 border rounded-lg transition-all">
        <IconRefresh class="w-4 h-4" @click="fetchData" />
      </button>
    </h2>
    <IndicatorLoading v-if="records.length === 0" />
    <div
      v-for="record in records" :key="record.id"
      class="px-2 py-1.5 hover:pl-4 hover:bg-slate-400/30 rounded-lg transition-all relative group flex items-center justify-center"
    >
      <div class="flex-1 overflow-hidden text-ellipsis whitespace-nowrap">
        {{ `${record.type} | ${record.name} | ${record.value}` }}
      </div>
      <div class="hidden group-hover:flex">
        <IconEdit
          class="w-5 h-5 mx-2 cursor-pointer"
          @click="modalData = {
            id: record.id,
            type: record.type,
            name: record.name,
            value: record.value,
            ttl: record.ttl,
          };showModal = 'update'"
        />
        <IconDelete
          class="w-5 h-5 inline mx-2 cursor-pointer"
          @click="modalData = {
            id: record.id,
            type: record.type,
            name: record.name,
            value: record.value,
            ttl: record.ttl,
          }; showModal = 'confirm-delete'"
        />
      </div>
    </div>
    <component :is="modal" :data="modalData" @submit="handleModalSubmit" @close="showModal = null" />
  </div>
</template>

<script setup lang="ts">
import { useToast } from 'vue-toastification'
import DialogRecordCreate from '@/components/Dialog/record/create.vue'
import DialogRecordUpdate from '@/components/Dialog/record/Update.vue'
import DialogRecordConfirmDelete from '@/components/Dialog/record/ConfirmDelete.vue'
import { useStore } from '@/store'
import { domainInfoGet, recordCreate, recordDelete, recordList, recordUpdate } from '@/utils/api'
import { RECORD_TYPES_SORT } from '@/config'

interface DomainInfo {
  id: string
  name: string
  status: string
  created_at: string
  ns: string[]
  provider: string
  c_beian: [-1, 0, 1]
}

interface Record {
  id: string
  name: string
  type: string
  value: string
  ttl: number
  proxied: boolean
  proxiable: boolean
  service: boolean
}
const route = useRoute()
const toast = useToast()
const store = useStore()

const showModal = ref<string | null>(null)
const modal = computed(() => {
  if (showModal.value === null)
    return null
  switch (showModal.value) {
    case 'create':
      return DialogRecordCreate
    case 'update':
      return DialogRecordUpdate
    case 'confirm-delete':
      return DialogRecordConfirmDelete
    default:
      return null
  }
})

watch(modal, () => {
  if (modal.value === null)
    document.body.style.overflowY = ''
  else
    document.body.style.overflowY = 'hidden'
})

const modalData = ref({} as any)
const newRecordTemplate = {
  id: '',
  type: 'TXT',
  name: '',
  value: '',
  ttl: 600,
}
const domainInfo = ref({ id: 'loading' } as DomainInfo)
const records = ref([] as Record[])
const { domain: domainId } = route.params

onMounted(() => {
  domainInfoGet(store.token, String(domainId))
    .then(res => res.json())
    .then((data) => {
      if (data.success === true)
        domainInfo.value = data.data
      else
        toast.error(data.msg)
    })
    .catch(err => toast.error(err.message))
  fetchData()
})

function fetchData() {
  records.value = []
  recordList(store.token, String(domainId))
    .then(res => res.json())
    .then((data) => {
      if (data.success === true) {
        const _rawData: Record[] = data.data
        _rawData.sort((a, b) => {
          if (a.type === b.type)
            return a.name.localeCompare(b.name)
          else
            return RECORD_TYPES_SORT.indexOf(a.type) - RECORD_TYPES_SORT.indexOf(b.type)
        })
        records.value = _rawData
      }
      else { toast.error(data.msg) }
    })
    .catch(err => toast.error(err.message))
}

function handleModalSubmit(modalType: string) {
  if (modalType === 'create')
    handleCreateRecord()
  if (modalType === 'update')
    handleUpdateRecord(modalData.value.id)
  if (modalType === 'confirm-delete')
    handleDeleteRecord(modalData.value.id)
  showModal.value = null
}

function handleCreateRecord() {
  const formData = new FormData()
  formData.append('type', modalData.value.type)
  formData.append('name', modalData.value.name)
  formData.append('value', modalData.value.value)
  formData.append('ttl', String(modalData.value.ttl))
  recordCreate(store.token, String(domainId), formData)
    .then(res => res.json())
    .then((data) => {
      if (data.success === true) {
        toast.success('记录创建成功')
        fetchData()
      }
      else {
        toast.error(data.msg)
      }
    })
    .catch(err => toast.error(err.message))
}

function handleUpdateRecord(recordId: string) {
  const formData = new FormData()
  formData.append('type', modalData.value.type)
  formData.append('name', modalData.value.name)
  formData.append('value', modalData.value.value)
  formData.append('ttl', String(modalData.value.ttl))
  recordUpdate(store.token, String(domainId), recordId, formData)
    .then(res => res.json())
    .then((data) => {
      if (data.success === true) {
        toast.success('记录更新成功')
        fetchData()
      }
      else {
        toast.error(data.msg)
      }
    })
    .catch(err => toast.error(err.message))
}

function handleDeleteRecord(recordId: string) {
  recordDelete(store.token, String(domainId), recordId)
    .then(res => res.json())
    .then((data) => {
      if (data.success === true) {
        toast.success('记录删除成功')
        fetchData()
      }
      else {
        toast.error(data.msg)
      }
    })
    .catch(err => toast.error(err.message))
}
</script>
