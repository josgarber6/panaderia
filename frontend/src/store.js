import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state: {
    cart: [],
    categories: [],
  },
  getters: {
    totalPrice: state => state.cart.reduce((total, item) => total + item.product.price * item.quantity, 0),
    totalItems: state => state.cart.reduce((total, item) => total + item.quantity, 0),
    getCategoryName: (state) => (id) => {
      const category = state.categories.find(item => item.id === id);
      return category ? category.name : '';
    },
  },
  mutations: {
    SET_CART: (state, cart) => {
      state.cart = cart;
    },
    ADD_TO_CART: (state, { product, quantity }) => {
      const productInCart = state.cart.find(item => item.product === product);
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
      const productInCart = state.cart.find(item => item.id === itemId);
      state.cart = state.cart.filter(item => item !== productInCart);
    },
    INCREASE_QUANTITY: (state, itemId) => {
      const productInCart = state.cart.find(item => item.id === itemId);
      productInCart.quantity++;
    },
    DECREASE_QUANTITY: (state, itemId) => {
      const productInCart = state.cart.find(item => item.id === itemId);
      if (productInCart.quantity > 1) {
        productInCart.quantity--;
      }
    },
    SET_CATEGORIES(state, categories) {
      state.categories = categories;
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
    increaseQuantity: ({ commit, dispatch }, itemId) => {
      commit('INCREASE_QUANTITY', itemId);
      dispatch('saveCart');
    },
    decreaseQuantity: ({ commit, dispatch }, itemId) => {
      commit('DECREASE_QUANTITY', itemId);
      dispatch('saveCart');
    },
    loadCategories({ commit }) {
      axios.get(`${import.meta.env.VITE_APP_BASE_URL}categories/`)
        .then(response => {
          commit('SET_CATEGORIES', response.data);
        })
        .catch(error => {
          console.log(error);
        });
    },
  },
});