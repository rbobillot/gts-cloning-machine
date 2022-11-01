<script setup lang="ts">
import { Ref, ref, watch } from 'vue'
import axios from 'axios';
import 'vue-select/dist/vue-select.css'
import 'light-icons/dist/light-icon.css'
import { useTransferStore } from '../stores/transferStore';

const tStore = useTransferStore()

const gtsServiceUrl = (endpoint: string) => {
  return `http://localhost:8081/${endpoint}`
}

const typesColors = {
    "bug": "#A8B820",
    "dark": "#705848",
    "dragon": "#7038F8",
    "electric": "#F8D030",
    "fairy": "#EE99AC",
    "fighting": "#C03028",
    "fire": "#F08030",
    "flying": "#A890F0",
    "ghost": "#705898",
    "grass": "#78C850",
    "ground": "#E0C068",
    "ice": "#98D8D8",
    "normal": "#A8A878",
    "poison": "#A040A0",
    "psychic": "#F85888",
    "rock": "#B8A038",
    "steel": "#B8B8D0",
    "water": "#6890F0",
}

const damageClassColors = {
    "physical": "#F08030",
    "special": "#6890F0",
    "status": "#78C850",
}

const damageClassIcons = {
    "physical": "light-icon-medical-cross",
    "special": "light-icon-target",
    "status": "light-icon-yin-yang",
}

const getTypeColor = (type, name) => {
    const noNameNorTypeColor = "#4b5356"
    if (!name || !type) {
    return `width : 70%; background-color : ${noNameNorTypeColor};`
    }
    return `width : 70%; background-color : ${typesColors[type]};`
}

const getDamageClassColor = (dc) => {
    const noDcColor = "#4b5356"
    if (!dc) {
    return `width : 10%; background-color : ${noDcColor};`
    }
    return `width : 10%; background-color : ${damageClassColors[dc]};`
}

const getDamageClassIcon = (dc) => {
    const noDcIcon = "light-icon-dots"
    if (!dc) {
    return noDcIcon
    }
    return damageClassIcons[dc]
}

const getPokemonSprite = () => {
    if (!tStore.selectedPkmnId || !tStore.transferablePkmns) return

    const p = tStore.selectedPkmn
    if (!p) return
    return `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${p.shiny ? 'shiny/' : ''}${p.index}.png`
}

const updateSelectedPkmnMovesInfo = () => {
  const p = tStore.selectedPkmn

  if (!p) return

  p.moves.forEach((move, index) => {
    if (typeof move === 'string') {
      axios
        .get(`https://pokeapi.co/api/v2/move/${move?.toLocaleLowerCase().replace(' ', '-')}`)
        .then((moveResp) => {
          p.moves[index] = {
            index: index,
            name: move,
            // name: moveResp.data.names.find((n: any) => n.language.name === 'fr').name,
            damage_class: moveResp.data.damage_class.name,
            type: moveResp.data.type.name,
          }
        })
        .catch((err) => {
          console.log(err)
        })
    }
  })

  tStore.setTransferablePkmn(p)
}

const removePokemon = () => {
  axios
    .delete(gtsServiceUrl('pokemon/' + tStore.selectedPkmnId))
    .then((response) => {
      tStore.setPkmnId(null)
      console.log(response)
    })
    .catch((error) => {
      console.log(error)
    })
}

/**
 * Display Pokemon infos when:
 * - A "Pokemon to Transfer" is selected, when "GTS to ..." is selected
 * OR
 * - A Pokemon has been received/stored in the GTS DB
 */
const shouldDisplayPkmn = () => {
    return (tStore.selectedMode && tStore.isGtsToNds && tStore.selectedPkmnId) || tStore.receivedPkmn
}

watch(() => tStore.selectedPkmnId, () => updateSelectedPkmnMovesInfo())

</script>

