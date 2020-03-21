package name.skitazaki.apiproxy;

import static org.hamcrest.CoreMatchers.*;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertThat;

import java.util.List;

import name.skitazaki.apiproxy.model.ServerInfo;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.AbstractTransactionalJUnit4SpringContextTests;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.transaction.TransactionConfiguration;
import org.springframework.transaction.annotation.Transactional;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = "classpath:test-context.xml")
@TransactionConfiguration
@Transactional
public class HomeControllerTest extends
		AbstractTransactionalJUnit4SpringContextTests {

	@Autowired
	private HomeController ctrl;

	@Before
	public void setUp() throws Exception {
		super.executeSqlScript("file:db/test-data.sql", true);
	}

	@After
	public void tearDown() throws Exception {
		super.deleteFromTables("server_info");
	}

	@Test
	public void home() {
		String home = ctrl.home(null, null);
		assertThat(home, is("home"));
	}

	@Test
	public void servers() {
		List<ServerInfo> servers = ctrl.servers();
		assertNotNull(servers);
		assertThat(servers.size(), is(6));
		ServerInfo r1 = servers.get(0);
		assertThat(r1.getId(), is(1));
		assertThat(r1.getName(), is("solr"));
		assertThat(r1.getUrl(), is("http://localhost:8983/solr"));
		ServerInfo r2 = servers.get(1);
		assertThat(r2.getId(), is(2));
		assertThat(r2.getName(), is("python"));
		assertThat(r2.getUrl(), is("http://localhost:8000"));
		ServerInfo r3 = servers.get(2);
		assertThat(r3.getId(), is(3));
		assertThat(r3.getName(), is("nodejs"));
		assertThat(r3.getUrl(), is("http://localhost:4000"));
		ServerInfo r6 = servers.get(5);
		assertThat(r6.getId(), is(6));
		assertThat(r6.getName(), is("wikipedia"));
		assertThat(r6.getUrl(), is("http://localhost:8983/solr/wikipedia"));
		assertThat(r6.getDefaults(), is("wt=json"));
	}

	@Test
	public void proxy() {
		MockHttpServletRequest request = new MockHttpServletRequest();
		String ret = ctrl.proxy("solr", request);
		assertNull(ret);
	}

	@Test(expected = ResourceNotFoundException.class)
	public void proxyNotFound() {
		MockHttpServletRequest request = new MockHttpServletRequest();
		ctrl.proxy("not_found", request);
	}
}
