define [
  'underscore'
  'backbone'
  'models/logrecord'
], (_, Backbone, LogrecordModel) ->

  class LogrecordCollection extends Backbone.Collection
    model: LogrecordModel

    url: -> @next or @root

    parse: (response, options) ->
      @next = response.next
      response.results