<template>

  <!-- Pokemon basic info props -->
  <div v-if="shouldDisplayPkmn()" class="pkmn-sprite-star-object-nature">
    <div class="pkmn-sprite" width="96" height="96">
      <img v-tooltip.top="tStore.selectedPkmn?.species" :src="getPokemonSprite()" />
    </div>
    <div class="pkmn-shiny-star" v-tooltip.top="(tStore.selectedPkmn?.shiny ? '' : 'Not') + 'Shiny'">
      <svg v-if="tStore.selectedPkmn?.shiny" width="20" height="20" style="color: red" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 16">
        <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" fill="red"/>
      </svg>
    </div>
    <div class="pkmn-held-item">
      <img v-if="tStore.selectedPkmn?.holding.toLocaleLowerCase() !== 'nothing'"
       v-tooltip.top="tStore.selectedPkmn?.holding"
       :src="`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/${tStore.selectedPkmn?.holding.toLocaleLowerCase().replace(' ', '-')}.png`" />
    </div>
    <div class="pkmn-name">
      {{tStore.selectedPkmn?.name}}
    </div>
    <div class="remove-pkmn">
      <lv-button v-show="tStore.isGtsToNds && tStore.selectedPkmnId"
        v-tooltip.top="'Remove Pokemon from inventory'"
        class="lv--danger"
        :disabled="tStore.isTransferPending"
        :rounded="true"
        outlined
        icon="light-icon-trash"
        @click="removePokemon()"
        />
    </div>
  </div>
  <div v-if="shouldDisplayPkmn()" class="pkm-stats index-level-nature">
    <div class="pkm-stat pkmn-index"><div class="pkm-stat-title">National Index</div><div class="pkm-stat-value">{{tStore.selectedPkmn?.index}}</div></div>
    <div class="pkm-stat pkmn-level"><div class="pkm-stat-title">Level</div><div class="pkm-stat-value">{{tStore.selectedPkmn?.level}}</div></div>
    <div class="pkm-stat pkmn-nature"><div class="pkm-stat-title">Nature</div><div class="pkm-stat-value">{{tStore.selectedPkmn?.nature}}</div></div>
  </div>
  <div v-if="shouldDisplayPkmn()" class="pkm-stats ability-hiddenpower-happiness">
    <div class="pkm-stat pkmn-ability"><div class="pkm-stat-title">Ability</div><div class="pkm-stat-value">{{tStore.selectedPkmn?.ability}}</div></div>
    <div class="pkm-stat pkmn-hiddenpower"><div class="pkm-stat-title">Hidden Power</div><div class="pkm-stat-value">{{tStore.selectedPkmn?.hidden_power.base_power}} ({{tStore.selectedPkmn?.hidden_power.power_type}})</div></div>
    <div class="pkm-stat pkmn-happiness"><div class="pkm-stat-title">Happiness</div><div class="pkm-stat-value">{{tStore.selectedPkmn?.happiness}}</div></div>
  </div>
  <div v-if="shouldDisplayPkmn()" class="pkm-stats ot-tid-sid-remove">
    <div class="pkm-stat pkmn-ot"><div class="pkm-stat-title">Original Trainer</div><div class="pkm-stat-value">{{tStore.selectedPkmn?.ot}}</div></div>
    <div class="pkm-stat pkmn-tid"><div class="pkm-stat-title">Trainer ID</div><div class="pkm-stat-value">{{tStore.selectedPkmn?.tid}}</div></div>
    <div class="pkm-stat pkmn-sid"><div class="pkm-stat-title">Secret ID</div><div class="pkm-stat-value">{{tStore.selectedPkmn?.sid}}</div></div>
  </div>
  <div v-if="shouldDisplayPkmn()" class="pkmn-moves">
    <span v-for="index in 4" :key="index" :class="`lv-buttonset pkmn-move-${index}`">
      <LvButton
        :label="(tStore.selectedPkmn?.moves[index-1]?.name || tStore.selectedPkmn?.moves[index-1])"
        :disabled="tStore.selectedPkmn?.moves[index-1] === null"
        :style="getTypeColor(tStore.selectedPkmn?.moves[index-1]?.type, tStore.selectedPkmn?.moves[index-1])"
        rounded />
      <LvButton
        :disabled="tStore.selectedPkmn?.moves[index-1] === null"
        :style="getDamageClassColor(tStore.selectedPkmn?.moves[index-1]?.damage_class)"
        :icon="getDamageClassIcon(tStore.selectedPkmn?.moves[index-1]?.damage_class)" />
    </span>
  </div>

  <!-- Pokemon IVs / EVs props -->
  <div v-if="shouldDisplayPkmn()" class="ivs">
    <div class="ivs-title">IVs</div>
    <div v-for="(iv, key) in tStore.selectedPkmn?.ivs" class="iv-line" :key="key">
      <div>{{key}}</div>
      <LvSlider :value="iv" :min="0" :max="31" :step="1" :disabled="true" sliderColor="#9973ff" />
      <div>{{iv}}</div>
    </div>
  </div>
  <div v-if="shouldDisplayPkmn()" class="evs">
    <div class="evs-title">EVs</div>
    <div v-for="(evValue, evName) in tStore.selectedPkmn?.evs" class="ev-line" :key="evName">
      <div>{{evName}}</div>
      <LvSlider
        :value="evValue"
        :min="0"
        :max="(evName.toString() !== 'total') ? 252 : 510"
        :step="1"
        :disabled="true"
        sliderColor="#38b2ac" />
      <div>{{evValue}}</div>
    </div>
  </div>

