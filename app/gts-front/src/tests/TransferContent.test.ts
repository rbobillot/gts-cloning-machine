import { shallowMount } from '@vue/test-utils'
import { afterEach, beforeEach, describe, expect, it, test } from 'vitest'
import { createTestingPinia } from '@pinia/testing'
import { useTransferStore } from '../stores/transferStore'
import TransferContent from '../components/TransferContent.vue'
import Tooltip from 'lightvue/tooltip'

describe('TransferContent, testing UI updates from transferStore values', () => {
  let wrapper: any = null
  let wrapperConf: any = null
  let pinia: any = null
  let tStore: any = null

  const dummyShinyPokemon = {
    "id": "3c4648df-d02f-4eaf-a3a6-4c97b46dd716",
    "checksum": "0x0000",
    "name": "PIKACHU",
    "index": 25,
    "holding": "nothing",
    "shiny": true,
    "level": 4,
    "happiness": 70,
    "nature": "Naive",
    "species": "Pikachu",
    "ability": "Static",
    "gender": "Female",
    "ot": "0",
    "tid": 0,
    "sid": 0,
    "hidden_power": {
      "power_type": "Psychic",
      "base_power": 64
    },
    "moves": [
      "Thunder Shock",
      "Growl",
      null,
      null
    ],
    "ivs": {
      "hp": 31,
      "atk": 31,
      "def": 31,
      "spa": 31,
      "spd": 31,
      "spe": 31
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
    "raw_pkm_data": "some base64 string",
  }
  

  beforeEach(() => {
    pinia = createTestingPinia({
      stubActions: true,
    })
    // (this.selectedMode && this.isGtsToNds && this.selectedPkmnId) || this.receivedPkmn
    tStore = useTransferStore()
    tStore.$patch({
      transferMode: { pf: 'gts-nds' },
      pokemonId: "",
      receivedPkmn: null,
      transferablePokemons: [dummyShinyPokemon],
    })

    wrapperConf = {
      global: {
        plugins: [pinia],
        stubs: ['LvButton', 'LvDropdown', 'LvLoader', 'LvBadge', 'LvProgressBar', 'LvSlider', 'LvDialog', 'LvCard'],
        directives: {
          Tooltip,
        }
      },
    }

    wrapper = shallowMount(TransferContent, wrapperConf)
  })

  afterEach(() => {
    wrapper.destroy
  })

  test('the transfer-content div should not exist when no Pokemon is selected', () => {
    expect(
      wrapper
        .find('.transfer-content')
        .exists()
    ).toBe(false)
  })

  it('should exist when a valid Pokemon is selected', () => {
    tStore.$patch({ pokemonId: dummyShinyPokemon.id })

    wrapper = shallowMount(TransferContent, wrapperConf)

    expect(
      wrapper
        .find('.transfer-content')
        .exists()
    ).toBe(true)
  })

  it('should not exists when a non-valid Pokemon is selected', () => {
    tStore.$patch({ pokemonId: "invalid-id" })

    wrapper = shallowMount(TransferContent, wrapperConf)

    expect(
      wrapper
        .find('.transfer-content')
        .exists()
    ).toBe(false)
  })

  it('should not exist when the selected Pokemon is deleted', () => {
    tStore.$patch({ pokemonId: dummyShinyPokemon.id })

    wrapper = shallowMount(TransferContent, wrapperConf)

    expect(wrapper.find('.transfer-content').exists()).toBe(true)

    tStore.$patch({
      pokemonId: '',
      transferablePokemons: [],
    })

    wrapper = shallowMount(TransferContent, wrapperConf)

    expect(wrapper.find('.transfer-content').exists()).toBe(false)
  })

  it.todo('should exists when a Pokemon is received (or Created)')

})