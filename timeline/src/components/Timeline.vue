<template>
  <div>
    <div id='timeline' ref='timeline' />
  </div>
</template>

<script>
import 'vis-timeline/styles/vis-timeline-graph2d.min.css';
import {DataSet, Timeline} from 'vis-timeline/standalone/umd/vis-timeline-graph2d.min.js';

export default {
  name: 'Timeline',
  props: {
    timelineEvents: Array,
    groups: Array,
  },
  data() {
    return {
      timelineInstance: null,
    };
  },
  mounted() {
    let dataset = new DataSet(this.timelineEvents);
    let options = {
      groupEditable: true,
    };
    let groups = this.groups;

    this.timelineInstance = new Timeline(this.$refs.timeline);
    this.timelineInstance.setOptions(options);
    this.timelineInstance.setGroups(groups);
    this.timelineInstance.setItems(dataset);
  },
  watch: {
    groups(newGroups) {
      this.timelineInstance.setGroups(newGroups);
    },
  },
}
</script>