</template>

<style scoped>

.pkmn-sprite-star-object-nature { 
  display: grid;
  grid-area: 5 / 2 / 8 / 5;
  grid-template-areas:
    "a a a b"
    "a a a c"
    "a a a r"
    "d d d -";
  grid-template: subgrid;
  justify-content: center;
}
.pkmn-sprite { grid-area: a; }
.pkmn-shiny-star { grid-area: b; }
.pkmn-held-item { grid-area: c; }
.pkmn-name { grid-area: d; font-weight: bold; }
.remove-pkmn { grid-area: r; }

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
  padding-left: 0.5rem;
  padding-right: 0.5rem;
}
.pkm-stat-title {
  font-style: italic;
}
.pkm-stat-value {
  font-weight: bold;
}

.index-level-nature {
  grid-area: 5 / 6 / 8 / 10;
  grid-template-areas:
    "e e e"
    "f f f"
    "g g g";
}
.pkmn-index { grid-area: e; }
.pkmn-level { grid-area: f; }
.pkmn-nature { grid-area: g; }

.ability-hiddenpower-happiness {
  grid-area: 5 / 11 / 8 / 15;
  grid-template-areas:
    "h h h"
    "i i i"
    "j j j";
}
.pkmn-ability { grid-area: h; }
.pkmn-hiddenpower { grid-area: i; }
.pkmn-happiness { grid-area: j; }

.ot-tid-sid-remove {
  grid-area: 5 / 16 / 8 / 20;
  grid-template-areas:
    "o o o"
    "p p p"
    "q q q";
}
.pkmn-ot { grid-area: o; }
.pkmn-tid { grid-area: p; }
.pkmn-sid { grid-area: q; }

.pkmn-moves {
  display: grid;
  grid-area: 9 / 6 / 11 / 15;
  grid-template-areas:
    "k k k k - l l l l"
    "m m m m - n n n n";
  row-gap: 2rem;
}
/*
** Every pkmn-move-{n} is called by the v-for loop in the template
*/ 
.pkmn-move-1 { grid-area: k; }
.pkmn-move-2 { grid-area: l; }
.pkmn-move-3 { grid-area: m; }
.pkmn-move-4 { grid-area: n; }

.ivs { grid-area: 12 / 4 / 18 / 10; }
.iv-line {
  display: grid;
  grid-template-columns: 1fr 4fr 1fr;
  grid-template-rows: 1fr 0.5fr;
  align-items: center;
}
.evs { grid-area: 12 / 11 / 19 / 17; }

.ev-line {
  display: grid;
  grid-template-columns: 1fr 4fr 1fr;
  grid-template-rows: 1fr 0.5fr;
  align-items: center;
}

</style>