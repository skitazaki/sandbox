package name.skitazaki.apiproxy.service;

import static org.junit.Assert.*;
import static org.hamcrest.CoreMatchers.*;
import static org.springframework.test.web.client.match.RequestMatchers.method;
import static org.springframework.test.web.client.match.RequestMatchers.requestTo;
import static org.springframework.test.web.client.response.ResponseCreators.withSuccess;

import name.skitazaki.apiproxy.model.ServerInfo;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.support.AnnotationConfigContextLoader;
import org.springframework.test.web.client.MockRestServiceServer;
import org.springframework.web.client.RestTemplate;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(loader = AnnotationConfigContextLoader.class)
public class HttpRequestProxyTest {

	private MockRestServiceServer mockServer;

	@Autowired
	private RestTemplate restTemplate;

	@Configuration
	static class Config {

		@Bean
		public RestTemplate restTemplate() {
			RestTemplate restTemplate = new RestTemplate();
			return restTemplate;
		}

	}

	@Before
	public void setUp() throws Exception {
		this.mockServer = MockRestServiceServer.createServer(this.restTemplate);
	}

	@After
	public void tearDown() throws Exception {
		this.mockServer.verify();
	}

	@Test
	public void queryStringIsNull() {
		String url = "http://localhost:8983/solr";
		HttpRequestProxy proxy = new HttpRequestProxy(restTemplate);
		String responseBody = "{\"name\" : \"Ludwig van Beethoven\", \"someDouble\" : \"1.6035\"}";
		this.mockServer
				.expect(requestTo(url))
				.andExpect(method(HttpMethod.GET))
				.andRespond(
						withSuccess(responseBody, MediaType.APPLICATION_JSON));
		ServerInfo info = new ServerInfo();
		info.setUrl(url);
		String ret = proxy.proxy(info, null);
		assertThat(ret, is(responseBody));
	}

	@Test
	public void queryStringIsEmpty() {
		String url = "http://localhost:8983/solr";
		HttpRequestProxy proxy = new HttpRequestProxy(restTemplate);
		String responseBody = "{\"name\" : \"Ludwig van Beethoven\", \"someDouble\" : \"1.6035\"}";
		this.mockServer
				.expect(requestTo(url))
				.andExpect(method(HttpMethod.GET))
				.andRespond(
						withSuccess(responseBody, MediaType.APPLICATION_JSON));
		ServerInfo info = new ServerInfo();
		info.setUrl(url);
		String ret = proxy.proxy(info, "");
		assertThat(ret, is(responseBody));
	}

	@Test
	public void queryStringIsSearchWord() {
		String url = "http://localhost:8983/solr";
		HttpRequestProxy proxy = new HttpRequestProxy(restTemplate);
		String responseBody = "{\"name\" : \"Ludwig van Beethoven\", \"someDouble\" : \"1.6035\"}";
		this.mockServer
				.expect(requestTo(url + "?q=spring"))
				.andExpect(method(HttpMethod.GET))
				.andRespond(
						withSuccess(responseBody, MediaType.APPLICATION_JSON));
		ServerInfo info = new ServerInfo();
		info.setUrl(url);
		String ret = proxy.proxy(info, "q=spring");
		assertThat(ret, is(responseBody));
	}

}
