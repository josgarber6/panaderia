import { shallowMount, flushPromises } from '@vue/test-utils'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import Cart from '@/components/Cart/Cart.vue'
import Vuex from 'vuex'

describe('Cart', () => {

  let actions;
  let store;
  let state;
  let getters;

  beforeEach(() => {
    state = {
      cart: [
        {
          product: {
            id: 1,
            name: 'Producto 1',
            price: 100,
            image: "",
            category: 1,
          },
          quantity: 2,
        },
      ],
    };

    getters = {
      getCategoryName: vi.fn().mockReturnValue((id) => `Category ${id}`),
    };

    actions = {
      loadCart: vi.fn(),
      loadCategories: vi.fn(),
      removeFromCart: vi.fn(),
      increaseQuantity: vi.fn(),
      decreaseQuantity: vi.fn(),
    };

    store = new Vuex.Store({
      state,
      actions,
      getters,
    });

  });

  it('carga el carrito en la creación', () => {
    shallowMount(Cart, {
      global: {
        plugins: [store],
        stubs: {
          'router-link': true,
          RouterLink: true,
        }
      },
    });
    expect(actions.loadCart).toHaveBeenCalled();
    expect(actions.loadCategories).toHaveBeenCalled();
  });

  it('muestra el carrito vacío', () => {
    state.cart = [];
    const wrapper = shallowMount(Cart, {
      global: {
        plugins: [store],
        stubs: {
          'router-link': true,
          RouterLink: true,
        }
      },
    });
    expect(wrapper.html()).toContain('Tu cesta');
  });

  it('muestra el carrito con productos', () => {
    
    const wrapper = shallowMount(Cart, {
      global: {
        plugins: [store],
        stubs: {
          'router-link': true,
          RouterLink: true,
        }
      },
    });

    const product = state.cart[0].product;

    expect(wrapper.html()).toContain(product.name);

    const img = wrapper.find('img');
    expect(img.exists()).toBe(true);
    expect(img.attributes('src')).toBe(product.image);
    expect(img.attributes('alt')).toBe("Imagen");

    expect(wrapper.html()).toContain(product.price);

    const html = wrapper.html();
    const match = html.match(/<button id="increasedecrease">-<\/button>\s*(\d+)\s*<button id="increasedecrease">\+/);
    expect(match).toBeTruthy();
    expect(match[1]).toBe('2');
  })

  it('aumenta la cantidad de un producto', async () => {

    const mutations = {
      INCREASE_QUANTITY: (state, itemId) => {
        const productInCart = state.cart.find(item => item.id === itemId);
        productInCart.quantity++;
      },
    };

    const actions = {
      increaseQuantity: vi.fn().mockImplementation(({ commit }, itemId) => {
        commit('INCREASE_QUANTITY', itemId);
      }),
      loadCart: vi.fn(),
      loadCategories: vi.fn(),
    };

    const store = new Vuex.Store({
      state,
      actions,
      mutations,
      getters,
    });
  
    const wrapper = shallowMount(Cart, {
      global: {
        plugins: [store],
        stubs: {
          'router-link': true,
          RouterLink: true,
        }
      },
    });
  
    const itemId = state.cart[0].product.id;

    const button = wrapper.findAll('button').at(1);
    await button.trigger('click');
    expect(actions.increaseQuantity).toHaveBeenCalled();

    const quantity = state.cart.find(item => item.product.id === itemId).quantity;
    expect(quantity).toBe(3);
  });

  it('disminuye la cantidad de un producto', async () => {
    const mutations = {
      DECREASE_QUANTITY: (state, itemId) => {
        const productInCart = state.cart.find(item => item.id === itemId);
        if (productInCart.quantity > 1) {
          productInCart.quantity--;
        }
      },
    };

    const actions = {
      decreaseQuantity: vi.fn().mockImplementation(({ commit }, itemId) => {
        commit('DECREASE_QUANTITY', itemId);
      }),
      loadCart: vi.fn(),
      loadCategories: vi.fn(),
    };

    const store = new Vuex.Store({
      state,
      actions,
      mutations,
      getters,
    });
    
    const wrapper = shallowMount(Cart, {
      global: {
        plugins: [store],
        stubs: {
          'router-link': true,
          RouterLink: true,
        }
      },
    });

    const itemId = state.cart[0].product.id;

    const button = wrapper.findAll('button').at(0);
    await button.trigger('click');
    expect(actions.decreaseQuantity).toHaveBeenCalled();

    const quantity = state.cart.find(item => item.product.id === itemId).quantity;
    expect(quantity).toBe(1);
  });

  it('elimina un producto', () => {
    const wrapper = shallowMount(Cart, {
      global: {
        plugins: [store],
        stubs: {
          'router-link': true,
          RouterLink: true,
        }
      },
    });

    const button = wrapper.find('[class="btn btn-danger btn-sm"]');
    button.trigger('click');
    expect(actions.removeFromCart).toHaveBeenCalled();
  });


    
})
