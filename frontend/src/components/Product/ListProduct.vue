<script>
import axios from 'axios';

export default {
  name: 'ListProduct',
  data() {
      return {
        products: [],
      };
  },
  computed: {
    cart() {
      return this.$store.state.cart;
    },
  },
  methods: {
    getProducts() {
        axios.get(`${import.meta.env.VITE_APP_BASE_URL}products/`)
            .then(response => {
            this.products = response.data;
        })
            .catch(error => {
            console.log(error);
        });
    },
    addToCart(product) {
      const quantity = parseInt(document.getElementById(`quantity-${product.id}`).value);
      if (this.$store.getters.getCategoryName(product.category) === 'Pico') {
        if (product.stock < quantity) {
          alert('No hay suficiente stock');
          return;
        } else {
          this.$store.dispatch('addToCart', { product, quantity });
        }
      } else {
        this.$store.dispatch('addToCart', { product, quantity });
      }
    },
    removeFromCart(itemId) {
      this.$store.dispatch('removeFromCart', itemId);
    },
  },
  created() {
    this.getProducts();
    this.$store.dispatch('loadCart')
    this.$store.dispatch('loadCategories');
  },
}
</script>

<template>
  <div class="container mt-4">
    <div class="row">
      <h3>Cat&aacute;logo de productos</h3>
    </div>

    <div class="row">
      <template v-for="product in products" :key="product.id">
        <div class="card-container" style="margin: 10px;">
          <div class="card">
            <img :src="product.image" alt="Imagen no disponible" class="card-img-top" style="width: 18rem; height: 16rem;"/>
            <div class="card-body">
              <template v-if="$store.getters.getCategoryName(product.category) == 'Otros'">
                <h5 class="card-title">{{ product.name }}</h5>
              </template>
              <template v-else>
                <h5 class="card-title">{{ product.name }} {{ $store.getters.getCategoryName(product.category) }}</h5>
              </template>
              <p class="card-text">{{ product.description }}</p>
              <h6 class="mb-0">{{ product.price }} €</h6>
              <template v-if="$store.getters.getCategoryName(product.category) == 'Pico'">
                <template v-if="product.stock > 1">
                  <p>Quedan {{ product.stock }} en stock</p>
                </template>
                <template v-else>
                  <p>Queda {{ product.stock }} en stock</p>
                </template>
                <template v-if="product.stock > 0">
                  <div class="d-flex align-items-center gap-1">
                    <div class="check">&#10003;</div>
                    <h6 class="text-success mb-0">Disponible</h6>
                  </div>
                </template>
                <template v-else>
                  <div class="d-flex align-items-center gap-1">
                    <div class="unavailable">&#10007;</div>
                    <h6 class="text-danger mb-0">Agotado</h6>
                  </div>
                </template>
              </template>
              <div class="d-flex justify-content-between">
                <div class="input-group mt-2">
                  <label class="input-group-text"
                          for="quantity">Cantidad</label>
                  <input type="number" class="form-control" :id="`quantity-${product.id}`"
                          name="quantity" min="1" value="1">
                  <button @click="addToCart(product)" class="btn btn-success" :id="`add-to-cart-${product.id}`">Añadir</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>


<style>
  
</style>
