<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <GroupPicker :categories="categories" />
    <Timeline :groups="groups" :timelineEvents="timelineEvents" />
  </div>
</template>

<script>
import Timeline from './components/Timeline.vue';
import GroupPicker from './components/GroupPicker.vue';

export default {
  name: 'App',
  components: {
    Timeline,
    GroupPicker,
  },
  data() {
    return {
      categories: [
        {id: 0, name: 'Sport', groups: [{id: 0, name: 'Tour de France 2020'}, {id: 1, name: 'Serie A'}]},
        {id: 0, name: 'Volitve', groups: [{id: 2, name: 'Občinske 2020'}, {id: 3, name: 'Državni zbor'}]},
      ],
      groups: [
        {id: 0, content: 'Volitve 2020'},
        {id: 1, content: 'Prvenstvo 2020'},
        {id: 2, content: 'Tour de France 2020'}
      ],
      timelineEvents: [
        {id: 0, content: 'item 1', start: '2020-05-20', group: 0},
        {id: 1, content: 'item 2', start: '2020-05-14', group: 1},
        {id: 2, content: 'item 3', start: '2020-05-18', group: 2},
        {id: 3, content: 'item 4', start: '2020-05-16', end: '2020-05-19', group: 0},
        {id: 4, content: 'item 5', start: '2020-05-25', group: 1},
        {id: 5, content: 'item 6', start: '2020-05-27', group: 2},
      ],
    };
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
