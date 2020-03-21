package name.skitazaki.apiproxy.service;

import name.skitazaki.apiproxy.model.ServerInfo;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.util.StringUtils;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

public class HttpRequestProxy {

	private static final Logger logger = LoggerFactory
			.getLogger(HttpRequestProxy.class);

	private RestTemplate restTemplate;

	@Autowired
	public HttpRequestProxy(RestTemplate restTemplate) {
		this.restTemplate = restTemplate;
	}

	public String proxy(ServerInfo info, String query) {
		String q = query == null ? "" : query;
		String defaults = info.getDefaults();
		if (StringUtils.hasText(defaults)) {
			q += "&" + defaults;
		}
		String url = info.getUrl();
		if (!url.contains("?")) {
			url += "?";
		}
		url += q;
		try {
			String ret = restTemplate.getForObject(url, String.class);
			//info.getResponseClass();
			return ret;
		} catch (RestClientException e) {
			logger.error("{} - {}", e.getMessage(), url);
		}
		return null;
	}

}
