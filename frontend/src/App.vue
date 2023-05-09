<template>
  <div class="mx-2 lg:w-[800px] lg:mx-auto border my-4 p-4 shadow-[0_2px_12px_0_rgb(0_0_0_/_20%)] rounded-xl">
    <RouterView />
    <br>
    <div class="text-center border-t pt-4 mt-2">
      OriDNS v{{ appVersion }} | @2023 OriLight
    </div>
  </div>
</template>

<script setup lang="ts">
import { appVersion } from './config'
</script>
