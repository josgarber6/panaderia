<script>
import axios from 'axios';
import moment from 'moment';
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import { RouterLink } from 'vue-router';

export default {
  data() {
    return {
      customer: {},
      order: {},
      products: [],
      orderId: this.$route.params.orderId,
      message: '',
    };
  },
  components: {
    Navbar,
    Footer,
    RouterLink,
  },
  methods: {
    async getOrder() {
      const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL}orders/${this.orderId}`);
      this.order = response.data;
      this.order.items.forEach((item, index) => {
            this.products[item.product] = products[index];
          });
      this.customer = await this.getCustomerInfo(this.order.customer);
      const user = await this.getUserInfo(this.customer.user);
      this.customer.user = user;
    },
    async getCustomerInfo(customerId) {
      const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL_SHORT}account/customers/${customerId}`);
      return response.data;
    },
    async getUserInfo(userId) {
      const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL_SHORT}account/get-user-info/${userId}`);
      return response.data;
    },
    async getProductInfo(orderId) {
      const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL}products/${orderId}`)
      return response.data;
    },
    formatDate(date) {
      return moment(date).format('DD/MM/YYYY HH:mm');
    },
    updateOrder() {
      const formData = new FormData();
      for (const key in this.order) {
        formData.append(key, this.order[key]);
      }
      const csrf_token = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];
      try {
        axios.put(`${import.meta.env.VITE_APP_BASE_URL}orders/${this.orderId}/`, formData, {
          headers: {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'multipart/form-data',
          },
        })
        .then((response) => {
          if (response.status === 200) {
            this.$store.commit('SET_ALERT_MESSAGE', 'Pedido actualizado correctamente');
          }
          this.$router.push('/admin/orders');
          })
        .catch((error) => {
          if (error.response) {
            if (error.response.status === 400 || error.response.status === 403) {
              this.message = error.response.data.detail;
            } else {
              console.log(error);
            }
          }
        });
      } catch (error) {
        console.log(error);
      }
    },
  },
  created() {
    this.getOrder();
  },
};

</script>

<template>
  <Navbar />
  <div class="container mt-4">
    <div v-if="message" class="alert alert-danger">
      {{ message }}
    </div>
    <div class="column" style="display: flex; justify-content: center; margin-bottom: 20px">
      <h3>Editar Pedido</h3>
    </div>
    <div class="column">
      <div style="display: flex; flex-direction: column; justify-content: center;">
        <div class="form-group-centered">
          <label for="name" class="mr-2">Estado</label>
          <select class="form-control" id="shipping_status" v-model="order.shipping_status" style="width: fit-content;">
            <option v-for="(value, key) in order.shipping_status_choices" :key="key" :value="value">{{ key }}</option>
          </select>
        </div>
        <div class="form-group" style="display: flex; flex-direction: row; justify-content: center; padding-right: 110px;">
          <label for="name" class="mr-2">Pagado</label>
          <input type="checkbox" class="form-control" id="paid" v-model="order.paid" style="width: fit-content;">
        </div>
        <div class="form-group-centered">
          <label for="name" class="mr-2">M&eacute;todo de env&iacute;o</label>
          <select class="form-control" id="shipping_method" v-model="order.shipping_method" style="width: fit-content;">
            <option v-for="(value, key) in order.shipping_method_choices" :key="key" :value="value">{{ key }}</option>
          </select>
        </div>
        <div class="form-group-centered" style="margin-top: 10px;">
          <label for="name" class="mr-2">M&eacute;todo de pago</label>
          <select class="form-control" id="payment_method" v-model="order.payment_method" style="width: fit-content;">
            <option v-for="(value, key) in order.payment_method_choices" :key="key" :value="value">{{ key }}</option>
          </select>
        </div>
      </div>
      <div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: 20px;">
        <button class="btn btn-primary" @click="updateOrder" style="margin-right: 10px;">Actualizar</button>
        <RouterLink class="btn btn-danger" to="/admin/orders">Cancelar</RouterLink>
      </div>
    </div>
  </div>
  <Footer id="footer-bottom"/>
</template>

<style>
</style>