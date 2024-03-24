import { describe, it, expect, beforeEach, vi } from "vitest";
import { flushPromises, shallowMount } from "@vue/test-utils";
import HomeView from "@/views/HomeView.vue";
import Vuex from "vuex";
import axios from "axios";


describe("HomeView", () => {

  let actions;
  let store;
  let state;
  let getters;
  let mockStore;
  let mockDispatch;

  beforeEach(() => {
    state = {
      cart: [],
    };

    actions = {
      addToCart: vi.fn(),
      removeFromCart: vi.fn(),
      loadCart: vi.fn(),
    };

    getters = {
      totalItems: () => 0,
    };

    store = new Vuex.Store({
      state,
      actions,
      getters,
    });

    mockDispatch = vi.fn();
    mockStore = {
      state: {
        cart: [],
      },
      dispatch: mockDispatch,
    };

    vi.resetAllMocks();

  });

  it("se monta correctamente", () => {
    const wrapper = shallowMount(HomeView, {
      global: {
        plugins: [store],
      },
    });
    expect(wrapper.exists()).toBe(true);
  });

  it("muestra el número de items en el carrito", () => {
    getters = {
      totalItems: () => 3,
    };

    const wrapper = shallowMount(HomeView, {
      global: {
        plugins: [store],
      },
    });
    expect(wrapper.html()).toContain("3");
  });

  it("muestra los productos destacados", async () => {
    getters = {
      totalItems: () => 0,
    };

    const products = [
      { name: "Producto 1", description: "Prueba", price: 100, image: "", highlighted: true, category: 2 },
      { name: "Producto 2", description: "Prueba", price: 100, image: "", highlighted: true, category: 2 },
      { name: "Producto 3", description: "Prueba", price: 100, image: "", highlighted: true, category: 2 },
    ];

    vi.spyOn(axios, "get").mockImplementationOnce(() => Promise.resolve({ data: products }));
    
    const wrapper = shallowMount(HomeView, {
      global: {
        plugins: [store],
      },
    });

    await flushPromises();

    await wrapper.vm.$nextTick();

    products.forEach((product) => {
      expect(wrapper.html()).toContain(product.name);
      expect(wrapper.html()).toContain(product.price.toString());
    });
  });

  it("añade un producto al carrito", async () => {
    getters = {
      totalItems: () => 0,
    };

    const product = { name: "Producto 1", description: "Prueba", price: 100, image: "", highlighted: true, category: "Category 1" };
    const quantity = 3;

    vi.spyOn(axios, "get").mockImplementationOnce(() => Promise.resolve({ data: product }));

    const wrapper = shallowMount(HomeView, {
      global: {
        mocks: {
          $store: mockStore,
        },
      },
    });

    await flushPromises();
    await wrapper.vm.$nextTick();

    vi.spyOn(document, "getElementById").mockImplementationOnce(() => ({ value: quantity.toString() }));

    wrapper.vm.addToCart(product);
    expect(mockDispatch).toHaveBeenCalledWith('addToCart', { product, quantity });

    mockStore.state.cart.push({ product, quantity });
    expect(wrapper.vm.cart.length).toBe(1);

    let totalItems = wrapper.vm.cart.reduce((acc, item) => acc + item.quantity, 0);
    expect(totalItems).toBe(quantity);

    vi.spyOn(document, "getElementById").mockRestore();
  });

});