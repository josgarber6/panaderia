import { createStore } from 'vuex';

export default createStore({
  state: {
    cart: [],
  },
  getters: {
    totalPrice: state => state.cart.reduce((total, item) => total + item.price, 0),
    totalItems: state => state.cart.reduce((total, item) => total + item.quantity, 0),
  },
  mutations: {
    SET_CART: (state, cart) => {
      state.cart = cart;
    },
    ADD_TO_CART: (state, { product, quantity }) => {
      const productInCart = state.cart.find(item => item.product.id === product.id);
      if (productInCart) {
        if (quantity > 0) {
          productInCart.quantity += quantity;
        } else {
          alert('La cantidad introducida tiene que ser mayor que 0');
        }
      } else {
        if (quantity > 0) {
          state.cart.push({ product, quantity });
        } else {
          alert('La cantidad introducida tiene que ser mayor que 0');
        }
      }
    },
    REMOVE_FROM_CART: (state, itemId) => {
      state.cart = state.cart.filter(item => item.id !== itemId);
    },
  },
  actions: {
    loadCart: ({ commit }) => {
      const savedCart = localStorage.getItem('cart');
      const cart = savedCart ? JSON.parse(savedCart) : [];
      commit('SET_CART', cart);
    },
    saveCart: ({ state }) => {
      localStorage.setItem('cart', JSON.stringify(state.cart));
    },
    addToCart: ({ commit, dispatch }, item) => {
      commit('ADD_TO_CART', item);
      dispatch('saveCart');
    },
    removeFromCart: ({ commit, dispatch }, itemId) => {
      commit('REMOVE_FROM_CART', itemId);
      dispatch('saveCart');
    },
  },
});