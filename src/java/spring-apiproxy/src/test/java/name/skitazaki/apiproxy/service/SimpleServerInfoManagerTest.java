package name.skitazaki.apiproxy.service;

import static org.hamcrest.CoreMatchers.*;
import static org.junit.Assert.assertThat;

import java.util.List;

import name.skitazaki.apiproxy.model.ServerInfo;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.AbstractTransactionalJUnit4SpringContextTests;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.transaction.TransactionConfiguration;
import org.springframework.transaction.annotation.Transactional;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = "classpath:test-context.xml")
@TransactionConfiguration
@Transactional
public class SimpleServerInfoManagerTest extends
		AbstractTransactionalJUnit4SpringContextTests {

	@Autowired
	private ServerInfoManager manager;

	@Before
	public void setUp() throws Exception {
		super.executeSqlScript("file:db/test-data.sql", true);
	}

	@After
	public void tearDown() throws Exception {
		super.deleteFromTables("server_info");
	}

	@Test
	public void nullReturnsNull() {
		ServerInfo info = manager.getConfiguration(null);
		assertThat(info, nullValue());
	}

	@Test
	public void emptyReturnsNull() {
		ServerInfo info = manager.getConfiguration("");
		assertThat(info, nullValue());
	}

	@Test
	public void invalidReturnsNull() {
		ServerInfo info = manager.getConfiguration("unknown");
		assertThat(info, nullValue());
	}

	@Test
	public void one() {
		ServerInfo info = manager.getConfiguration("solr");
		assertThat(info, notNullValue());
		assertThat(info.getId(), is(1));
		assertThat(info.getName(), is("solr"));
		assertThat(info.getUrl(), is("http://localhost:8983/solr"));
		assertThat(info.getKind(), is("search"));
		assertThat(info.getDefaults(), nullValue());
		assertThat(info.getResponseClass(),
				is("name.skitazaki.apiproxy.model.SolrResponse"));
	}

	@Test
	public void all() {
		List<ServerInfo> list = manager.getConfigurations();
		assertThat(list, notNullValue());
		assertThat(list.size(), is(6));
		assertThat(list.get(0).getId(), is(1));
		assertThat(list.get(0).getName(), is("solr"));
		assertThat(list.get(0).getKind(), is("search"));
		assertThat(list.get(0).getUrl(), is("http://localhost:8983/solr"));
		assertThat(list.get(1).getId(), is(2));
		assertThat(list.get(1).getName(), is("python"));
		assertThat(list.get(1).getKind(), is("static"));
		assertThat(list.get(1).getUrl(), is("http://localhost:8000"));
		assertThat(list.get(1).getDefaults(), nullValue());
		assertThat(list.get(1).getResponseClass(), nullValue());
		assertThat(list.get(2).getId(), is(3));
		assertThat(list.get(2).getName(), is("nodejs"));
		assertThat(list.get(2).getKind(), is("webapp"));
		assertThat(list.get(2).getUrl(), is("http://localhost:4000"));
	}
}
