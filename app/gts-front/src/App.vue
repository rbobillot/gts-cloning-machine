<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios';
import 'vue-select/dist/vue-select.css'

const fgtsStatus = ref({isRunning: false, status: "Not Running"}) // ref("Running on 192.168.0.1") --> handle with SocketIO ?
const ndsStatus = ref({isConnected: false, status: "Not Connected"}) // ref("Connected") --> handle with SocketIO ?

const transferModes = [
  { mode: { pf: 'nds-gts', gen: 4 }, desc : "NDS (Gen 4) to GTS" },
  { mode: { pf: 'gts-nds', gen: 4 }, desc : "GTS to NDS (Gen 4)" },
]
const selectedMode = ref(null)

const selectedPkmnId = ref(null)

const isTransferPending = ref(false)
const transferProgress = ref(0)

const receivedPkmn = ref(null)

// TODO: remove dummy pkmns, and call them through API
const arceus = {
  "id": "d02e1805-7920-4b58-809f-e85b7d13efd8",
  "checksum": "0x3fd4",
  "name": "ARCEUS",
  "index": 493,
  "holding": "rare-candy",
  "shiny": true,
  "level": 80,
  "happiness": 70,
  "nature": "Adamant",
  "species": "Arceus",
  "ability": "Multitype",
  "gender": "Genderless",
  "ot": "B",
  "tid": 39771,
  "sid": 39765,
  "hidden_power": {
    "power_type": "Electric",
    "base_power": 63
  },
  "moves": [
    "Refresh",
    "Future Sight",
    "Recover",
    "Hyper Beam"
  ],
  "ivs": {
    "hp": 25,
    "atk": 25,
    "def": 31,
    "spa": 9,
    "spd": 2,
    "spe": 27
  },
  "evs": {
    "hp": 0,
    "atk": 0,
    "def": 0,
    "spa": 0,
    "spd": 0,
    "spe": 0,
    "total": 0
  },
  "original_language": "Français (France/Québec)",
  "modified_fields": [],
  "raw_pkm_data": "tpe4lwAAP9TtATIAW5tVmwDECQBGeQADAAAAAAAAAAAAAAAAAAAAAB8B+ABpAD8AFA8KBQAAAAA5/50EAAAAAAQAAAAAAFYAKwE8AS0BLwE/AT0B//8AAAAAAAAAAAAMAAAAAAAAAAAsAf//AAAAAAAAAAAAAAAAAAAACQUcAABWAAABUAUAAAAAAABQAC4BLgHuAN0A2gC3AMYAAAAAAAADCv//////////////////////////////VwH//1AB////////OAH///////8vAf////8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM="
}

const giratina = {
  "id": "296d5246-9da6-44b5-b308-bce361a7d4d1",
  "checksum": "0xa3dd",
  "name": "GIRATINA",
  "index": 487,
  "holding": "rare-candy",
  "shiny": true,
  "level": 47,
  "happiness": 71,
  "nature": "Relaxed",
  "species": "Giratina",
  "ability": "Pressure",
  "gender": "Genderless",
  "ot": "B",
  "tid": 39771,
  "sid": 39765,
  "hidden_power": {
    "power_type": "Psychic",
    "base_power": 42
  },
  "moves": [
    "Ominous Wind",
    "AncientPower",
    "Dragon Claw",
    "Shadow Force"
  ],
  "ivs": {
    "hp": 27,
    "atk": 10,
    "def": 29,
    "spa": 28,
    "spd": 23,
    "spe": 25
  },
  "evs": {
    "hp": 0,
    "atk": 0,
    "def": 0,
    "spa": 0,
    "spd": 0,
    "spe": 0,
    "total": 0
  },
  "original_language": "Français (France/Québec)",
  "modified_fields": [],
  "raw_pkm_data": "VCdaJwAAo93nATIAW5tVm/L6AQBHLgADAAAAAAAAAAAAAAAAAAAAANIB9gBRAdMBBQUPBQAAAABb9cwvAAAAAAQAAAAAAD4AMQEzATwBKwE+ATMBOAErAf//AAAAAAAMAAAAAAAAAAAsAf//AAAAAAAAAAAAAAAAAAAACQEdAAA+AAABLwUAAAAAAAAvANIA0gBnAJAAWgBwAIAAAAAAAAADCv//////////////////////////////VwH//1AB////////OAH///////8vAf////8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM="
}

const transferablePkmns = ref([arceus, giratina])

const transferPokemon = () => {
  isTransferPending.value = true
  setTimeout(() => {
    isTransferPending.value = false
  }, 5000)
}

const canTransfer = () => {
  return (!fgtsStatus.value.isRunning || !ndsStatus.value.isConnected
  || !selectedMode.value
  || (!selectedPkmnId.value && selectedMode?.value.pf === 'gts-nds') 
  || isTransferPending.value)
}

const selectedPkmn = () => {
  return transferablePkmns.value.find(p => p.id === selectedPkmnId.value)
}

