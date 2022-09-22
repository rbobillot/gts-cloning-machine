<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { useFlatpassStore } from '../stores/flatpassStore';

const fpStore = useFlatpassStore()

const gtsServiceUrl = (endpoint: string) => {
  return `http://localhost:8081/${endpoint}`
}

const ndsStatus = ref({isConnected: false, status: "Not Connected"}) // --> handle with SocketIO ?

const fetchFlatpassStatus = () => {
  axios.get(gtsServiceUrl('flatpass-status'))
    .then(response => {
      fpStore.setFgtsStatus(response.data.isRunning ? response.data : {isRunning: false, status: "Not Running"})
    })
    .catch(error => {
      console.log(error)
    })
}

fetchFlatpassStatus() // handle refresh via socket.io, rather than page refresh

</script>

<template>

<div class="fgts-status">
  <LvBadge :color="fpStore.isFgtsRunning ? 'info' : 'danger'" @click="fetchFlatpassStatus()">
    GTS Status: {{fpStore.getFgtsStatus}}
  </LvBadge>
</div>
<div class="nds-status">
  <LvBadge v-if="ndsStatus.isConnected" :color="ndsStatus.isConnected ? 'info' : 'danger'">NDS Status: {{ndsStatus.status}}</LvBadge>
</div>

</template>

<style scoped>

.fgts-status { grid-area: 1 / 1 / 2 / 7; }
.nds-status { grid-area: 1 / 14 / 2 / 19; }
/*.transfer-status { grid-area: 1 / 5 / 3 / 16; }*/

</style>
