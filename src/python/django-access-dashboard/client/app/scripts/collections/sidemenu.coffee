define [
  'underscore'
  'backbone'
  'models/sidemenu'
], (_, Backbone, SidemenuModel) ->

  class SidemenuCollection extends Backbone.Collection
    model: SidemenuModel

    parse: (response, options) ->
      response.results
