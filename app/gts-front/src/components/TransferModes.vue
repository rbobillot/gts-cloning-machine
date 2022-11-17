<script setup lang="ts">
import axios from 'axios';
import 'vue-select/dist/vue-select.css';
import { useEventManagerStore } from '../stores/eventManagerStore'
import { useTransferStore } from '../stores/transferStore';

const emStore = useEventManagerStore()
const tStore = useTransferStore()

const gtsServiceUrl = (endpoint: string) => {
  return `http://localhost:8081/${endpoint}`
}

const transferModes = [
  { mode: { pf: 'nds-gts', gen: 4 }, desc: "NDS (Gen 4) to GTS" },
  { mode: { pf: 'nds-gts', gen: 5 }, desc: "NDS (Gen 5) to GTS" },
  { mode: { pf: 'gts-nds', gen: 4 }, desc: "GTS to NDS (Gen 4)" },
  { mode: { pf: 'gts-nds', gen: 5 }, desc: "GTS to NDS (Gen 5)" },
]

const transferablesSortByOptions = [
  { value: 'name', label: 'Name' },
  { value: 'index', label: 'Index' },
  { value: 'level', label: 'Level' },
]

const transferPokemon = () => {
  tStore.setTransferPending(true)

  const { ['optionLabelName']: _, ...pkm } = tStore.selectedPkmn

  const pf = tStore.selectedMode?.pf
  const gen = tStore.selectedMode?.gen

  axios
    .post(gtsServiceUrl(`flatpass/transfer?transfer_platform=${pf}&gen=${gen}`), pkm)
    .then((response) => {
      // console.log(response)
    })
    .catch((error) => {
      tStore.setTransferPending(false)
      console.log(error)
    })

  // TODO: update gts-service to accept a more complex request: {id, date, pkm}
}

const pokemonOrdering = (px, py) => {
  if (tStore.transferableSortBy === 'level')
    return px.level - py.level
  else if (tStore.transferableSortBy === 'index')
    return px.index - py.index
  else
    return px.name.localeCompare(py.name)
}

const fetchAndUpdateTransferablePkmns = () => {
  return axios.get(gtsServiceUrl('pokemon'))
    .then(response => {
      tStore.setTransferablePkmns(
        response
          .data
          .sort(pokemonOrdering)
          .map(pkm => {
            return {
              ...pkm,
              optionLabelName: `${pkm.name} (dex #${pkm.index}, lvl. ${pkm.level})`,
            }
          })
      )
    })
    .catch(error => {
      console.log('cannot fetch transferable pkmns', error)
    })
}

fetchAndUpdateTransferablePkmns()

// TODO: handle pending transfers fetch ?

emStore.getFrontSocket.on('flatpass-transfer', (datastr: string) => {
  const data = JSON.parse(datastr) // TODO: handle data as object, rather than string

  if (data.status?.endsWith("success")) {
    fetchAndUpdateTransferablePkmns().then(() => {
      tStore.setTransferPending(false)
      if (data.status === "create-success") {
        const pkmn = tStore.transferablePkmns.find(p => p.raw_pkm_data === data.details)
        tStore.setReceivedPkmn(pkmn)
      }
    })
  } else if (["error", "failure"].includes(data.status?.toLocaleLowerCase())) {
    tStore.setTransferPending(false)
  }
})

</script>

<template>

  <!-- Tranfers options -->
  <div class="transfer-mode" width="100%">
    <lv-dropdown
      class="transfer-mode-dropdown"
      v-model="tStore.transferMode"
      iconRight="light-icon-chevron-down"
      optionLabel="desc"
      optionValue="mode"
      placeholder="Select a Transfer Mode"
      :value="tStore.transferMode"
      :options="transferModes"
      :rounded="true"
      :disabled="tStore.isTransferPending"
      @before-hide="tStore.resetSelectedPkmn()"
      />
  </div>
  <div class="start-transfer">
    <lv-button v-if="!tStore.isTransferPending"
      class="start-transfer-button"
      :disabled="tStore.isTransferDisabled"
      :rounded="true"
      size="lg"
      @click="transferPokemon()"
      label="Transfer"
      />
    <LvLoader v-else
      class="start-transfer-loader"
      type="line-scale"
      :disabled="tStore.isTransferDisabled"
      :scale="2"
      color="grey" />
  </div>
  <div class="pkmn-to-transfer">
    <LvDropdown v-show="tStore.isGtsToNds"
      class="pkmn-to-transfer-dropdown"
      v-model="tStore.pokemonId"
      iconRight="light-icon-chevron-down"
      optionLabel="optionLabelName"
      optionValue="id"
      placeholder="Select a Pokemon to transfer"
      :value="tStore.pokemonId"
      :options="tStore.transferablePkmns"
      :rounded="true"
      :disabled="tStore.isTransferPending"
      :clearable="true"
      />
      <!-- scrollHeight="350px" creates warning during tests -->
    </div>
  <div class="transferable-sort-by">
    <LvDropdown v-show="tStore.isGtsToNds"
      class="transferable-sort-by-dropdown"
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
      @before-hide="tStore.sortTransferablePokemons()"
      />
  </div>
</template>

<style scoped>
  
.transfer-mode { grid-area: 3 / 1 / 4 / 7; }
.start-transfer { grid-area: 3 / 8 / 4 / 9; }
.pkmn-to-transfer { grid-area: 3 / 10 / 4 / 16; }
.transferable-sort-by { grid-area: 3 / 17 / 4 / 19; }

.confirmation-content {
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>
