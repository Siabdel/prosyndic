<template>
  <div id="app">
    <!-- Ajoutez d'autres composants ici -->
     <file-sharing-component></file-sharing-component>
  </div>
</template>

<script>
import FileSharingComponent from './components/FileSharingComponent.vue';

// Importez d'autres composants ici

export default {
  components: {
    // Ajoutez d'autres composants ici
    FileSharingComponent
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
