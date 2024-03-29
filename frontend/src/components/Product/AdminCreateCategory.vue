<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import axios from 'axios';
import { RouterLink } from 'vue-router';

export default {
  name: 'AdminCreateCategory',
  components: {
    Navbar,
    Footer,
    RouterLink,
  },
  data() {
    return {
      category: {
        name: '',
      },
      // mensaje de error si los hay
      message: '',
    };
  },
  methods: {
    createCategory() {
      // Creamos un objeto FormData para enviar los datos de la categoría
      const formData = new FormData();
      formData.append('name', this.category.name);
      const csrf_token = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];
      try {
        return axios.post(`${import.meta.env.VITE_APP_BASE_URL}categories/`, formData, {
          headers: {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'multipart/form-data',
          },
          })
          .then((response) => {
          if (response.status === 201) {
            // Mostramos un mensaje de éxito, cuya configuración se encuentra en el store.js
            this.$store.commit('SET_ALERT_MESSAGE', 'Categoría creada correctamente');
          }
          // Redirigimos a la vista de categorías
          this.$router.push('/admin/categories');
          })
          .catch((error) => {
            if (error.response) {
              if (error.response.status === 400 || error.response.status === 403) {
                this.message = error.response.data.detail;
              } else if (error.response && error.response.status === 500) {
                this.message = 'Ha ocurrido un error al crear la categoría';
              }
            }
          });
      } catch (error) {
        console.log(error);
      }
    },
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
      <h3>Crear Categor&iacute;a</h3>
    </div>
    <div class="column">
      <div style="display: flex; flex-direction: column; justify-content: center;">
        <div class="form-group-centered">
          <label for="name" class="mr-2">Nombre</label>
          <input type="text" class="form-control" id="name" placeholder="Ej. Integral" v-model="category.name" style="width: fit-content;">
        </div>
      </div>
      <div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: 20px;">
        <button class="btn btn-primary" @click="createCategory" style="margin-right: 10px;">Crear</button>
        <RouterLink class="btn btn-danger" to="/admin/categories">Cancelar</RouterLink>
      </div>
    </div>
  </div>
  <Footer id="footer-bottom"/>
</template>

<style scoped>
</style>