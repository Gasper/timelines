import SeriesCache from '../src/components/SeriesCache';

//    Cache: [                        ]
//    Input: [    (in)                ] 
// Expected: [    (xx)                ]
test('empty cache returns full input range', () => {
  let cache = new SeriesCache();
  expect(cache.missingRanges('series', '2030-05-06T00:00:00', '2030-07-08T00:00:00'))
    .toStrictEqual([{start: '2030-05-06T00:00:00', end: '2030-07-08T00:00:00'}]);
});

test('cache with no data for that series returns full input range', () => {
  let cache = new SeriesCache();
  cache.store('series-A', '2030-05-06T00:00:00', '2030-07-08T00:00:00', []);

  expect(cache.missingRanges('series-B', '2030-05-06T00:00:00', '2030-07-08T00:00:00'))
    .toStrictEqual([{start: '2030-05-06T00:00:00', end: '2030-07-08T00:00:00'}]);
});

//    Cache: [         (data)         ]
//    Input: [    (in)                ] 
// Expected: [    (xxxx)              ]
test('input range before cache data returns (input start, data start)', () => {
  let cache = new SeriesCache();
  cache.store('series-1', '2030-05-06T00:00:00', '2030-07-08T00:00:00', []);

  expect(cache.missingRanges('series-1', '2030-03-04T00:00:00', '2030-03-019T00:00:00'))
    .toStrictEqual([{start: '2030-03-04T00:00:00', end: '2030-05-06T00:00:00'}]);
});

//    Cache: [         (data)         ]
//    Input: [                 (in)   ] 
// Expected: [              (xxxxx)   ]
test('input range after cache data returns (data end, input end)', () => {
  let cache = new SeriesCache();
  cache.store('series-2', '2030-05-06T00:00:00', '2030-07-08T00:00:00', []);

  expect(cache.missingRanges('series-2', '2030-09-04T00:00:00', '2030-09-19T00:00:00'))
    .toStrictEqual([{start: '2030-07-08T00:00:00', end: '2030-09-19T00:00:00'}]);
});

//    Cache: [         (data)         ]
//    Input: [            (  in  )    ] 
// Expected: [              (xxxx)    ]
test('input range overlaping with cache data end returns (data end, input end)', () => {
  let cache = new SeriesCache();
  cache.store('series-3', '2030-05-06T00:00:00', '2030-07-08T00:00:00', []);

  expect(cache.missingRanges('series-3', '2030-07-01T00:00:00', '2030-07-19T00:00:00'))
    .toStrictEqual([{start: '2030-07-08T00:00:00', end: '2030-07-19T00:00:00'}]);
});

//    Cache: [         (data)         ]
//    Input: [    (  in  )            ] 
// Expected: [    (xxxx)              ]
test('input range overlaping with cache data start returns (input start, data start)', () => {
  let cache = new SeriesCache();
  cache.store('series-4', '2030-05-06T00:00:00', '2030-07-08T00:00:00', []);

  expect(cache.missingRanges('series-4', '2030-05-01T00:00:00', '2030-05-19T00:00:00'))
    .toStrictEqual([{start: '2030-05-01T00:00:00', end: '2030-05-06T00:00:00'}]);
});

//    Cache: [         (data)         ]
//    Input: [    (      in     )     ] 
// Expected: [    (xxxx)    (xxx)     ]
test('input range that encapsulates cache data returns side ranges', () => {
  let cache = new SeriesCache();
  cache.store('series-5', '2030-05-06T00:00:00', '2030-07-08T00:00:00', []);

  expect(cache.missingRanges('series-5', '2030-05-01T00:00:00', '2030-07-19T00:00:00'))
    .toStrictEqual([
      {start: '2030-05-01T00:00:00', end: '2030-05-06T00:00:00'},
      {start: '2030-07-08T00:00:00', end: '2030-07-19T00:00:00'}
    ]);
});

//    Cache: [         (data)         ]
//    Input: [          (in)          ] 
// Expected: [                        ]
test('input range that is encapsulated in cache range returns empty list', () => {
  let cache = new SeriesCache();
  cache.store('series-6', '2030-05-06T00:00:00', '2030-07-08T00:00:00', []);

  expect(cache.missingRanges('series-6', '2030-05-18T00:00:00', '2030-07-01T00:00:00'))
    .toStrictEqual([]);
});

test('cache for series is empty it gets initialized with first store', () => {
  let cache = new SeriesCache();
  cache.store('series-7', '2030-05-06T00:00:00', '2030-07-08T00:00:00', [
    {start: '2030-05-06T14:13:00'},
    {start: '2030-05-06T19:15:00'},
  ]);

  expect(cache.seriesMap).toStrictEqual({
    'series-7': {
      items: [
        {start: '2030-05-06T14:13:00'},
        {start: '2030-05-06T19:15:00'},
      ],
      start: '2030-05-06T00:00:00',
      end: '2030-07-08T00:00:00',
    }
  });
});

test('overlaping data is appended to series in cache', () => {
  let cache = new SeriesCache();
  cache.store('series-7', '2030-05-06T00:00:00', '2030-07-08T00:00:00', [
    {start: '2030-05-06T14:13:00'},
    {start: '2030-05-06T19:15:00'},
  ]);

  cache.store('series-7', '2030-07-08T00:00:00', '2030-07-19T00:00:00', [
    {start: '2030-07-16T14:13:00'},
    {start: '2030-07-16T19:15:00'},
  ]);

  expect(cache.seriesMap).toStrictEqual({
    'series-7': {
      items: [
        {start: '2030-05-06T14:13:00'},
        {start: '2030-05-06T19:15:00'},
        {start: '2030-07-16T14:13:00'},
        {start: '2030-07-16T19:15:00'},
      ],
      start: '2030-05-06T00:00:00',
      end: '2030-07-19T00:00:00',
    }
  });
});