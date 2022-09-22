<script setup lang="ts">
import { Ref, ref } from 'vue'
import axios from 'axios';
import 'vue-select/dist/vue-select.css';
import { useFlatpassStore } from '../stores/flatpassStore';
import { useTransferStore } from '../stores/transferStore';

const fpStore = useFlatpassStore()
const tStore = useTransferStore()

const gtsServiceUrl = (endpoint: string) => {
  return `http://localhost:8081/${endpoint}`
}

const transferModes = [
  { mode: { pf: 'nds-gts', gen: 4 }, desc : "NDS (Gen 4) to GTS" },
  { mode: { pf: 'gts-nds', gen: 4 }, desc : "GTS to NDS (Gen 4)" },
]

const transferablesSortByOptions = [
  { value: 'name', label: 'Name' },
  { value: 'index', label: 'Index' },
  { value: 'level', label: 'Level' },
]

const transferNdsToGts = () => {
  axios
    .get(gtsServiceUrl('flatpass-receive'))
    .then((response) => {
      tStore.setTransferPending(false)
      console.log(response)
    })
    .catch((error) => {
      tStore.setTransferPending(false)
      console.log(error)
    })
}

const transferGtsToNds = () => {
  const { ['optionLabelName']: _, ...pkm } = tStore.selectedPkmn // remove optionLabelName prop from selectedPkmn

  axios
    .post(gtsServiceUrl('flatpass-send'), pkm)
    .then((response) => {
      tStore.setTransferPending(false)
      console.log(response)
    })
    .catch((error) => {
      tStore.setTransferPending(false)
      console.log(error)
    })
}

const transferPokemon = () => {
  // dummy transfer pending
  tStore.setTransferPending(true)
  setTimeout(() => {
    tStore.setTransferPending(false)
  }, 1000)
  if (tStore.selectedMode.pf === 'nds-gts') {
    transferNdsToGts()
  } else if (tStore.selectedMode.pf === 'gts-nds') {
    transferGtsToNds()
  }
}

const canTransfer = () => {
  return (!fpStore.isFgtsRunning
  // || !ndsStatus.value.isConnected
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
