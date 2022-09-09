<script setup lang="ts">
import { ref } from 'vue'
import 'vue-select/dist/vue-select.css'

const fgtsStatus = ref("Running on 192.168.0.1")
const ndsStatus = ref("Connected")

const selectedMode = ref(null)
const selectedPkmnId = ref(null)
const isTransferPending = ref(false)
const transferProgress = ref(0)

const transferModes = [
  { mode: { pf: 'nds-gts', gen: 4 }, desc : "NDS (Gen 4) to GTS" },
  { mode: { pf: 'gts-nds', gen: 4 }, desc : "GTS to NDS (Gen 4)" },
]

// dummy pkmns
const bulbasaur = {
  id: '7885443d-d724-480e-81b2-06607d19e211',
  index: 1,
  shiny: true,
  name: "BULBIZARRE", // sprite: https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/1.png
  level: 25,
  holding: "Master Ball", // sprite: https://pokeapi.co/media/sprites/items/master-ball.png
  nature: "Timid",
  ability: "",
  hiddenPower: {
    powerType: "dark-type",
    basePower: 42
  },
  moves: [
    { name: "Tackle", type: "normal-type", category: "physical" },
    { name: "Growl", type: "normal-type", category: "status" },
    { name: "Vine Whip", type: "grass-type", category: "physical" },
    { name: "Leech Seed", type: "grass-type", category: "status" },
  ],
  happiness: 200,
  ot: "B",
  tid: "000000",
  sid: "000000",
  ivs: { hp: 31, atk: 31, def: 31, spa: 31, spd: 31, spe: 31 },
  evs: { hp: 252, atk: 0, def: 0, spa: 252, spd: 0, spe: 0 },
}

const charmander = {
  id: 'abacd6f8-6aad-433b-b8e2-a6e9bec053ef',
  index: 4,
  shiny: false,
  name: "SALAMECHE", // sprite: https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png
  level: 100,
  holding: "Potion", // sprite: https://pokeapi.co/media/sprites/items/potion.png
  nature: "Adamant",
  ability: "",
  hiddenPower: {
    powerType: "dark-type",
    basePower: 42
  },
  moves: [
    { name: "Flammeche", type: "fire-type", category: "special" },
    { name: "Charge", type: "electric-type", category: "physical" },
    { name: "Lance-Flammes", type: "fire-type", category: "special" },
    { name: "Griffe", type: "normal-type", category: "physical" },
  ],
  happiness: 200,
  ot: "B",
  tid: "000000",
  sid: "000000",
  ivs: { hp: 31, atk: 31, def: 31, spa: 31, spd: 31, spe: 31 },
  evs: { hp: 252, atk: 0, def: 0, spa: 252, spd: 0, spe: 0 },
}

const transferablePkmns = ref([bulbasaur, charmander])

const transferPokemon = () => {
  isTransferPending.value = true
  setTimeout(() => {
    isTransferPending.value = false
  }, 5000)
}

const canTransfer = () => {
  return (!selectedMode.value
  || (!selectedPkmnId.value && selectedMode?.value.pf === 'gts-nds') 
  || !fgtsStatus.value
  || !ndsStatus.value
  || isTransferPending.value)
}

const selectedPkmn = () => {
  return transferablePkmns.value.find(p => p.id === selectedPkmnId.value)
}

const getPokemonSprite = () => {
  if (!selectedPkmnId || !transferablePkmns) return

  const p = selectedPkmn()
  return `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${p.shiny ? 'shiny/' : ''}${p.index}.png`
}

</script>

<template>

<div class="main-grid">
  <div class="fgts-status">
    <LvBadge color="info">GTS Status: {{fgtsStatus}}</LvBadge>
  </div>
  <div class="nds-status">
    <LvBadge color="info">NDS Status: {{ndsStatus}}</LvBadge>
  </div>
  
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

  <!-- add v-if ?
    divs must be visible when:
     - A "Pokemon to Transfer" is selected, when "GTS to ..." is selected
     OR
     - A Pokemon has been received/stored in the GTS DB
  -->
  <div v-show="selectedPkmnId" class="pkmn-object-nature-icon">
    <img v-if="selectedPkmnId" :src="getPokemonSprite()"/>
    <!-- add nature, gender, shiny-status?, object -->
  </div>
  <div v-show="selectedPkmnId" class="name-index-level">
    <div class="pkmn-name">Name: {{selectedPkmn()?.name}}</div>
    <div class="pkmn-index">Index: {{selectedPkmn()?.index}}</div>
    <div class="pkmn-level">Level: {{selectedPkmn()?.level}}</div>
  </div>
  <div v-show="selectedPkmnId" class="ability-hiddenpower-happiness">
    <div class="pkmn-ability">ability: {{selectedPkmn()?.ability}}</div>
    <div class="pkmn-hiddenpower">hiddenpower: {{[selectedPkmn()?.hiddenPower.powerType, selectedPkmn()?.hiddenPower.basePower]}}</div>
    <div class="pkmn-level">happiness: {{selectedPkmn()?.happiness}}</div>
  </div>
  <div v-show="selectedPkmnId" class="ot-tid-sid">
    <div class="pkmn-ot">Original Trainer: {{selectedPkmn()?.ot}}</div>
    <div class="pkmn-tid">Trainer ID: {{selectedPkmn()?.tid}}</div>
    <div class="pkmn-sid">Secret ID: {{selectedPkmn()?.sid}}</div>
  </div>
  <div v-show="selectedPkmnId" class="attacks">
    <div class="pkmn-moves">Moves: {{selectedPkmn()?.moves}}</div>
  </div>
  <div v-show="selectedPkmnId" class="nckbl ivs">
    ivs
  </div>
  <div v-show="selectedPkmnId" class="nckbl evs">
    evs
  </div>
</div>

</template>

<style scoped>

.ckbl {
  background: blue;
}

.nckbl {
  background: orange;
}

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
.pkmn-object-nature-icon { grid-area: 7 / 2 / 10 / 5; }
.name-index-level { grid-area: 7 / 6 / 10 / 10; }
.ability-hiddenpower-happiness { grid-area: 7 / 11 / 10 / 15; }
.ot-tid-sid { grid-area: 7 / 16 / 10 / 19; }
.attacks { grid-area: 11 / 6 / 14 / 15; }
.ivs { grid-area: 15 / 4 / 22 / 10; }
.evs { grid-area: 15 / 11 / 22 / 17; }

</style>
