package name.skitazaki.apiproxy.repository;

import static org.junit.Assert.*;
import static org.hamcrest.CoreMatchers.*;
import java.util.List;

import name.skitazaki.apiproxy.model.ServerInfo;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.AbstractTransactionalJUnit4SpringContextTests;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.transaction.TransactionConfiguration;
import org.springframework.transaction.annotation.Transactional;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration
@TransactionConfiguration
@Transactional
public class JdbcServerInfoDaoTest extends
		AbstractTransactionalJUnit4SpringContextTests {

	@Qualifier("jdbcDao")
	@Autowired
	private ServerInfoDao serverInfoDao;

	@Before
	public void setUp() throws Exception {
		super.executeSqlScript("file:db/schema.sql", false);
		super.executeSqlScript("file:db/test-data.sql", true);
	}

	@After
	public void tearDown() throws Exception {
		super.deleteFromTables("server_info");
	}

	@Test
	public void getServers() {
		List<ServerInfo> servers = serverInfoDao.getServers();
		assertThat("wrong number of servers?", servers.size(), is(6));
	}

	@Test
	public void getServer() {
		ServerInfo server1 = serverInfoDao.getServer("solr");
		assertThat(server1.getName(), is("solr"));
		assertThat(server1.getUrl(), is("http://localhost:8983/solr"));
		assertThat(server1.getDefaults(), nullValue());

		ServerInfo server2 = serverInfoDao.getServer("python");
		assertThat(server2.getName(), is("python"));
		assertThat(server2.getUrl(), is("http://localhost:8000"));
		assertThat(server2.getDefaults(), nullValue());
	}

	@Test
	public void saveServer() {
		List<ServerInfo> servers = serverInfoDao.getServers();
		for (ServerInfo p : servers) {
			p.setUrl("http://localhost");
			serverInfoDao.saveServer(p);
		}

		List<ServerInfo> updatedServers = serverInfoDao.getServers();
		for (ServerInfo p : updatedServers) {
			assertThat("wrong server url?", p.getUrl(), is("http://localhost"));
		}
	}
}
