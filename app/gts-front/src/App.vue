<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import TransferMode from './components/TransferMode.vue'
import { ref } from 'vue'
import TransferContent from './components/TransferContent.vue';

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
  <div class="statuses-header status-grid">
    <div class="status-fgts">
      <p>Fake-GTS Status: {{showFgtsStatus()}}</p>
    </div>
    <div class="status-blank"></div>
    <div class="status-nds">
      <p>Nintendo DS Status: {{showNdsStatus()}}</p>
    </div>

    <div class="transfer-mode">
      <TransferMode />
    </div>
    <div class="transfer-blank"></div>
    <div class="transfer-blank"></div>

    <!-- might be split in multiple divs: <pokemon logo> .. <pokemon infos> -->
    <div class="transfer-content">
      <TransferContent />
    </div>
  </div>

</template>

<style scoped>

.statuses-header {
  padding: 1rem;
}

.status-blank, .transfer-blank {
  background-color: burlywood;
  padding: 1rem;
}

.status-nds, .status-fgts {
  background-color: #646cffaa;
  padding: 1rem;
}

.transfer-mode {
  background-color: #42b883aa;
  padding: 1rem;
}

.transfer-content {
  background-color: burlywood;
  padding: 1rem;
}

.status-grid {
  display: grid;
  grid-template-columns: 1fr 4fr 1fr;
  grid-template-rows: 1fr 1fr 3fr;
  grid-gap: 1%;
}

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
