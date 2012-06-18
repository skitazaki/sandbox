@Grab(group='org.codehaus.groovy.modules.http-builder', module='http-builder', version='0.5.2')
import groovyx.net.http.HTTPBuilder
import static groovyx.net.http.Method.GET
import static groovyx.net.http.ContentType.JSON
 
def http = new HTTPBuilder( 'http://ajax.googleapis.com' )

// perform a GET request, expecting JSON response data
http.request( GET, JSON ) {
  uri.path = '/ajax/services/search/web'
  uri.query = [ v:'1.0', q: 'groovy 使い方' ]

  headers.'User-Agent' = 'Mozilla/5.0 Ubuntu/8.10 Firefox/3.0.4'
  headers.'Accept-Charset' = 'utf-8'

  // response handler for a success response code:
  response.success = { resp, json ->
    println resp.statusLine

    // parse the JSON response object:
    json.responseData.results.each {
      // XXX: Encode with UTF-8, current output is Shift_JIS.
      println "- ${it.titleNoFormatting} : ${it.visibleUrl}"
    }
  }

  // handler for any failure status code:
  response.failure = { resp ->
    println "Unexpected error: ${resp.statusLine.statusCode} : ${resp.statusLine.reasonPhrase}"
  }
}
