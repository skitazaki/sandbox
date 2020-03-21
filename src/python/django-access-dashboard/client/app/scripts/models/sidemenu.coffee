define [
  'underscore'
  'backbone'
], (_, Backbone) ->
  'use strict';

  class SidemenuModel extends Backbone.Model
    url: '',

    initialize: () ->

    defaults: {}

    validate: (attrs, options) ->

    parse: (response, options) ->
      response
