<script>
import Navbar from '../Navbar.vue'
import Footer from '../Footer.vue'

export default {

  components: {
    Navbar,
    Footer,
  },

  data() {
    return {
      fields: [
                { key: 'image', label: 'Imagen' },
                { key: 'product', label: 'Producto' },
                { key: 'quantity', label: 'Cantidad' },
                { key: 'remove', label: 'Eliminar' },
                { key: 'price', label: 'Precio Unitario' },
                { key: 'total', label: 'Precio' },
      ],
    }
  },
  methods: {
    increaseQuantity(itemId) {
      this.$store.dispatch('increaseQuantity', itemId);
    },
    decreaseQuantity(itemId) {
      this.$store.dispatch('decreaseQuantity', itemId);
    },
    removeFromCart(itemId) {
      this.$store.dispatch('removeFromCart', itemId);
    },
  },
  computed: {
    cart() {
      return this.$store.state.cart;
    },
    totalPrice() {
      return this.$store.getters.totalPrice;
    },
  },
  created() {
    this.$store.dispatch('loadCart');
  },
};
</script>

<template>
  <Navbar/>
  <div class="container">
    <div class="row">
      <div class="col-12 text-center" style="margin-top: 10px;">
        <h1>Tu cesta</h1>
      </div>
    </div>
    <div class="row">
        <div class="col-md-12">
          <table class="table table-striped table-bordered">
            <thead>
              <tr>
                <th v-for="field in fields" :key="field.key">{{ field.label }}</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="item in cart" :key="item.id">
                <td><img :src="item.image" alt="Imagen" style="width: 100px; height: 100px;"></td>
                <td>{{ item.product.name }}</td>
                <td><button @click="decreaseQuantity(item.id)">-</button> {{ item.quantity }} <button @click="increaseQuantity(item.id)">+</button></td>
                <td><button @click="removeFromCart(item.id)">Eliminar</button></td>
                <td>{{ item.price }}</td>
                <td>{{ item.quantity * item.price }}</td>
              </tr>
              <tr class="table-secondary">
                <td colspan="5" class="text-end">Total</td>
                <td class="num">{{ totalPrice }} €</td>
              </tr>
            </tbody>
          </table>
        <!-- </div> -->
      </div>
    </div>
  </div>
  <Footer id="footer-bottom"/>
</template>

<style>

</style>