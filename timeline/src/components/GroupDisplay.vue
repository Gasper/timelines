<template>
  <div class="group-header">
    <button type="button" class="close" aria-label="Close" @click="closeGroup">
      <span aria-hidden="true">&times;</span>
    </button>
    <div class="group-title">{{ name }}</div>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.css';

export default {
  name: 'GroupDisplay',
  props: {
    name: String,
    groupId: String,
  },
  methods: {
    closeGroup() {
      this.$emit('closeGroup', this.groupId);
    },
  },
};
</script>

<style scoped>
.close {
  height: 100%;
}

.group-header {
  width: 200px;
  height: 100%;
}

.group-title {
  font-weight: bolder;
  margin-left: 10px;
  height: 100%;
  width: 100%;
  text-align: left;
}
</style>