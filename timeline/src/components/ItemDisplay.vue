<template>
  <div id="item-display" class="card">
    <h5 class="card-header">{{ title }}</h5>
    <p class="card-text">{{ content }}</p>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.css';

export default {
  name: 'ItemDisplay',
  props: {
    title: String,
    content: String,
  },
};
</script>

<style>
#item-display {
  min-height: 200px;
  margin: 7px;
}
</style>