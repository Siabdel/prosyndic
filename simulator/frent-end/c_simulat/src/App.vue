<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <devis-component />
  </div>
</template>

<script>
import DevisComponent from './components/DevisComponent.vue'

export default {
  name: 'App',
  components: {
    DevisComponent,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
