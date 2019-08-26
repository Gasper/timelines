<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <GroupPicker :categories="categories" @displayGroup="displayGroup" />
    <Timeline :groups="displayedGroups" :timelineEvents="timelineEvents" @closeGroup="closeGroup" />
  </div>
</template>

<script>
import Timeline from './components/Timeline.vue';
import GroupPicker from './components/GroupPicker.vue';
import TimelineApi from './components/TimelineApi';
import SeriesCache from './components/SeriesCache';

export default {
  name: 'App',
  components: {
    Timeline,
    GroupPicker,
  },
  created() {
    this.timelineApi = new TimelineApi('http://localhost:5000/graphql');
    this.loadCategories();
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
      let groups = [];
      for (const displayedGroupId of this.displayedGroupIds) {
        if (displayedGroupId in this.groupsMap) {
          let displayedGroup = this.groupsMap[displayedGroupId];
          groups.push({id: displayedGroup.id, content: displayedGroup.name});
        }
      }

      return groups;
    },
  },
  data() {
    return {
      displayedGroupIds: ['country'],
      timelineEvents: [
        {id: 0, content: 'item 1', start: '2020-05-20', group: 0},
        {id: 1, content: 'item 2', start: '2020-05-14', group: 1},
        {id: 2, content: 'item 3', start: '2020-05-18', group: 2},
        {id: 3, content: 'item 4', start: '2020-05-16', end: '2020-05-19', group: 0},
        {id: 4, content: 'item 5', start: '2020-05-25', group: 1},
        {id: 5, content: 'item 6', start: '2020-05-27', group: 2},
      ],
      eventSeriesData: new SeriesCache(),
      groupsCategories: null,
      groupsMap: {},
    };
  },
  methods: {
    async loadCategories() {
      this.groupsCategories = await this.timelineApi.getGroups();
      
      let groupsMap = {};
      for (const group of this.groupsCategories.groups) {
        groupsMap[group.id] = group;
      }

      this.groupsMap = groupsMap;
    },
    displayGroup(groupId) {
      if (!this.displayedGroupIds.includes(groupId)) {
        this.displayedGroupIds.push(groupId);
      }
    },
    closeGroup(groupId) {
      let position = this.displayedGroupIds.findIndex(group => group.groupId == groupId);
      this.displayedGroupIds.splice(position, 1);
    },
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
  margin-top: 60px;
}
</style>
