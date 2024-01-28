<template>
  <div class="container">
    <div class="row">
      <div class="col text-left">
        <h1>Listado de productos</h1>
        
        <div class="col-md-12">
          <table class="table table-striped">
            <thead>
              <tr>
                <th v-for="field in fields" :key="field.key">{{ field.label }}</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="product in products" :key="product.id">
                <td>{{ product.name }}</td>
                <td>{{ product.description }}</td>
                <td>{{ product.price }}</td>
                <td><img :src="product.img" alt="product.name" width="100px"></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <!-- Your component's HTML code goes here -->
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ListProduct',
  // Your component's JavaScript code goes here
  data() {
    return {
      fields: [
        { key: 'name', label: 'Nombre' },
        { key: 'description', label: 'Descripción' },
        { key: 'price', label: 'Precio' },
        { key: 'img', label: 'Imagen'}
      ],
      products: []
    }
  },
  methods: {
    getProducts() {
      axios.get('http://localhost:8000/api/v1.0/products/')
        .then(response => {
          this.products = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    }
  },
  created() {
    this.getProducts();
  },
}
</script>

<style scoped>
/* Your component's CSS code goes here */
</style>
