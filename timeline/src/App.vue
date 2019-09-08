<template>
  <div id="app">
    <GroupPicker :categories="categories" @displayGroup="displayGroup" />

    <Timeline :groups="displayedGroups" :timelineEvents="displayedEvents"
      @closeGroup="closeGroup" @rangeChanged="loadNewRange"
      @selectEvent="loadEvent" />

    <EventDisplay :title="selectedEvent.title" :content="selectedEvent.content" />
  </div>
</template>

<script>
// @ is an alias to /src
import _ from 'loadsh';
import Env from '../env';
import Timeline from '@/components/Timeline.vue';
import GroupPicker from '@/components/GroupPicker.vue';
import TimelineApi from '@/components/TimelineApi';
import SeriesCache from '@/components/SeriesCache';
import EventDisplay from '@/components/EventDisplay';

export default {
  name: 'App',
  components: {
    Timeline,
    GroupPicker,
    EventDisplay,
  },
  created() {
    this.timelineApi = new TimelineApi(Env.GRAPHQL_API, new SeriesCache());
    this.loadGroupsAndCategories();

    this.debouncedEventLoad = _.debounce(() => {
      this.loadEvents();
    }, 300);

    this.restoreDisplayedGroups();
  },
  computed: {
    categories() {
      if (this.groupsCategories === null) {
        return [];
      }

      let categoryMap = {};
      for (const category of this.groupsCategories.categories) {
        categoryMap[category.id] = category;
        categoryMap[category.id].groups = [];
      }

      for (const group of this.groupsCategories.groups) {
        categoryMap[group.categoryId].groups.push(group);
      }

      return Object.values(categoryMap);
    },
    displayedGroups() {
      let displayedGroupsData = [];
      for (const displayedGroupId of this.displayedGroupIds) {
        displayedGroupsData.push(this.groupsMap[displayedGroupId]);
      }

      return displayedGroupsData;
    },
    displayedEvents() {
      return this.timelineEvents.map((item) => {
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
      });
    },
  },
  data() {
    return {
      displayedGroupIds: [],
      timelineEvents: [],
      groupsCategories: null,
      groupsMap: {},
      start: null,
      end: null,
      selectedEvent: {
        title: "",
        content: "",
      },
    };
  },
  methods: {
    displayGroup(groupId) {
      if (!this.displayedGroupIds.includes(groupId)) {
        this.displayedGroupIds.push(groupId);
        this.storeDisplayedGroups();
      }
      this.debouncedEventLoad();
    },
    closeGroup(groupId) {
      let position = this.displayedGroupIds.findIndex(group => group == groupId);
      this.displayedGroupIds.splice(position, 1);

      this.storeDisplayedGroups();
    },
    loadNewRange(range) {
      this.start = range.start;
      this.end = range.end;
      this.debouncedEventLoad();
    },
    async loadGroupsAndCategories() {
      this.groupsCategories = await this.timelineApi.getGroupsAndCategories();
      
      let groupsMap = {};
      for (const group of this.groupsCategories.groups) {
        groupsMap[group.id] = group;
      }

      this.groupsMap = groupsMap;
    },
    async loadEvent(eventId) {
      if (eventId !== undefined) {
        const eventData = await this.timelineApi.getEvent(eventId);
        this.selectedEvent = {
          title: eventData.title || '',
          content: eventData.description || '',
        };
      }
      else {
        this.selectedEvent = {title: '', content: ''};
      }
    },
    async loadEvents() {
      let start = this.start;
      let end = this.end;
      let groupIds = this.displayedGroupIds;

      if (start === null || end === null || groupIds === null) {
        return;
      }

      this.timelineEvents = await this.timelineApi.getEvents(groupIds, start, end);
    },
    storeDisplayedGroups() {
      localStorage.displayedGroups = JSON.stringify(this.displayedGroupIds);
    },
    restoreDisplayedGroups() {
      if (localStorage.displayedGroups) {
        this.displayedGroupIds = JSON.parse(localStorage.displayedGroups);
      }
    }
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;
}
</style>
