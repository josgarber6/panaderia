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
    showPermissionMessage(productId=null, path=null, action=null) {
      if (this.$store.state.user.isTwoFactorEnabled) {
        if (action === 'delete') {
          if (confirm('¿Estás seguro de que quieres eliminar este producto?')) {
            axios.delete(`${import.meta.env.VITE_APP_BASE_URL}products/${productId}/`, {
              headers: {
                'X-CSRFToken': document.cookie.split('=')[1],
              },
            })
              .then((response) => {
                if (response.status === 204) {
                  this.$store.commit('SET_PRODUCT_ALERT_MESSAGE', 'Producto eliminado correctamente');
                }
                this.getProducts();
              })
              .catch(error => {
                console.log(error);
              });
          }
        } else {
          this.$router.push(`${path}${productId}/edit`);
        }
      } else {
        alert('Necesitas tener habilitado el doble factor de autenticación para realizar esta acción');
      }
    },
    clearProductAlertMessage() {
      setTimeout(() => {
        this.$store.commit('SET_PRODUCT_ALERT_MESSAGE', null);
      }, 5000);
    },
  },
  created() {
    this.getProducts();
    this.$store.dispatch('loadCart')
    this.$store.dispatch('loadCategories');
    this.clearProductAlertMessage();
  },
}
</script>

<template>
  <div class="container mt-4">
    <div v-if="$store.state.productAlertMessage" class="alert alert-success">
      {{ $store.state.productAlertMessage }}
    </div>
    <div class="row">
      <h3>Cat&#225;logo de productos</h3>
    </div>
    <button class="btn btn-primary" @click="showPermissionMessage(null,'/admin/products/new',null)">Crear Producto</button>
    <div class="row">
      <template v-for="product in products" :key="product.id">
        <div class="card-container" style="margin: 10px;">
          <div class="card">
            <img :src="product.image" alt="Imagen no disponible" class="card-img-top" style="width: 18rem; height: 16rem;"/>
            <div class="card-body">
              <h5 class="card-title">{{ product.name }} {{ $store.getters.getCategoryName(product.category) }} </h5>
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
              <div style="margin-top: 5px;">
                <button class="btn btn-primary" style="margin-right: 5px;" @click="showPermissionMessage(product.id, '/admin/products/', 'edit')">Editar</button>
                <button class="btn btn-danger" @click="showPermissionMessage(product.id, '/admin/products/', 'delete')">Eliminar</button>
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
