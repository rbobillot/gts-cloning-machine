<script setup lang="ts">
import { Ref, ref } from 'vue'
import axios from 'axios';
import 'vue-select/dist/vue-select.css'
import 'light-icons/dist/light-icon.css'

</script>

<template>

<!-- Terminals infos -->
<div class="main-grid">

  <TransferHeader />
  
  <TransferModes />

  <TransferContent />

</div>

</template>

<style scoped>

body {
  font-family: 'Source Sans Pro', 'Helvetica Neue', Arial, sans-serif;
}

.main-grid {
  display: grid;
  grid-template-columns: repeat(23, 1fr);
  grid-template-rows: repeat(16, 1fr);
  grid-column-gap: 0px;
  grid-row-gap: 0px;
}

</style>
