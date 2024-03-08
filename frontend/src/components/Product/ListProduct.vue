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
      const quantity = parseInt(document.getElementById('quantity').value);
      this.$store.dispatch('addToCart', { product, quantity });
    },
    removeFromCart(itemId) {
      this.$store.dispatch('removeFromCart', itemId);
    },
  },
  created() {
    this.getProducts();
    this.$store.dispatch('loadCart')
  },
}
</script>

<template>
  <div class="container mt-4">
    <div class="row">
      <h3>Cat&#225;logo de productos</h3>
    </div>

    <div class="row">
      <template v-for="product in products" :key="product.id">
        <div class="card-container" style="margin: 10px;">
          <div class="card">
            <img :src="product.image" alt="Imagen no disponible" class="card-img-top"/>
            <div class="card-body">
              <h5 class="card-title">{{ product.name }} {{ product.category.name }} </h5>
              <p class="card-text">{{ product.description }}</p>
              <div class="d-flex justify-content-between">
                <h6 class="mb-0">{{ product.price }} €</h6>
                <template v-if="product.category.name == 'Pico'">
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
              </div>
              <div class="d-flex justify-content-between">
                <div class="input-group mt-2">
                  <label class="input-group-text"
                          for="quantity">Cantidad</label>
                  <input type="number" class="form-control" id="quantity"
                          name="quantity" min="1" value="1">
                  <button @click="addToCart(product)" class="btn btn-success">Añadir</button>
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
