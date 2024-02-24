<script>

  import axios from 'axios';
  import { RouterLink } from 'vue-router';

  export default {
    data() {
        return {
            user: null,
            imageUrl: 'http://localhost:5173/src/assets/LogoPanaderia.png',
            sessionId: '',
            userIsAuthenticated: false,
        };
    },
    created() {
      this.getUserInfo()
    },
    methods: {
      getUserInfo() {
        axios.defaults.withCredentials = true;
        axios.get('http://localhost:8000/account/get-username-from-session/')
        .then(response => {
          this.userIsAuthenticated = true;
          this.user = response.data;
        })
        .catch(error => {
          console.error('Error retrieving user info:', error);
          this.userIsAuthenticated = false;
        });
      },
    },
};

</script>

<template>
  <div class="container-fluid m-0 p-0">
    <div id="bg-color" class="p-3" style="display: flex; flex-direction: row; justify-content: center;">
      <div style="display: flex; flex-direction: column; justify-content: center;">
        <RouterLink to="/">
          <img :src="imageUrl" alt="US" class="img-fluid col-md-3" id="logo">
        </RouterLink>
      </div>
      <div style="display: flex; flex-direction: row; justify-content: left;">
        <h5 style="display: flex; flex-direction: column; justify-content: center;">
          <RouterLink to="/products" style="color: white;">Productos</RouterLink>
        </h5>
      </div>
      <template v-if="userIsAuthenticated">
        <div id="account-setup">
          <div id="column-display">
            <div class="dropdown">
              <button class="dropbtn">{{ user.email ? user.email : user.username }}</button>
              <div class="dropdown-content">
                <a href="http://localhost:8000/account/change-password">Cambiar contraseña</a>
              </div>
            </div>
          </div>
        </div>
        <div id="column-display" style="margin-left: 10px;">
          <a class="btn btn-secondary" id="logout" href="http://localhost:8000/account/logout">Cerrar Sesión</a>
        </div>
      </template>
      <template v-else>
      <div id="account-setup">
        <div id="column-display">
          <a class="btn btn-secondary" id="login" href="http://localhost:8000/account/login">Iniciar Sesión</a>
        </div>
        <div id="column-display">
          <a class="btn btn-secondary" id="signup" href="http://localhost:8000/account/signup">Registrarse</a>
        </div>
      </div>
      </template>
    </div>
  </div>
</template>


<style scoped>
  #bg-color {
    background-color: #edb45e;
    height: 100px;
  }

  #logo {
    min-width: 120px;
    max-width: 120px;
  }

  #account-setup {
    display: flex;
    flex-direction: row;
    margin-left: auto;
  }

  #column-display {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  #login {
    display: inline-flex;
    flex-direction: column;
    background-color: #6b4d1f;
    width: fit-content;
    height: fit-content;
  }
  
  #signup {
    margin-left: 10px;
    display: inline-flex;
    background-color: #6b4d1f;
    width: fit-content;
    height: fit-content;
  }

  #logout {
    display: inline-flex;
    flex-direction: column;
    background-color: #6b4d1f;
    width: fit-content;
    height: fit-content;
  }

  .dropdown {
    position: relative;
    display: inline-block;
  }
  
  .dropbtn {
    display: inline-block;
    padding: 0.5em 1em;
    background: #6b4d1f;
    color: white;
    border-radius: 1em;
    border: none;
    outline: 1px solid black;
    outline-offset: 3px;
  }

  .dropdown-content {
    display: none;
    position: absolute;
    background-color: #f5f5f5; /* Color de fondo más claro */
    min-width: 160px;
    border-radius: 0.5em;
    border: 2px solid black;
    padding: 0.5em 0;
    z-index: 1;
  }

  .dropdown-content a {
    color: black;
    padding: 0.5em 1em;
    text-decoration: none;
    display: block;
  }

  .dropdown-content a:hover {
    background-color: #ddd; /* Cambio de color al pasar el mouse */
  }

  .dropdown:hover .dropdown-content {
    display: block;
  }
</style>

