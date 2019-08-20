<template>
  <div>
    <div id='timeline' ref='timeline' />
  </div>
</template>

<script>
import Vue from 'vue';
import 'vis-timeline/styles/vis-timeline-graph2d.min.css';
import {DataSet, Timeline} from 'vis-timeline/standalone/umd/vis-timeline-graph2d.min.js';
import GroupDisplay from './GroupDisplay.vue';

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
  errorCaptured: false,
  mounted() {
    let capturedThis = this;
    let dataset = new DataSet(this.timelineEvents);
    let options = {
      groupEditable: true,
      groupTemplate(group) {
        let groupTag = new Vue({
          ...GroupDisplay,
          parent: capturedThis,
          abstract: true,
          errorCaptured: false,
          propsData: {name: group.content, groupId: group.id},
        }).$mount();

        groupTag.$on('closeGroup', (groupId) => {
          capturedThis.closeGroup(groupId);
        });

        return groupTag.$el;
      },
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
  methods: {
    closeGroup(groupId) {
      this.$emit('closeGroupA', groupId);
    }
  }
}
</script>