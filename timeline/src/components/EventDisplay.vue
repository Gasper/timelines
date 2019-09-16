<template>
  <div id="event-display" class="card">
    <h5 class="card-header">{{ title }}</h5>
    <div id="empty-message" class="text-muted" v-if="title === '' && content === ''">
      Select an event from the timeline.
    </div>
    <div class="card-text" v-html="markdownContent"></div>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.css';
import DOMPurify from 'dompurify/dist/purify.min.js';
import marked from 'marked/marked.min.js';

export default {
  name: 'EventDisplay',
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
#event-display {
  min-height: 100px;
  margin: 7px;
}

#empty-message {
  margin: 23px;
}
</style>