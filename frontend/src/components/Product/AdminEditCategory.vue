<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import axios from 'axios';
import { RouterLink } from 'vue-router';

export default {
  name: 'AdminEditCategory',
  components: {
    Navbar,
    Footer,
    RouterLink,
  },
  data() {
    return {
      category: {},
      categoryId: this.$route.params.categoryId,
      message: '',
    };
  },
  methods: {
    getCategory() {
      axios.get(`${import.meta.env.VITE_APP_BASE_URL}categories/${this.categoryId}/`)
        .then(response => {
          this.category = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    },
    updateCategory() {
      const formData = new FormData();
      formData.append('name', this.category.name);
      const csrf_token = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];
      try {
        axios.put(`${import.meta.env.VITE_APP_BASE_URL}categories/${this.categoryId}/`, formData, {
          headers: {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'multipart/form-data',
          },
        })
        .then((response) => {
          if (response.status === 200) {
            this.$store.commit('SET_ALERT_MESSAGE', 'Categoría actualizada correctamente');
          }
          this.$router.push('/admin/categories');
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
    this.getCategory();
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
      <h3>Editar Categor&iacute;a</h3>
    </div>
    <div class="column">
      <div style="display: flex; flex-direction: column; justify-content: center;">
        <div class="form-group-centered">
          <label for="name" class="mr-2">Nombre</label>
          <input type="text" class="form-control" id="name" v-model="category.name" style="width: fit-content;">
        </div>
      </div>
      <div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: 20px;">
        <button class="btn btn-primary" @click="updateCategory" style="margin-right: 10px;">Actualizar</button>
        <RouterLink class="btn btn-danger" to="/admin/categories">Cancelar</RouterLink>
      </div>
    </div>
  </div>
  <Footer id="footer-bottom"/>
</template>

<style>
.form-group-centered {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>