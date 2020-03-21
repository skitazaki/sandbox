define [
  'backbone'
], (Backbone) ->

  class LogrecordRouter extends Backbone.Router

    constructor: (@func) ->
      super

    routes:
      'source/:source': 'source'
      '*actions': 'defaultAction'

    initialize: ->
      Backbone.history.start()

    source: (source) ->
      @func source

    defaultAction: (actions) ->
      @func()
