<template>
  <div id="app">
    <main class="content">
      <GroupPicker :categories="categories" @displayGroup="displayGroup" />

      <ErrorMessage v-if="displayErrorMessage" />

      <Timeline :groups="displayedGroups" :timelineEvents="timelineEvents"
        @closeGroup="closeGroup" @rangeChanged="loadNewRange"
        @selectEvent="loadEvent" />

      <EventDisplay :title="selectedEvent.title" :content="selectedEvent.content" />
    </main>

    <Footer />
  </div>
</template>

<script>
import _ from 'loadsh';
import Env from '../env';
import Timeline from '@/components/Timeline.vue';
import GroupPicker from '@/components/GroupPicker.vue';
import GraphqlEndpoint from '@/components/GraphqlEndpoint';
import TimelineApi from '@/components/TimelineApi';
import SeriesCache from '@/components/SeriesCache';
import EventDisplay from '@/components/EventDisplay';
import ErrorMessage from '@/components/ErrorMessage.vue';
import Footer from '@/components/Footer.vue';

export default {
  name: 'App',
  components: {
    Timeline,
    GroupPicker,
    EventDisplay,
    ErrorMessage,
    Footer,
  },
  created() {
    this.timelineApi = new TimelineApi(new GraphqlEndpoint(Env.GRAPHQL_API), new SeriesCache());
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
  },
  data() {
    return {
      displayErrorMessage: false,
      displayedGroupIds: [],
      timelineEvents: [],
      groupsCategories: null,
      groupsMap: {},
      start: null,
      end: null,
      selectedEvent: {
        title: '',
        content: '',
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
      try {
        this.groupsCategories = await this.timelineApi.getGroupsAndCategories();
        this.displayErrorMessage = false;
      }
      catch(error) {
        console.error(error);
        this.displayErrorMessage = true;
      }
      
      let groupsMap = {};
      for (const group of this.groupsCategories.groups) {
        groupsMap[group.id] = group;
      }

      this.groupsMap = groupsMap;
    },
    async loadEvent(eventId) {
      if (eventId !== undefined) {
        try {
          let eventData = await this.timelineApi.getEvent(eventId);
          this.displayErrorMessage = false;

          this.selectedEvent = {
            title: eventData.title || '',
            content: eventData.description || '',
          };
        }
        catch (error) {
          console.error(error);
          this.displayErrorMessage = true;
        }
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

      try {
        this.timelineEvents = await this.timelineApi.getEvents(groupIds, start, end);
        this.displayErrorMessage = false;
      }
      catch (error) {
        console.log(error);
        this.displayErrorMessage = true;
      }
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
  display: flex;
  flex-direction: column;
  height: 100%;
}

body, html {
  height: 100%;
}

main {
  flex: 1 0 auto;
  padding-bottom: 20px;
}
</style>