const getPokemonSprite = () => {
  if (!selectedPkmnId || !transferablePkmns) return

  const p = selectedPkmn()
  if (!p) return
  return `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${p.shiny ? 'shiny/' : ''}${p.index}.png`
}

/**
 * Display Pokemon infos when:
 * - A "Pokemon to Transfer" is selected, when "GTS to ..." is selected
 * OR
 * - A Pokemon has been received/stored in the GTS DB
 */
const shouldDisplayPkmn = () => {
  return (selectedMode.value && selectedMode.value.pf === 'gts-nds' && selectedPkmnId.value) || receivedPkmn.value
}

/* TODO: handle Pokemon moves correctly (colored divs depending on type, and logo depending on damage class)
const updateMoveInfo = (move: string, index: number) => {
  axios
  .get(`https://pokeapi.co/api/v2/move/${move.toLocaleLowerCase().replace(' ', '-')}`)
  .then((moveResp) => {
    selectedPkmnMoves.value.splice(index, 1, {
      index: index,
      name: move,
      damage_class: moveResp.data.damage_class.name,
      type: moveResp.data.type.name,
      // name_fr: moveResp.data.names.find((n: any) => n.language.name === 'fr').name,
    })
  })
}
*/

</script>

<template>

<!-- Terminals infos -->
<div class="main-grid">
  <div class="fgts-status">
    <LvBadge :color="fgtsStatus.isRunning ? 'info' : 'danger'">GTS Status: {{fgtsStatus.status}}</LvBadge>
  </div>
  <div class="nds-status">
    <LvBadge :color="ndsStatus.isConnected ? 'info' : 'danger'">NDS Status: {{ndsStatus.status}}</LvBadge>
  </div>
  
  <!-- Tranfers options -->
  <div class="transfer-mode">
    <lv-dropdown
      v-model="selectedMode"
      optionLabel="desc"
      optionValue="mode"
      placeholder="Select a Transfer Mode"
      icon-right="light-icon-arrow-down-circle"
      :value="selectedMode"
      :options="transferModes"
      :rounded="true"
      :disabled="isTransferPending"
      />
  </div>
  <div class="start-transfer">
    <lv-button
      v-show="!isTransferPending"
      :disabled="canTransfer()"
      :rounded="true"
      @click="transferPokemon"
      label="Start Transfer"
      />
    <LvLoader v-show="isTransferPending" type="line-scale" :scale="2" color="grey" />
  </div>
  <div class="pkmn-to-transfer">
    <lv-dropdown v-show="selectedMode?.pf === 'gts-nds'"
      v-model="selectedPkmnId"
      optionLabel="name"
      optionValue="id"
      placeholder="Select a Pokemon to transfer"
      icon-right="light-icon-arrow-down-circle"
      :value="selectedPkmnId"
      :options="transferablePkmns"
      :rounded="true"
      :disabled="isTransferPending"
      />
  </div>

  <!-- Pokemon basic info props -->
  <div v-if="shouldDisplayPkmn()" class="pkmn-object-nature-icon">
    <div class="pkmn-sprite" width="96" height="96">
      <img :src="getPokemonSprite()" />
    </div>
    <div class="pkmn-shiny-star">
    <svg v-if="selectedPkmn()?.shiny" width="20" height="20" style="color: red" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 16">
        <path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288L8 2.223l1.847 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.565.565 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z" fill="red" />
    </svg>
    </div>
    <div class="pkmn-held-item">
      <img :src="`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/${selectedPkmn()?.holding}.png`" />
    </div>
    <div class="pkmn-name">
      {{selectedPkmn()?.name}}
    </div>
  </div>
  <div v-if="shouldDisplayPkmn()" class="pkm-stats index-level-nature">
    <div class="pkm-stat pkmn-index"><div class="pkm-stat-title">National Index</div><div class="pkm-stat-value">{{selectedPkmn()?.index}}</div></div>
    <div class="pkm-stat pkmn-level"><div class="pkm-stat-title">Level</div><div class="pkm-stat-value">{{selectedPkmn()?.level}}</div></div>
    <div class="pkm-stat pkmn-nature"><div class="pkm-stat-title">Nature</div><div class="pkm-stat-value">{{selectedPkmn()?.nature}}</div></div>
  </div>
  <div v-if="shouldDisplayPkmn()" class="pkm-stats ability-hiddenpower-happiness">
    <div class="pkm-stat pkmn-ability"><div class="pkm-stat-title">Ability</div><div class="pkm-stat-value">{{selectedPkmn()?.ability}}</div></div>
    <div class="pkm-stat pkmn-hiddenpower"><div class="pkm-stat-title">Hidden Power</div><div class="pkm-stat-value">{{selectedPkmn()?.hidden_power.base_power}} ({{selectedPkmn()?.hidden_power.power_type}})</div></div>
    <div class="pkm-stat pkmn-happiness"><div class="pkm-stat-title">Happiness</div><div class="pkm-stat-value">{{selectedPkmn()?.happiness}}</div></div>
  </div>
  <div v-if="shouldDisplayPkmn()" class="pkm-stats ot-tid-sid">
    <div class="pkm-stat pkmn-ot"><div class="pkm-stat-title">Original Trainer</div><div class="pkm-stat-value">{{selectedPkmn()?.ot}}</div></div>
    <div class="pkm-stat pkmn-tid"><div class="pkm-stat-title">Trainer ID</div><div class="pkm-stat-value">{{selectedPkmn()?.tid}}</div></div>
    <div class="pkm-stat pkmn-sid"><div class="pkm-stat-title">Secret ID</div><div class="pkm-stat-value">{{selectedPkmn()?.sid}}</div></div>
  </div>
  <div v-if="shouldDisplayPkmn()" class="pkmn-moves">
    <LvBadge color="secondary" class="pkmn-move-1">{{selectedPkmn()?.moves[0]}}</LvBadge>
    <LvBadge color="secondary" class="pkmn-move-2">{{selectedPkmn()?.moves[1]}}</LvBadge>
    <LvBadge color="secondary" class="pkmn-move-3">{{selectedPkmn()?.moves[2]}}</LvBadge>
    <LvBadge color="secondary" class="pkmn-move-4">{{selectedPkmn()?.moves[3]}}</LvBadge>
  </div>

  <!-- Pokemon IVs / EVs props -->
  <div v-if="shouldDisplayPkmn()" class="ivs">
    <div class="ivs-title">IVs</div>
    <div v-for="(iv, key) in selectedPkmn()?.ivs" class="iv-line" :key="key">
      <div>{{key}}</div>
      <LvSlider :value="iv" :min="0" :max="31" :step="1" :disabled="true" sliderColor="#9973ff" />
      <div>{{iv}}</div>
    </div>
  </div>
  <div v-if="shouldDisplayPkmn()" class="evs">
    <div class="evs-title">EVs</div>
    <div v-for="(ev, key) in selectedPkmn()?.evs" class="ev-line" :key="key">
      <div>{{key}}</div>
      <LvSlider :value="ev" :min="0" :max="252" :step="1" :disabled="true" sliderColor="#38b2ac" />
      <div>{{ev}}</div>
    </div>
  </div>
