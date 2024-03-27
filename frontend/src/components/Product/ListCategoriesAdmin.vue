<script>
import axios from 'axios';
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';

export default {
  name: 'ListCategoriesAdmin',
  data() {
    return {
      categories: [],
    };
  },
  methods: {
    getCategories() {
      axios.get(`${import.meta.env.VITE_APP_BASE_URL}categories/`)
        .then((response) => {
          this.categories = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    showPermissionMessage(categoryId = null, path = null, action = null) {
      if (this.$store.state.user.isTwoFactorEnabled) {
        if (action === 'delete') {
          if (confirm('¿Estás seguro de que quieres eliminar esta categoría?')) {
            axios.delete(`${import.meta.env.VITE_APP_BASE_URL}categories/${categoryId}/`, {
              headers: {
                'X-CSRFToken': document.cookie.split('=')[1],
              },
            })
              .then((response) => {
                if (response.status === 204) {
                  this.$store.commit('SET_ALERT_MESSAGE', 'Categoría eliminada correctamente');
                }
                this.getCategories();
              })
              .catch((error) => {
                console.log(error);
              });
          }
        } else if (action === 'edit') {
          this.$router.push(`${path}${categoryId}/edit`);
        } else {
          this.$router.push(path);
        }
      } else {
        alert('Necesitas tener habilitado el doble factor de autenticación para realizar esta acción');
      }
    },
    clearAlertMessage() {
      setTimeout(() => {
        this.$store.commit('SET_ALERT_MESSAGE', null);
      }, 5000);
    },
  },
  created() {
    this.getCategories();
    this.$store.dispatch('loadCart');
    this.clearAlertMessage();
  },
};
</script>

<template>
  <div class="container mt-4">
    <div v-if="$store.state.alertMessage" class="alert alert-success">
      {{ $store.state.alertMessage }}
    </div>
    <div class="container d-flex justify-content-center align-items-center">
      <div class="row">
        <div class="col-md-8">
          <h2 class="text-center" style="margin-top: 20px;">Categor&iacute;as</h2>
          <button class="btn btn-primary" @click="showPermissionMessage(null,'/admin/categories/new',null)">Crear Categoría</button>
          <div style="display: flex; flex-direction: row; justify-content: center;">
            <table class="table table-bordered table-auto" style="margin-top: 20px;">
              <thead>
                <tr>
                  <th>Nombre</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="category in categories" :key="category.id">
                  <td>{{ category.name }}</td>
                  <td>
                    <div style="display: flex; flex-direction: row;">
                      <button class="btn btn-primary" @click="showPermissionMessage(category.id, '/admin/categories/', 'edit')" style="margin-right: 10px;">Editar</button>
                      <button class="btn btn-danger" @click="showPermissionMessage(category.id, '/admin/categories/', 'delete')">Eliminar</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
</style>