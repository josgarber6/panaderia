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
        <div class="alert alert-danger" role="alert" v-if="cart.length === 0">
          No hay productos en la cesta
        </div>
        <div class="table-responsive">
          <table class="table table-striped table-bordered" style="margin-bottom: 10px;">
            <thead id="cabecera">
              <tr>
                <th v-for="field in fields" :key="field.key" style="color: black; font-weight: bold;">{{ field.label }}</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="item in cart" :key="item.id">
                <td><img :src="item.product.image" alt="Imagen" style="width: 100px; height: 100px;"></td>
                <td>{{ item.product.name }}</td>
                <td><button @click="decreaseQuantity(item.id)" id="increasedecrease">-</button> {{ item.quantity }} <button @click="increaseQuantity(item.id)" id="increasedecrease">+</button></td>
                <td><button @click="removeFromCart(item.id)" class="btn btn-danger btn-sm">Eliminar</button></td>
                <td style="text-align: center;">{{ item.product.price }} €</td>
                <td style="text-align: center;">{{ item.quantity * item.product.price }} €</td>
              </tr>
              <tr class="table-secondary">
                <td colspan="5" style="text-align: end;">Total</td>
                <td class="num" style="text-align: center;">{{ totalPrice }} €</td>
              </tr>
            </tbody>
          </table>
          <div style="margin-bottom: 110px;">
            <p style="text-align: end;">
              <RouterLink class="btn btn-primary" to="/products" style="margin-right: 10px;">Continuar comprando</RouterLink>
              <template v-if="cart.length > 0">
              <RouterLink class="btn btn-success" to="/order/create">Realizar pedido</RouterLink>
              </template>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <Footer id="footer-bottom"/>
</template>

<style>

#increasedecrease {
  width: fit-content;
  height: fit-content;
  color: black;
  background-color: #edb45e;
  border: none;
  border-radius: 0.2em;
}

#cabecera {
  background-color: #edb45e;
  color: white;
}

</style>