<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useEventManagerStore } from '../stores/eventManagerStore'
import { useFlatpassStore } from '../stores/flatpassStore'
import { useTransferStore } from '../stores/transferStore';

const emStore = useEventManagerStore()
const fpStore = useFlatpassStore()
const tStore = useTransferStore()

const gtsServiceUrl = (endpoint: string) => {
  return `http://localhost:8081/${endpoint}`
}

const updateFlatpassStatus = (data: any) => {
  const connection_details: any = data.connection_details
  const isRunning: boolean = data.status?.toLowerCase() === "running"
  const status: string = `${!isRunning ? "Not Running" : `Running on ${connection_details?.host}`}`

  fpStore.setFgtsStatus({ isRunning, status })

  if (!isRunning) tStore.setTransferPending(false)
}

const updateNdsStatus = (data: any) => {
  const isConnected = data.status?.toLowerCase() === "connected"
  const status = isConnected ? "Connected" : "Not Connected"

  fpStore.setNdsStatus({ isConnected, status })

  if (!isConnected) tStore.setTransferPending(false)
}

const fetchAndUpdateFlatpassStatus = () => {
  axios.get(gtsServiceUrl('flatpass/status?platform=flatpass'))
    .then(response => {
      updateFlatpassStatus(response.data)
    })
    .catch(error => {
      console.log(error)
    })
}

fetchAndUpdateFlatpassStatus()

emStore.getFrontSocket.on('flatpass-status', (datastr: string) => {
  const data = JSON.parse(datastr) // TODO: handle data as object, rather than string

  if (!data.platform) return

  const platform = data.platform.toLowerCase()

  if (data.platform.toLowerCase() === 'nds') updateNdsStatus(data)
  else if (platform === 'flatpass') updateFlatpassStatus(data)
})

</script>

<template>

<div class="fgts-status">
  <LvBadge :color="fpStore.isFgtsRunnig ? 'info' : 'danger'">
    GTS Status: {{fpStore.fgtsStatus?.status}}
  </LvBadge>
</div>
<div class="nds-status">
  <LvBadge v-if="fpStore.isNdsConnected"
    :color="fpStore.isNdsConnected ? 'info' : 'danger'"
    >NDS Status: {{fpStore.ndsStatus?.status}}</LvBadge>
</div>

</template>

<style scoped>

.fgts-status { grid-area: 1 / 1 / 2 / 7; }
.nds-status { grid-area: 1 / 14 / 2 / 19; }
/*.transfer-status { grid-area: 1 / 5 / 3 / 16; }*/

</style>
