<template>
  <div id="item-display" class="card">
    <h5 class="card-header">{{ title }}</h5>
    <div class="card-text" v-html="markdownContent"></div>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.css';
import DOMPurify from 'dompurify/dist/purify.min.js';
import marked from 'marked/marked.min.js';

export default {
  name: 'ItemDisplay',
  props: {
    title: String,
    content: String,
  },
  computed: {
    markdownContent() {
      return DOMPurify.sanitize(marked(this.content));
    },
  },
};
</script>

<style>
#item-display {
  min-height: 200px;
  margin: 7px;
}
</style>