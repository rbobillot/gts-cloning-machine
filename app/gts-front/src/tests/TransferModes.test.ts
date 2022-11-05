import { shallowMount } from '@vue/test-utils'
import { afterEach, beforeEach, describe, expect, it, test } from 'vitest'
import { createTestingPinia } from '@pinia/testing'
import { useFlatpassStore } from '../stores/flatpassStore'
import { useTransferStore } from '../stores/transferStore'
import TransferModes from '../components/TransferModes.vue'

describe('TransferModes, testing UI updates from flatpassStore and transferStore values', () => {
  let wrapper: any = null
  let wrapperConf: any = null
  let pinia: any = null
  let fpStore: any = null
  let tStore: any = null

  beforeEach(() => {
    pinia = createTestingPinia({
      stubActions: false, // do not allow actions to be called
    })

    fpStore = useFlatpassStore()
    fpStore.$patch({
      baseFgtsStatus: { isRunning: false }
    })

    tStore = useTransferStore()
    tStore.$patch({
      transferMode: null,
      transferablePokemons: [],
      pokemonId: ""
    })

    wrapperConf = {
      global: {
        plugins: [pinia],
        stubs: ['LvButton', 'LvDropdown', 'LvLoader'],
      },
    }
    wrapper = shallowMount(TransferModes, wrapperConf)
  })

  afterEach(() => {
    wrapper.destroy
  })

  test('the transfer-mode div should always be displayed', () => {
    expect(
      wrapper
        .find('.transfer-mode')
        .isVisible()
    ).toBe(true)
  })

  it('should contain a LvDropdown mode selector', () => {
    expect(
      wrapper
        .find('.transfer-mode-dropdown')
        .isVisible()
    ).toBe(true)
  })

  test('the start-transfer div should always be displayed', () => {
    expect(
      wrapper
        .find('.start-transfer')
        .isVisible()
    ).toBe(true)
  })

  it('should contain a transfer-button (LvButton) when transfer is not pending', () => {
    tStore.$patch({ isPending: false })
    expect(
      wrapper
        .find('.start-transfer-button')
        .exists()
    ).toBe(true)
  })

  test('the transfer-button should be disabled if the nds-gts transer cannot start', () => {
    // it cannot start when:
    // - flatpass is not running
    // - no transfer-mode is selected
    // - no transferable-pokemon is selected
    fpStore.$patch({
      baseFgtsStatus: { isRunning: false }
    })
    tStore.$patch({
      transferMode: { pf: 'nds-gts' },
      pokemonId: ""
    })

    wrapper = shallowMount(TransferModes, wrapperConf)

    expect(wrapper.find('.start-transfer-button').attributes('disabled')).toBe('true')
  })

  it('should not be disabled if the nds-gts transfer can start', () => {
    // it can start when:
    // - flatpass is running
    // - the transfer-mode "nds-gts" is selected
    // - no transferable-pokemon is selected
    fpStore.$patch({
      baseFgtsStatus: { isRunning: true }
    })
    tStore.$patch({
      transferMode: { pf: 'nds-gts' },
      pokemonId: ""
    })

    wrapper = shallowMount(TransferModes, wrapperConf)

    expect(wrapper.find('.start-transfer-button').attributes('disabled')).toBe('false')
  })

  it('should be disabled if the gts-nds transfer cannot start', () => {
    // it cannot start when:
    // - flatpass is running
    // - the transfer-mode "gts-nds" is selected
    // - no valid transferable-pokemon is selected
    fpStore.$patch({
      baseFgtsStatus: { isRunning: true }
    })
    tStore.$patch({
      transferMode: { pf: 'gts-nds' },
      transferablePokemons: [{ id: "valid-id" }],
      pokemonId: "invalid-id"
    })

    wrapper = shallowMount(TransferModes, wrapperConf)

    expect(wrapper.find('.start-transfer-button').attributes('disabled')).toBe('true')
  })

  it('should not be disabled if the gts-nds transfer can start', () => {
    // it can start when:
    // - flatpass is running
    // - the transfer-mode "gts-nds" is selected
    // - a valid transferable-pokemon is selected
    fpStore.$patch({
      baseFgtsStatus: { isRunning: true }
    })
    tStore.$patch({
      transferMode: { pf: 'gts-nds' },
      transferablePokemons: [{ id: "valid-id" }],
      pokemonId: "valid-id"
    })

    wrapper = shallowMount(TransferModes, wrapperConf)

    expect(wrapper.find('.start-transfer-button').attributes('disabled')).toBe('false')
  })

  it('should contain a LvLoader when a gts-nds transfer is pending', () => {
    fpStore.$patch({
      baseFgtsStatus: { isRunning: true }
    })
    tStore.$patch({
      isPending: true,
      transferMode: { pf: 'gts-nds' },
      transferablePokemons: [{ id: "valid-id" }],
      pokemonId: "valid-id"
    })

    wrapper = shallowMount(TransferModes, wrapperConf)

    expect(
      wrapper
        .find('.start-transfer-loader')
        .exists()
    ).toBe(true)
  })

  it('should contain a transfer-loader when a nds-gts transfer is pending', () => {
      fpStore.$patch({
        baseFgtsStatus: { isRunning: true }
      })
      tStore.$patch({
        isPending: true,
        transferMode: { pf: 'nds-gts' },
      })
  
      wrapper = shallowMount(TransferModes, wrapperConf)
  
      expect(
        wrapper
          .find('.start-transfer-loader')
          .exists()
      ).toBe(true)
  })

  it('should not contain a transfer-loader when after a transfer is done, it should rather contain a transfer-button', () => {
      fpStore.$patch({
        baseFgtsStatus: { isRunning: true }
      })
      tStore.$patch({
        isPending: true,
        transferMode: { pf: 'nds-gts' },
      })
  
      wrapper = shallowMount(TransferModes, wrapperConf)
  
      expect(wrapper.find('.start-transfer-loader').exists()).toBe(true)

      tStore.$patch({
        isPending: false,
        transferMode: { pf: 'nds-gts' },
      })
  
      wrapper = shallowMount(TransferModes, wrapperConf)
  
      expect(wrapper.find('.start-transfer-loader').exists()).toBe(false)
      expect(wrapper.find('.start-transfer-button').exists()).toBe(true)
  })

})
