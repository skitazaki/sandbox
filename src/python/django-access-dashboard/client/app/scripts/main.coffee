#/*global require*/
'use strict'

require.config
  shim:
    bootstrap:
      deps: ['jquery'],
      exports: 'jquery'
    nvd3:
      deps: ['d3.global'],
      exports: 'nv'
  paths:
    jquery: '../bower_components/jquery/dist/jquery'
    backbone: '../bower_components/backbone/backbone'
    underscore: '../bower_components/lodash/dist/lodash'
    bootstrap: '../bower_components/sass-bootstrap/dist/js/bootstrap'
    d3: '../bower_components/d3/d3'
    nvd3: '../bower_components/nvd3/nv.d3'
    moment: '../bower_components/moment/min/moment-with-langs'

###
See:
http://stackoverflow.com/questions/13157704/how-to-integrate-d3-with-require-js
###
define 'd3.global', ['d3'], (_) ->
  d3 = _;

require [
  'jquery',
  'moment',
  'nvd3',
  'routes/logrecord'
  'collections/logrecord'
  'views/logrecord'
  'collections/sidemenu'
  'views/sidemenu'
], ($, moment, nv, LogRecordRouter,
    LogRecordCollection, LogRecordView, SideMenuCollection, SideMenuView) ->

  class GraphWrapper
    constructor: (@url, @screen) ->
      @dataset = []

    render: (datum) ->
      screenId = @screen

      nv.addGraph () ->
        chart = nv.models['stackedAreaChart']()
                      .x((d) -> d[0])
                      .y((d) -> d[1])
                      .margin({left: 100, right: 100, top: 20, bottom: 20})
                      .useInteractiveGuideline(true)
                      .transitionDuration(350)
                      .showLegend(true)
                      .showYAxis(true)
                      .showXAxis(true)
                      .clipEdge(true)
                      .color(d3.scale.category10().range())

        chart.xAxis
             .axisLabel('Day')
             .tickFormat (d) -> d3.time.format('%Y/%m/%d')(new Date d)

        chart.yAxis
             .axisLabel('Access Count')
             .showMaxMin(false)
             .tickFormat d3.format ','

        # Cleanup previously rendered chart.
        d3.select(screenId).selectAll('svg').remove()
        # Render new chart.
        d3.select(screenId).append('svg')
          .datum(datum)
          .call(chart)

        # Update the chart when window resizes.
        nv.utils.windowResize () -> chart.update()
        chart;

    transform: (dataset) ->
      # Transform list of objects into series of list.
      values =
        s200: []
        s300: []
        s400: []
        s500: []
      for t in dataset
        day = moment(t.day)
        l = ([parseInt(k, 10), v] for k, v of t.status)
        for i in [200, 300, 400, 500]
          r = l.filter((x) -> x[0] >= i and x[0] < i + 100)
          if r.length > 0
            values['s' + i].push [day, (x[1] for x in r).reduce (x, y) -> x + y]
          else
            values['s' + i].push [day, 0]
      values

    load: (source, page) ->
      # Clear internal memory when the first page is requested.
      if !page
        @dataset = []
      url = @url + '/api/stats/daily/'
      page = page or 1
      params =
        source: source
        page_size: 100
        ordering: 'day'
        page: page
      self = this
      $.ajax(
        type: 'GET'
        url: url
        data: params
      ).success (dt) ->
        # console.table dt.results
        self.dataset.push.apply(self.dataset, dt.results)
        if dt.next
          self.load(source, page + 1)
        else
          values = self.transform self.dataset
          self.render [
            { key: '20x', values: values.s200 }
            { key: '30x', values: values.s300 }
            { key: '40x', values: values.s400 }
            { key: '50x', values: values.s500 }
          ]

  class LatestRecords
    constructor: (@url, @screen) ->

    load: (source) ->
      c = new LogRecordCollection
      c.root = @url + '/api/log/'
      v = new LogRecordView
                el: @screen
                collection: c
                source: source
      c.fetch(
        data:
          source: source
      )

  class SideMenu
    constructor: (url, screen) ->
      @collection = new SideMenuCollection
      @collection.url = url + '/api/source/'
      @view = new SideMenuView
                el: screen
                collection: @collection
      @collection.fetch()

    change: (source) ->
      @view.render(source)

  root = 'http://localhost:8000/accesslog'
  sidemenu = new SideMenu root, '#sidemenu'
  graph = new GraphWrapper root, '#chart'
  latest = new LatestRecords root, '#latest'
  new LogRecordRouter (source) ->
    sidemenu.change(source)
    graph.load(source)
    latest.load(source)
