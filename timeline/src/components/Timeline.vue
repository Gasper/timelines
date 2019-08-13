<template>
  <div>
    <div id='timeline' ref='timeline' />
  </div>
</template>

<script>
import {DataSet, Timeline} from 'vis-timeline/standalone/umd/vis-timeline-graph2d.min.js';

export default {
  name: 'Timeline',
  data() {
    return {
      timelineInstance: null,
    };
  },
  mounted() {
    let dataset = new DataSet([]);
    let options = {};

    this.timelineInstance = new Timeline(this.$refs.timeline, dataset, options);
  },
}
</script>