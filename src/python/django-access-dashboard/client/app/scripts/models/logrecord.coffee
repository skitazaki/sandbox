define [
  'underscore'
  'backbone'
], (_, Backbone) ->
  'use strict';

  class LogrecordModel extends Backbone.Model
    url: '',

    initialize: () ->

    defaults: {}

    validate: (attrs, options) ->

    parse: (response, options) ->
      response
