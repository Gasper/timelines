<template>
  <div>
    <span>{{ name }}</span>
    <button type="button" class="close" aria-label="Close" @click="closeGroup">
      <span aria-hidden="true">&times;</span>
    </button>
  </div>
</template>

<script>
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