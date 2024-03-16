<script>
import Navbar from '../Navbar.vue'
import Footer from '../Footer.vue'
import PaymentOptions from '../Order/PaymentOptions.vue'
import { mapState } from 'vuex'

export default {

  components: {
    Navbar,
    Footer,
    PaymentOptions,
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
      showPaymentOptions: false,
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
    handleConfirm(data) {
      data.items = this.$store.state.cart;
      this.$store.dispatch('placeOrder', data);
      this.$store.dispatch('setPaymentOptions', false);
      this.showPaymentOptions = false;
    },
    cancel() {
      this.$store.dispatch('setPaymentOptions', false);
      this.showPaymentOptions = false;
    },
  },
  computed: {
    cart() {
      return this.$store.state.cart;
    },
    totalPrice() {
      return this.$store.getters.totalPrice;
    },
    ...mapState(['setShowPaymentOptions']),
  },
  created() {
    this.$store.dispatch('loadCart');
    this.$store.dispatch('loadCategories');
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
                <td>{{ item.product.name }} {{ $store.getters.getCategoryName(item.product.category) }}</td>
                <td><button @click="decreaseQuantity(item.product.id)" id="increasedecrease">-</button> {{ item.quantity }} <button @click="increaseQuantity(item.product.id)" id="increasedecrease">+</button></td>
                <td><button @click="removeFromCart(item.product.id)" class="btn btn-danger btn-sm">Eliminar</button></td>
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
                <button class="btn btn-success" @click="showPaymentOptions = true">Realizar Pedido</button>
                <PaymentOptions v-if="showPaymentOptions" @confirm="handleConfirm" @cancel="cancel" />
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