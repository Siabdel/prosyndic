<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png"  class="">
    <fact-component/>
  </div>
</template>

<script>
import FactComponent from './components/FactComponent.vue'

export default {
  name: 'App',
  components: {
    FactComponent,
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
