<template>
  <div>
    <div id='timeline' ref='timeline' />
  </div>
</template>

<script>
import Vue from 'vue';
import 'vis-timeline/styles/vis-timeline-graph2d.min.css';
import './vis-timeline.patch.css';
import {Timeline} from 'vis-timeline/standalone/umd/vis-timeline-graph2d.min.js';
import GroupDisplay from './GroupDisplay.vue';

export default {
  name: 'Timeline',
  props: {
    timelineEvents: Array,
    groups: Array,
  },
  created() {
    this.timelineInstance = null;
  },
  mounted() {
    let capturedThis = this;

    let options = {
      orientation: 'both',
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

    this.timelineInstance = new Timeline(this.$refs.timeline);
    this.timelineInstance.setOptions(options);

    this.timelineInstance.on('rangechanged', (data) => {
      this.rangeChanged(data.start, data.end);
    });

    this.timelineInstance.on('select', (data) => {
      this.selectEvent(data.items[0]);
    });

    let timelineWindow = this.timelineInstance.getWindow();
    this.rangeChanged(timelineWindow.start, timelineWindow.end);
  },
  watch: {
    groups(newGroups) {
      let formattedGroupsData = newGroups.map(data => {
        return {
          id: data.id,
          content: data.name
        };
      });

      this.timelineInstance.setGroups(formattedGroupsData);
    },
    timelineEvents(newEvents) {
      this.timelineInstance.setItems(newEvents.map((item) => {
        let event = {
          id: item.id,
          content: item.title,
          start: item.start,
          group: item.groupId,
        };

        if ('end' in item && item.end != item.start) {
          event['end'] = item.end;
        }

        return event;
      }));
    }
  },
  methods: {
    closeGroup(groupId) {
      this.$emit('closeGroup', groupId);
    },
    selectEvent(eventId) {
      this.$emit('selectEvent', eventId);
    },
    rangeChanged(start, end) {
      this.$emit('rangeChanged', {
        start: new Date(start).toISOString(),
        end: new Date(end).toISOString(),
      });
    }
  }
}
</script>

<style scoped>
#timeline {
  box-sizing: border-box;
  width: 100%;
  height: 100%;
}
</style>