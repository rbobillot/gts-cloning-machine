<script setup lang="ts">
import axios from 'axios';
import 'vue-select/dist/vue-select.css';
import { useEventManagerStore } from '../stores/eventManagerStore'
import { useFlatpassStore } from '../stores/flatpassStore';
import { useTransferStore } from '../stores/transferStore';

const emStore = useEventManagerStore()
const fpStore = useFlatpassStore()
const tStore = useTransferStore()

const gtsServiceUrl = (endpoint: string) => {
  return `http://localhost:8081/${endpoint}`
}

const transferModes = [
  { mode: { pf: 'nds-gts', gen: 4 }, desc: "NDS (Gen 4) to GTS" },
  { mode: { pf: 'gts-nds', gen: 4 }, desc: "GTS to NDS (Gen 4)" },
  // { mode: { pf: 'nds-gts', gen: 5 }, desc: "NDS (Gen 5) to GTS" },
  // { mode: { pf: 'gts-nds', gen: 5 }, desc: "GTS to NDS (Gen 5)" },
]

const transferablesSortByOptions = [
  { value: 'name', label: 'Name' },
  { value: 'index', label: 'Index' },
  { value: 'level', label: 'Level' },
]

const transferPokemon = () => {
  tStore.setTransferPending(true)

  // removing optionLabelName prop from selectedPkmn
  // optionLabelName is only used by lv-dropdown to display the selected option
  // if tStore.selectedPkmn = {}, then pkm = {}
  const { ['optionLabelName']: _, ...pkm } = tStore.selectedPkmn

  const pf = tStore.selectedMode?.pf
  const gen = tStore.selectedMode?.gen

  axios
    .post(gtsServiceUrl(`flatpass/transfer?transfer_platform=${pf}&gen=${gen}`), pkm)
    .then((response) => {
      console.log(response)
    })
    .catch((error) => {
      tStore.setTransferPending(false)
      console.log(error)
    })

    /*{
      // TODO: update gts-service to accept a more complex request (and update database of course)

      .post(gtsServiceUrl('flatpass/transfer', {
        id: tStore.transferId // not sure of the transferId generation yet
        date: new Date().toISOString(),
        platform: tStore.selectedMode?.pf,
        gen: tStore.selectedMode?.gen,
        pkm: pkm
      }
    */
}

const canTransfer = () => {
  return (!fpStore.isFgtsRunnig // || !fpStore.isNdsConnected) ? false : true
  || !tStore.selectedMode
  || (!tStore.selectedPkmnId && tStore.isGtsToNds) 
  || tStore.isTransferPending)
}

const pkmsOrder = (a, b) => {
  if (tStore.transferableSortBy === 'level')
    return a.level - b.level
  else if (tStore.transferableSortBy === 'index')
    return a.index - b.index
  else
    return a.name.localeCompare(b.name)
}

// Fetch all transferable Pokemon from gts-service, and update transferablePkmns moves info
const fetchTransferablePkmns = () => {
  axios.get(gtsServiceUrl('pokemon'))
    .then(response => {
      tStore.setTransferablePkmns(
        response
          .data
          .sort((a, b) => pkmsOrder(a, b))
          .map(pkm => {
            return {
              ...pkm,
              optionLabelName: `${pkm.name} (dex#${pkm.index}, lvl. ${pkm.level})`,
            }
          })
      )
    })
    .catch(error => {
      console.log('cannot fetch transferable pkmns', error)
    })
}

fetchTransferablePkmns()

/* TODO: fetch pending transfers, when gts-service will support it

  const fetchPendingTransfers = () => {
    axios.get(gtsServiceUrl('flatpass/transfer/status'))
      .then(response => {
        tStore.setPendingTransfers(response.data.status)
        tStore.setSelectedMode(response.data.mode)
        tStore.setSelectedPkmn(response.data.selectedPkm)
      })
      .catch(error => {
        console.log('cannot fetch pending transfers', error)
      })
  }

  fetchPendingTransfer()
*/

emStore.getFrontSocket.on('flatpass-transfer', (datastr: string) => {
  const data = JSON.parse(datastr) // TODO: handle data as object, rather than string

  if (!data.status) return

  // const platform = data.platform.toLowerCase()

  if (data.status === "success") {
    tStore.setTransferPending(false)
  } else if (data.status === "error") {
    tStore.setTransferPending(false)
  }
})

</script>

<template>

  <!-- Tranfers options -->
  <div class="transfer-mode" width="100%">
    <lv-dropdown
      v-model="tStore.transferMode"
      iconRight="light-icon-chevron-down"
      optionLabel="desc"
      optionValue="mode"
      placeholder="Select a Transfer Mode"
      :value="tStore.transferMode"
      :options="transferModes"
      :rounded="true"
      :disabled="tStore.isTransferPending"
      />
  </div>
  <div class="start-transfer">
    <lv-button
      v-show="!tStore.isTransferPending"
      :disabled="canTransfer()"
      :rounded="true"
      size="lg"
      @click="transferPokemon()"
      label="Start Transfer"
      />
    <LvLoader v-show="tStore.isTransferPending" type="line-scale" :scale="2" color="grey" />
  </div>
  <div class="pkmn-to-transfer">
    <LvDropdown v-show="tStore.isGtsToNds"
      iconRight="light-icon-chevron-down"
      v-model="tStore.pokemonId"
      optionLabel="optionLabelName"
      optionValue="id"
      placeholder="Select a Pokemon to transfer"
      :value="tStore.pokemonId"
      :options="tStore.transferablePkmns"
      :rounded="true"
      :disabled="tStore.isTransferPending"
      scrollHeight="350px"
      @before-show="fetchTransferablePkmns()"
      />
  </div>
  <div class="transferable-sort-by">
    <LvDropdown v-show="tStore.isGtsToNds"
      iconRight="light-icon-chevron-down"
      v-model="tStore.transferableSortBy"
      optionLabel="label"
      optionValue="value"
      placeholder="Sort by"
      iconLeft="light-icon-sort-descending"
      :value="tStore.transferableSortBy"
      :options="transferablesSortByOptions"
      :rounded="true"
      :disabled="tStore.isTransferPending"
      />
  </div>
</template>

<style scoped>
  
.transfer-mode { grid-area: 3 / 1 / 4 / 7; }
.start-transfer { grid-area: 3 / 8 / 4 / 11; }
.pkmn-to-transfer { grid-area: 3 / 12 / 4 / 18; }
.transferable-sort-by { grid-area: 3 / 19 / 4 / 21; }

.confirmation-content {
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>
