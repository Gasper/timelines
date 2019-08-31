<template>
  <div id="app">
    <GroupPicker :categories="categories" @displayGroup="displayGroup" />

    <Timeline :groups="displayedGroups" :timelineEvents="displayedEvents"
      @closeGroup="closeGroup" @rangeChanged="loadNewRange"
      @selectItem="selectItem" />

    <ItemDisplay :title="displayedItem.title" :content="displayedItem.content" />
  </div>
</template>

<script>
// @ is an alias to /src
import _ from 'loadsh';
import Timeline from '@/components/Timeline.vue';
import GroupPicker from '@/components/GroupPicker.vue';
import TimelineApi from '@/components/TimelineApi';
import SeriesCache from '@/components/SeriesCache';
import ItemDisplay from '@/components/ItemDisplay';

export default {
  name: 'App',
  components: {
    Timeline,
    GroupPicker,
    ItemDisplay,
  },
  created() {
    this.timelineApi = new TimelineApi('http://localhost:5000/graphql');
    this.loadCategories();

    this.debouncedEventLoad = _.debounce(() => {
      this.loadEvents();
    }, 300);

    if (localStorage.displayedGroups) {
      this.displayedGroupIds = JSON.parse(localStorage.displayedGroups);
    }
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
      eventSeriesData: new SeriesCache(),
      groupsCategories: null,
      groupsMap: {},
      start: null,
      end: null,
      displayedItem: {
        title: "",
        content: "",
      },
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
        
        localStorage.displayedGroups = JSON.stringify(this.displayedGroupIds);
      }
      this.debouncedEventLoad();
    },
    closeGroup(groupId) {
      let position = this.displayedGroupIds.findIndex(group => group == groupId);
      this.displayedGroupIds.splice(position, 1);

      localStorage.displayedGroups = JSON.stringify(this.displayedGroupIds);
    },
    async selectItem(itemId) {
      if (itemId !== undefined) {
        const eventData = await this.timelineApi.getEvent(itemId);
        this.displayedItem = {
          title: eventData.title || '',
          content: eventData.description || '',
        };
      }
      else {
        this.displayedItem = {
          title: '',
          content: '',
        };
      }
    },
    loadNewRange(range) {
      this.start = range.start;
      this.end = range.end;
      this.debouncedEventLoad();
    },
    async loadEvents() {
      let start = this.start;
      let end = this.end;
      let groupIds = this.displayedGroupIds;

      if (start === null || end === null || groupIds === null) {
        return;
      }

      let loadingRanges = [];
      for (const groupId of groupIds) {
        const missingRanges = this.eventSeriesData.missing_ranges(groupId, start, end);

        for (const missingRange of missingRanges) {
          const loadEventsPromise = this.timelineApi.getEvents(groupId, missingRange.start, missingRange.end);
          const loadEventsStorePromise = loadEventsPromise.then((events) => {
            this.eventSeriesData.store(groupId, start, end, events);
          });

          loadingRanges.push(loadEventsStorePromise);
        }
      }

      await Promise.all(loadingRanges);

      var displayedEvents = [];
      for (const groupId of groupIds) {
        const storedEvents = this.eventSeriesData.retrieve(groupId, start, end);
        displayedEvents = displayedEvents.concat(storedEvents);
      }

      this.timelineEvents = displayedEvents;
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
