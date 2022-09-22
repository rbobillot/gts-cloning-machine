<!-- USELESS FOR NOW -->
<script setup lang="ts">
import { ref } from 'vue'

const fgtsStatus = ref({running: false, host: ""})
const ndsStatus = ref({connected: false})

const showFgtsStatus = () => {
  if (fgtsStatus.value.running) {
    return "Running on " + fgtsStatus.value.host
  } else {
    return "Not running"
  }
}

const showNdsStatus = () => {
  if (ndsStatus.value.connected) {
    return "Connected"
  } else {
    return "Not connected"
  }
}

</script>

<template>

  <div class="fgts-status">
    GTS Status: {{showFgtsStatus()}}
  </div>

  <div class="transfer-status">
    Transfer
  </div>

  <div class="nds-status">
    NDS Status: {{showNdsStatus()}}
  </div>

</template>

<style scoped>

.fgts-status {
  grid-column: 2 / 3;
  grid-row: 2 / 3;
}

.transfer-status {
  grid-column: 5 / 15;
  grid-row: 2 / 3;
}

.nds-status {
  grid-column: 17 / 18;
  grid-row: 2 / 3;
}

</style>
