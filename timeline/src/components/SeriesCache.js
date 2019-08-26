
class SeriesCache {
  constructor() {
    this.seriesMap = {};
  }

  store(seriesId, start, end, data) {
    data.sort((a, b) => {
      if (a.start < b.start) {
        return -1;
      }
      else if (b.start < a.start) {
        return 1;
      }
      else {
        return 0;
      }
    });

    if (seriesId in this.seriesMap === false) {
      this.seriesMap[seriesId] = {start: start, end: end, items: data};
      return;
    }

    let seriesData = this.seriesMap[seriesId];

    let olderSamples = [];
    var i = 0;
    while (data[i].start < seriesData.start) {
      olderSamples.push(data[i]);
    }

    let newerSamples = [];
    i = data.length - 1;
    while (data[i].start > seriesData.end) {
      newerSamples.unshift(data[i]);
    }

    seriesData.items = olderSamples.concat(seriesData.items, newerSamples);
    
    if (start < seriesData.start) {
      seriesData.start = start;
    }

    if (end > seriesData.end) {
      seriesData.end = end;
    }
  }

  retrieve(seriesId, start, end) {
    const seriesData = this.seriesMap[seriesId];

    return seriesData.filter(item => {
      item.start >= start && item.start <= end
    });
  }

  has_data(seriesId, start, end) {
    if (seriesId in this.seriesMap === false) {
      return false;
    }
    
    const seriesData = this.seriesMap[seriesId];
    
    if (start < seriesData.start || end > seriesData.end) {
      return false;
    }
    else {
      return true;
    }
  }
}

export default SeriesCache;
