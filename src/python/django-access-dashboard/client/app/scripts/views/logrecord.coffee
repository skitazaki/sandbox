define [
  'jquery'
  'underscore'
  'backbone'
  'templates'
], ($, _, Backbone, JST) ->
  class LogrecordView extends Backbone.View
    template: JST['app/scripts/templates/logrecord.ejs']

    tagName: 'div'

    id: ''

    className: ''

    events: {}

    initialize: (options) ->
      options = options or {}
      @source = options.source
      _.bindAll this, 'render'
      # Triggered after fetching successfully.
      @listenTo @collection, 'sync', @render

    render: () ->
      params =
        collection: @collection.toJSON()
        source: @source
      @$el.html @template params
