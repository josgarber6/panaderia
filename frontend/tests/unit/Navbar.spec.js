import { describe, it, expect } from "vitest";
import { shallowMount } from "@vue/test-utils";
import Navbar from "@/components/Navbar.vue";
import Vuex from "vuex";

describe("Navbar", () => {
  it("se monta correctamente", () => {
    const getters = {
      totalItems: () => 0,
    };

    const store = new Vuex.Store({
      getters,
    });
    const wrapper = shallowMount(Navbar, {
      global: {
        plugins: [store],
      },
    });
    expect(wrapper.exists()).toBe(true);
  });

  it("muestra el número de items en el carrito", () => {
    const getters = {
      totalItems: () => 3,
    };

    const store = new Vuex.Store({
      getters,
    });
    const wrapper = shallowMount(Navbar, {
      global: {
        plugins: [store],
      },
    });
    expect(wrapper.html()).toContain("3");
  });
});