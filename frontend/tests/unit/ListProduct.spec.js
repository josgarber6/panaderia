import { describe, it, expect, beforeEach, vi } from "vitest";
import { shallowMount, flushPromises } from "@vue/test-utils";
import ListProduct from "@/components/Product/ListProduct.vue";
import Vuex from "vuex";
import axios from "axios";


describe("ListProduct", () => {

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
      const wrapper = shallowMount(ListProduct, {
        global: {
          plugins: [store],
        },
      });
      expect(wrapper.exists()).toBe(true);
    });

    it("muestra los productos", async () => {
      const products = [
        {
          name: "Producto 1",
          category: "Category 1",
          price: 100,
          stock: 10,
        },
        {
          name: "Producto 2",
          category: "Category 1",
          price: 200,
          stock: 20,
        },
      ];

      vi.spyOn(axios, "get").mockImplementationOnce(() => Promise.resolve({ data: products }));
      const wrapper = shallowMount(ListProduct, {
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

    it("muestra el stock de productos", async () => {
      const category = {
        id: 1,
        name: "Pico"
      };

      const products = [
        {
          name: "Producto 1",
          category: category,
          price: 100,
          stock: 10,
        },
      ];

      vi.spyOn(axios, "get").mockImplementationOnce(() => Promise.resolve({ data: products }));
      const wrapper = shallowMount(ListProduct, {
        global: {
          plugins: [store],
        },
      });

      await flushPromises();
      await wrapper.vm.$nextTick();
      
      expect(wrapper.html()).toContain("Quedan " + products[0].stock + " en stock");
    });

    it("añade un producto al carrito", async () => {
      getters = {
        totalItems: () => 0,
      };
  
      const category = {
        id: 1,
        name: "Category 1"
      };

      const products = [
        { 
          name: "Producto 1", 
          description: "Prueba", 
          price: 100, 
          category: category
        }
      ];

      const product = products[0];

      const quantity = 3;
  
      vi.spyOn(axios, "get").mockImplementationOnce(() => Promise.resolve({ data: products }));
  
      const wrapper = shallowMount(ListProduct, {
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