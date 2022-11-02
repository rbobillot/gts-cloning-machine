<script setup lang="ts">
import 'vue-select/dist/vue-select.css'
import 'light-icons/dist/light-icon.css'

</script>

<template>

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
  grid-template-columns: repeat(20, 1fr);
  grid-template-rows: repeat(17, 1fr);
  grid-column-gap: 0px;
  grid-row-gap: 0px;
}

</style>
