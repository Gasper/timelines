# Timelines
Timelines is a simple tool for displaying series of events in multiple timelines.

Its original purpose was displaying automatically collected public and semi-public events such as local holidays, sports events, and various deadlines. These may be sometimes still useful to notice, but would just polute the calendar if they were stored there.

Main features:
- Customizable display of various groups of events
- Event descriptions with markdown
- The configuration of groups is kept between the sessions

## Bring your own content
The code for collecting, parsing, and loading the events is not included in this repository.

## Running
Docker and docker-compose are required for running this program.

First build the images with:
```
$ ./build.sh
```
Once images are ready, you can run them with:
```
$ ./run.sh
```
The timelines are now available on the `localhost:8080`.

On the first run, demo data can be added to the database:
```
$ ./demo_data.sh
```
To stop the services simply run:
```
$ ./stop.sh
```

## License

Licensed under either of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or
  http://www.apache.org/licenses/LICENSE-2.0)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)

at your option.

Icon made by Freepik from www.flaticon.com