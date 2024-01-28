<script>

  // import { RouterLink } from 'vue-router';

  export default {
    data() {
        return {
            user: {

            }, // Agrega los datos del usuario aquí si están disponibles
            imageUrl: 'http://localhost:5173/src/assets/LogoPanaderia.png'
        };
    },
    computed: {
        userIsAuthenticated() {
            // Ajusta esta lógica según cómo determines si el usuario está autenticado
            return this.user && this.user.is_authenticated;
        },
    },
    methods: {
        logout() {
            // Agrega la lógica para cerrar sesión aquí
        },
    },
};

</script>

<template>
  <div class="container-fluid m-0 p-0">
    <div id="bg-color" class="p-3" style="display: flex; flex-direction: row; justify-content: center;">
      <RouterLink to="/">
        <img :src="imageUrl" alt="US" class="img-fluid col-md-3" id="logo">
      </RouterLink>
      <template v-if="userIsAuthenticated">
        <p class="nav-link m-0 me-3" style="color: black;">
          <div class="dropdown">
            <button class="dropbtn">{{ user.email ? user.email : user.username }}</button>
            <div class="dropdown-content">
              <a href="http://localhost:8000/account/change-password">Cambiar contraseña</a>
            </div>
          </div>
        </p>
        <button class="btn btn-secondary me-3" style="background-color: #6b4d1f;" @click="logout">Cerrar Sesión</button>
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


<style>
  #bg-color {
    background-color: #edb45e;
  }

  #logo {
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

  .dropbtn {
    background-color: #4CAF50;
    color: white;
    padding: 16px;
    font-size: 16px;
    border: none;
    cursor: pointer;
  }
  
  .dropdown {
    position: relative;
    display: inline-block;
  }
  
  .dropdown-content {
    display: none;
    position: absolute;
    background-color: #f9f9f9;
    min-width: 160px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 1;
  }
  
  .dropdown-content a {
    color: black;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
  }
  
  .dropdown-content a:hover {background-color: #f1f1f1}
  
  .dropdown:hover .dropdown-content {
    display: block;
  }
  
  .dropdown:hover .dropbtn {
    background-color: #3e8e41;
  }
</style>

