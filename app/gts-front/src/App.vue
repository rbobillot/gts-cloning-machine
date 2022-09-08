<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import { ref } from 'vue'
//import TransferContent from './components/TransferContent.vue'
//import TransferHeader from './components/TransferHeader.vue';
//import TransferMode from './components/TransferMode.vue'
import 'vue-select/dist/vue-select.css'

const selectedMode = ref(null)
const selectedPkmn = ref(null)

const transferModes = [
  { mode: 0, desc: "NDS (Gen 4) to GTS" },
  { mode: 1, desc : "GTS to NDS (Gen 4)" },
]

const transferablePkmns = ref([])

</script>

<template>

<!--
  <div class="transfer-grid">
    <div class="transfer-header">
      <TransferHeader />
    </div>

    <div class="transfer-mode" >
      <TransferMode />
    </div>

    <div class="transfer-content">
      <TransferContent />
    </div>
  </div>
-->

<div class="parent">
  <div class="nckbl fgts-status">fgts-status</div>
  <div class="nckbl nds-status">nds-status</div>
  <div class="nckbl transfer-status">transfer-status</div>
  
  <!--<div class="nckbl transfer-mode">transfer-mode</div>-->
  <div class="transfer-mode">
    Transfer Mode: 
    <v-select
      v-model="selectedMode"
      :options="transferModes"
      placeholder="Select a transfer mode"
      label="desc"
      ></v-select>
  </div>
  <button class="ckbl start-transfer">start-transfer</button>
  <!-- add v-if option:
    if must be either "pkmn-to-transfer" or "pokemon-received"
   -->
  <div class="pkmn-to-transfer">
    Pokemon to Transfer: 
    <v-select
      v-model="selectedPkmn"
      :options="transferablePkmns"
      placeholder="Select a Pokemon to transfer"
      label="desc"
      ></v-select>
  </div>

  <!-- add v-if ?
    divs must be visible when:
     - A "Pokemon to Transfer" is selected, when "GTS to ..." is selected
     OR
     - A Pokemon has been received/stored in the GTS DB
  -->
  <div class="nckbl pkmn-object-nature-icon">pkmn-object-nature-icon</div>
  <div class="nckbl name-index-level">name-index-level</div>
  <div class="nckbl ability-hiddenpower-happiness">ability-hiddenpower-happiness</div>
  <div class="nckbl ot-tid-sid">ot-tid-sid</div>
  <div class="nckbl attacks">attacks</div>
  <div class="nckbl ivs">ivs</div>
  <div class="nckbl evs">evs</div>
</div>

</template>

<style scoped>

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

/*.transfer-grid {
  display: grid;
  grid-template-columns: repeat(19, 1fr);
  grid-template-rows: repeat(22, 1fr);
  grid-gap: 0px;
}

.transfer-header {
  display: grid;
  grid-column: auto;
  grid-row: auto;
}

.transfer-mode {
  grid-column: auto;
  grid-row: auto;
}

.transfer-content {
  grid-column: auto;
  grid-row: auto;
}*/

.ckbl {
  background: blue;
}

.nckbl {
  background: orange;
}

.parent {
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
