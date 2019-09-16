<template>
  <div id="groups-menu">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="#">
        <img src="../assets/icon.svg" width="30" height="30" alt="">
      </a>
      <div class="navbar-nav" v-for="category in categories" :key="category.id">
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            {{ category.name }}
          </a>
          <div class="dropdown-menu" aria-labelledby="navbarDropdown">
            <a class="dropdown-item" href="#" 
              v-for="group in category.groups"
              :key="group.id"
              @click="displayGroup(group.id)">
              {{ group.name }}
            </a>
          </div>
        </li>
      </div>
    </nav>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

export default {
  name: 'GroupPicker',
  props: {
    categories: Array,
  },
  methods: {
    displayGroup(groupId) {
      this.$emit('displayGroup', groupId);
    },
  },
}
</script>

<style scoped>
#groups-menu {
  margin-bottom: 0px;
}
</style>