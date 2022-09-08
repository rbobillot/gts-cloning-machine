<!-- USELESS FOR NOW -->
<script setup lang="ts">
import { ref } from 'vue'
import 'vue-select/dist/vue-select.css';

//defineProps<{ msg: string }>()

const selectedMode = ref(null)

const transferModes = [
  { mode: 0, desc: "NDS (Gen 4) to GTS" },
  { mode: 1, desc : "GTS to NDS (Gen 4)" },
]

</script>

<template>

  <div id="modes-selector" class="transfer-mode">
    <h2>Transfer Mode: </h2>
    <v-select
      v-model="selectedMode"
      :options="transferModes"
      placeholder="Select a transfer mode"
      label="desc"
      ></v-select>
  </div>

  <div class="start-transfer">
    <button class="submit">Start Transfer</button>
  </div>

  <div class="pokemon-to-transfer">
    <p>Selected Mode: {{selectedMode}}</p>
  </div>

</template>

<style scoped>
.read-the-docs {
  color: #888;
}

body {
  font-family: 'Source Sans Pro', 'Helvetica Neue', Arial, sans-serif;
}

h2 {
  font-size: 26px;
  font-weight: 600;
  color: #2c3e5099;
  text-rendering: optimizelegibility;
  -moz-osx-font-smoothing: grayscale;
  -moz-text-size-adjust: none;
}

#modes-selector {
  max-width: 30em;
  margin: 1em auto;
}

.transfer-mode {
  grid-column: 2 / 7;
  grid-row: 5;
}

.start-transfer {
  grid-column: 9 / 11;
  grid-row: 5;
}

.pokemon-to-transfer {
  grid-column: 13 / 18;
  grid-row: 5;
}

</style>
