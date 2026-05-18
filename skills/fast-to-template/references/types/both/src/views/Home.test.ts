import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import Home from './Home.vue'

describe('Home', () => {
  it('renders the project name', () => {
    const wrapper = mount(Home, {
      global: {
        stubs: {
          'el-button': { template: '<button><slot /></button>' },
          'van-button': { template: '<button><slot /></button>' },
        },
      },
    })

    expect(wrapper.text()).toContain('__PROJECT_NAME__')
  })
})
