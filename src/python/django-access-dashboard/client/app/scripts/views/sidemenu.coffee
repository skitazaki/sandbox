define [
  'jquery'
  'underscore'
  'backbone'
  'templates'
], ($, _, Backbone, JST) ->
  class SidemenuView extends Backbone.View
    template: JST['app/scripts/templates/sidemenu.ejs']

    tagName: 'div'

    id: ''

    className: ''

    events: {}

    initialize: () ->
      @listenTo @collection, 'sync', @render

    render: (source) ->
      @$el.html @template collection: @collection, current: source
