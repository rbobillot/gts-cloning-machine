import { shallowMount } from '@vue/test-utils'
import { afterEach, beforeEach, describe, expect, it, test } from 'vitest'
import { createTestingPinia } from '@pinia/testing'
import { useFlatpassStore } from '../stores/flatpassStore'
import TransferHeader from '../components/TransferHeader.vue'

describe('TransferHeader, testing UI updates from flatpassStore values', () => {
  let wrapper: any = null
  let wrapperConf: any = null
  let pinia: any = null
  let fpStore: any = null

  beforeEach(() => {
    pinia = createTestingPinia({
      stubActions: true, // do not allow actions to be called
    })
    fpStore = useFlatpassStore()
    wrapperConf = {
      global: {
        plugins: [pinia],
        stubs: ['LvBadge'],
        // stubs: ['LvButton', 'LvDropdown', 'LvLoader', 'LvBadge', 'LvProgressBar', 'LvSlider', 'LvDialog', 'LvCard'],
      },
    }
    wrapper = shallowMount(TransferHeader, wrapperConf)
  })

  afterEach(() => {
    wrapper.destroy
  })

  test('the fgts-status div should always be displayed', () => {
    expect(
      wrapper
        .find('.fgts-status')
        .isVisible()
    ).toBe(true)
  })

  it('should contain a status LvBadge', () => {
    expect(
      wrapper
        .find('.fgts-status-badge')
        .isVisible()
    ).toBe(true)
  })

  it('should display the badge with "danger" color, when fgts is not running', () => {
    fpStore.$patch({ baseFgtsStatus: { isRunning: false } })

    expect(
      wrapper
        .find('.fgts-status-badge')
        .attributes('color')
    ).toBe("danger")
  })

  it('should display the badge with "info" color, when fgts is running', () => {
    fpStore.$patch({ baseFgtsStatus: { isRunning: true } })

    wrapper = shallowMount(TransferHeader, wrapperConf)

    expect(
      wrapper
        .find('.fgts-status-badge')
        .attributes('color')
    ).toBe("info")
  })

  test.todo('display the nds-status div, and handle the badge color')

})

describe.todo('TransferHeader, testing functions updating flatpassStore')

describe.todo('TransferHeader, testing UI updates from SocketIO events')