</div>

</template>

<style scoped>

.main-grid {
  display: grid;
  grid-template-columns: repeat(19, 1fr);
  grid-template-rows: repeat(22, 1fr);
  grid-column-gap: 0px;
  grid-row-gap: 0px;
}

.fgts-status { grid-area: 2 / 2 / 4 / 4; }
.nds-status { grid-area: 2 / 17 / 4 / 19; }
.transfer-status { grid-area: 2 / 5 / 4 / 16; }
.transfer-mode { grid-area: 5 / 2 / 6 / 8; }
.start-transfer { grid-area: 5 / 9 / 6 / 12; }
.pkmn-to-transfer { grid-area: 5 / 13 / 6 / 19; }

.pkmn-object-nature-icon { 
  display: grid;
  grid-area: 7 / 2 / 10 / 5;
  grid-template-areas:
    "a a a b"
    "a a a c"
    "a a a -"
    "d d d -";
  grid-template: subgrid;
  justify-content: center;
}
.pkmn-sprite { grid-area: a; }
.pkmn-shiny-star { grid-area: b; }
.pkmn-held-item { grid-area: c; }
.pkmn-name { grid-area: d; font-weight: bold; }

.pkm-stats {
  display: grid;
  grid-gap: 1rem;
  align-content: center;
  margin: 1fr;
}
.pkm-stat {
  display: flex;
  justify-content: space-between;
  border: solid lightgray;
  border-width: 1px 0;
  padding-left: 1rem;
  padding-right: 1rem;
}
.pkm-stat-title {
  font-style: italic;
}
.pkm-stat-value {
  font-weight: bold;
}

.index-level-nature {
  grid-area: 7 / 6 / 10 / 10;
  grid-template-areas:
    "a a a"
    "b b b"
    "c c c";
}
.pkmn-index { grid-area: a; }
.pkmn-level { grid-area: b; }
.pkmn-nature { grid-area: c; }

.ability-hiddenpower-happiness { grid-area: 7 / 11 / 10 / 15; }

.ot-tid-sid { grid-area: 7 / 16 / 10 / 19; }

.pkmn-moves {
  display: grid;
  grid-area: 11 / 6 / 14 / 15;
  grid-template-areas:
    "a a a a - b b b b"
    "c c c c - d d d d";
}
.pkmn-move-1 { grid-area: a; }
.pkmn-move-2 { grid-area: b; }
.pkmn-move-3 { grid-area: c; }
.pkmn-move-4 { grid-area: d; }

.ivs { grid-area: 15 / 4 / 22 / 10; }
.iv-line {
  display: grid;
  grid-template-columns: 1fr 4fr 1fr;
  grid-template-rows: 1fr 0.5fr;
  align-items: center;
}
.evs { grid-area: 15 / 11 / 22 / 17; }

.ev-line {
  display: grid;
  grid-template-columns: 1fr 4fr 1fr;
  grid-template-rows: 1fr 0.5fr;
  align-items: center;
}

</style>
