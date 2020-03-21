INSERT INTO server_info (id, name, kind, url, responseClass) values(1, 'solr', 'search', 'http://localhost:8983/solr', 'name.skitazaki.apiproxy.model.SolrResponse');
INSERT INTO server_info (id, name, kind, url) values(2, 'python', 'static', 'http://localhost:8000');
INSERT INTO server_info (id, name, kind, url) values(3, 'nodejs', 'webapp', 'http://localhost:4000');
INSERT INTO server_info (id, name, kind, url) values(4, 'tomcat', 'webapp', 'http://localhost:8080');
INSERT INTO server_info (id, name, kind, url) values(5, 'jetty', 'webapp', 'http://localhost:8983');
INSERT INTO server_info (id, name, kind, url, defaults) values(6, 'wikipedia', 'search', 'http://localhost:8983/solr/wikipedia', 'wt=json');
