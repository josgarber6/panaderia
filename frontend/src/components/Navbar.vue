<script>

  import { RouterLink } from 'vue-router';
  import logo from '@/assets/LogoPanaderia.png';
  import cart from '@/assets/cart.png';
  import hamburguer from '@/assets/hamburger_icon.png';

  export default {
    data() {
        return {
            user: null,
            logo,
            cart,
            sessionId: '',
            windowWidth: 0,
            hamburguer,
            base_url: import.meta.env.VITE_APP_BASE_URL_SHORT,
        };
    },
    components: {
      RouterLink,
    },
    created() {
      window.addEventListener('resize', this.handleResize);
      this.handleResize();
      this.getUserInfo()
    },
    destroyed() {
      window.removeEventListener('resize', this.handleResize);
    },
    methods: {
      getUserInfo() {
        const store = this.$store;
        store.dispatch('getUserInfo');
      },
      handleResize() {
        this.windowWidth = window.innerWidth;
      },
    },
};

</script>

<template>
  <template v-if="windowWidth >= 992">
    <div class="container-fluid m-0 p-0">
      <div id="bg-color" class="p-3" style="display: flex; flex-direction: row; justify-content: center;">
        <div style="display: flex; flex-direction: column; justify-content: center;">
          <RouterLink to="/">
            <img :src="logo" alt="US" class="img-fluid col-md-3" id="logo">
          </RouterLink>
        </div>
        <template v-if="this.$store.state.isAdmin">
          <div style="display: flex; flex-direction: row; justify-content: left;">
            <div id="column-display">
              <div id="account-setup">
                <div class="dropdown">
                  <button class="dropbtn" style="color: white;">Administración</button>
                  <div class="dropdown-content">
                    <RouterLink to="/admin/products">Productos</RouterLink>
                    <RouterLink to="/admin/categories">Categorías</RouterLink>
                    <RouterLink to="/admin/orders">Pedidos</RouterLink>
                    <RouterLink to="/admin/stats">Estad&iacute;sticas</RouterLink>
                  </div>
                </div>
              </div>
            </div>
            <h5 style="display: flex; flex-direction: column; justify-content: center; margin-left: 20px;">
              <RouterLink to="/about" style="color: white;">Sobre Nosotros</RouterLink>
            </h5>
          </div>
        </template>
        <template v-else>
          <div style="display: flex; flex-direction: row; justify-content: left;">
            <h5 style="display: flex; flex-direction: column; justify-content: center;">
              <RouterLink to="/products" style="color: white;">Productos</RouterLink>
            </h5>
            <h5 style="display: flex; flex-direction: column; justify-content: center; margin-left: 20px;">
              <RouterLink to="/about" style="color: white;">Sobre Nosotros</RouterLink>
            </h5>
          </div>
        </template>
        <template v-if="this.$store.state.authenticated">
          <div id="account-setup">
            <div id="column-display">
              <div class="dropdown">
                <button class="dropbtn">{{ this.$store.state.user.email ? this.$store.state.user.email : this.$store.state.user.username }}</button>
                <div class="dropdown-content">
                  <a :href="base_url + 'account/change-password'">Cambiar contraseña</a>
                  <template v-if="!this.$store.state.user.isTwoFactorEnabled">
                    <a :href="base_url + 'account/two_factor/setup'">Activar doble factor</a>
                  </template>
                  <template v-if="!this.$store.state.isAdmin">
                    <RouterLink to="/order/my_orders">Mis pedidos</RouterLink>
                  </template>
                </div>
              </div>
            </div>
          </div>
          <div id="column-display" style="margin-left: 10px;">
            <a class="btn btn-secondary" id="logout" :href="base_url + 'account/logout'">Cerrar Sesión</a>
          </div>
          <div id="column-display" style="margin-left: 10px;">
            <router-link to="/cart">
              <img :src="cart" alt="Cart" width="40" height="40"/>
              <span class="badge" style="color: aliceblue; background-color: #6b4d1f;">
                {{ this.$store.getters.totalItems }}
              </span>
            </router-link>
          </div>
        </template>
        <template v-else>
          <div id="account-setup">
            <div id="column-display">
              <a class="btn btn-secondary" id="login" :href="base_url + 'account/login'">Iniciar Sesión</a>
            </div>
            <div id="column-display">
              <a class="btn btn-secondary" id="signup" :href="base_url + 'account/signup'">Registrarse</a>
            </div>
            <div id="column-display" style="margin-left: 10px;">
              <router-link to="/cart">
                <img :src="cart" alt="Cart" width="40" height="40"/>
                <span class="badge" style="color: aliceblue; background-color: #6b4d1f;">
                  {{ this.$store.getters.totalItems }}
                </span>
              </router-link>
            </div>
          </div>
        </template>
      </div>
    </div>
  </template>
  
  <!-- Navbar oculto con hamburguesa en pantallas pequeñas -->
  
  <template v-else>
    <div class="container-fluid m-0 p-0">
      <nav class="navbar navbar-expand-lg navbar-custom">
        <div style="display: flex; flex-direction: column; justify-content: center;">
          <RouterLink to="/">
            <img :src="logo" alt="US" class="img-fluid col-md-3" id="logo">
          </RouterLink>
        </div>
        <div style="display: flex; flex-direction: row; justify-content: center; margin-left: auto;">
          <div style="display: flex; flex-direction: column; justify-content: center">
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
              <span>
                <img :src=hamburguer alt="Hamburger" width="40" height="40"/>
              </span>
            </button>
          </div>
        </div>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <template v-if="this.$store.state.isAdmin">
            <div style="display: flex; flex-direction: row; justify-content: left; margin-bottom: 5px;">
              <div id="column-display">
                <div id="account-setup">
                  <div class="dropdown">
                    <button class="dropbtn" style="color: white;">Administración</button>
                    <div class="dropdown-content">
                      <RouterLink to="/admin/products">Productos</RouterLink>
                      <RouterLink to="/admin/categories">Categorías</RouterLink>
                      <RouterLink to="/admin/orders">Pedidos</RouterLink>
                      <RouterLink to="/admin/stats">Estad&iacute;sticas</RouterLink>
                    </div>
                  </div>
                </div>
              </div>
              <h5 style="display: flex; flex-direction: column; justify-content: center; margin-left: 20px;">
                <RouterLink to="/about" style="color: white;">Sobre Nosotros</RouterLink>
              </h5>
            </div>
          </template>
          <template v-else>
          <div style="display: flex; flex-direction: row; justify-content: left; margin-bottom: 5px;">
            <h5>
              <RouterLink to="/products" style="color: white;">Productos</RouterLink>
              <RouterLink to="/about" style="color: white; margin-left: 20px">Sobre Nosotros</RouterLink>
            </h5>
          </div>
          </template>
          <template v-if="this.$store.state.authenticated">
            <div id="account-setup">
              <div id="column-display" style="margin-top: 5px;">
                <div class="dropdown">
                  <button class="dropbtn">{{ this.$store.state.user.email ? this.$store.state.user.email : this.$store.state.user.username }}</button>
                  <div class="dropdown-content">
                    <a :href="base_url + 'account/change-password'">Cambiar contraseña</a>
                    <template v-if="!this.$store.state.user.isTwoFactorEnabled">
                      <a :href="base_url + 'account/two_factor/setup'">Activar doble factor</a>
                    </template>
                    <RouterLink to="/order/my_orders">Mis pedidos</RouterLink>
                  </div>
                </div>
              </div>
              <div id="column-display" style="margin-left: 10px;">
                <a class="btn btn-secondary" id="logout" :href="base_url + 'account/logout'">Cerrar Sesión</a>
              </div>
            </div>
            <div id="column-display" style="margin-top: 5px;">
              <RouterLink to="/cart">
                <img :src="cart" alt="Cart" width="40" height="40"/>
                <span class="badge" style="color: aliceblue; background-color: #6b4d1f;">
                  {{ this.$store.getters.totalItems }}
                </span>
              </RouterLink>
            </div>
          </template>
          <template v-else>
            <div id="account-setup">
              <div id="column-display">
                <a class="btn btn-secondary" id="login" :href="base_url + 'account/login'">Iniciar Sesión</a>
              </div>
              <div id="column-display">
                <a class="btn btn-secondary" id="signup" :href="base_url + 'account/signup'">Registrarse</a>
              </div>
            </div>
              <div id="column-display">
                <RouterLink to="/cart">
                  <img :src="cart" alt="Cart" width="40" height="40"/>
                  <span class="badge" style="color: aliceblue; background-color: #6b4d1f;">
                    {{ this.$store.getters.totalItems }}
                  </span>
                </RouterLink>
              </div>
          </template>
        </div>
      </nav>
    </div>
  </template>
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

  .navbar-custom {
    background-color: #edb45e;
  }

</style>

