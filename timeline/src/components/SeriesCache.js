
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
    while (data[i].start < seriesData.start && data[i] < seriesData.items.length) {
      olderSamples.push(data[i]);
      i += 1;
    }

    let newerSamples = [];
    i = data.length - 1;
    while (data[i].start > seriesData.end && i >= 0) {
      newerSamples.unshift(data[i]);
      i -= 1;
    }

    seriesData.items = olderSamples.concat(seriesData.items, newerSamples);
    
    if (start < seriesData.start) {
      seriesData.start = start;
    }

    if (end > seriesData.end) {
      seriesData.end = end;
    }

    this.seriesMap[seriesId] = seriesData;
  }

  retrieve(seriesId, start, end) {
    const seriesData = this.seriesMap[seriesId];
    return seriesData.items.filter(item => item.start >= start && item.start <= end);
  }

  has_data(seriesId, start, end) {
    if (this.seriesMap[seriesId] === undefined) {
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
