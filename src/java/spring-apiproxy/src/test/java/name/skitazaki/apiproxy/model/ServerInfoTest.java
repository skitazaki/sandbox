package name.skitazaki.apiproxy.model;

import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.CoreMatchers.nullValue;
import static org.junit.Assert.assertThat;

import org.junit.Before;
import org.junit.Test;

public class ServerInfoTest {

	private ServerInfo info;

	@Before
	public void setUp() throws Exception {
		info = new ServerInfo();
	}

	@Test
	public void testSetAndGetName() {
		String name = "solr";
		assertThat(info.getName(), nullValue());
		info.setName(name);
		assertThat(info.getName(), is(name));
		// XXX: Long text to set
	}

	@Test
	public void testSetAndGetKind() {
		String kind = "static";
		assertThat(info.getKind(), nullValue());
		info.setKind(kind);
		assertThat(info.getKind(), is(kind));
		// XXX: Long text to set
	}

	@Test
	public void testSetAndGetUrl() {
		String url = "http://localhost:8983/solr";
		assertThat(info.getUrl(), nullValue());
		info.setUrl(url);
		assertThat(info.getUrl(), is(url));
		// XXX: Long text to set
	}

	@Test
	public void testSetAndGetDefaults() {
		String defaults = "a=b&c=d";
		assertThat(info.getDefaults(), nullValue());
		info.setDefaults(defaults);
		assertThat(info.getDefaults(), is(defaults));
		// XXX: Long text to set
	}

	@Test
	public void testSetAndGetResponseClass() {
		String responseClass = "name.skitazaki.apiproxy.model.SolrResponse";
		assertThat(info.getResponseClass(), nullValue());
		info.setConverter(responseClass);
		assertThat(info.getResponseClass(), is(responseClass));
		// XXX: Long text to set
	}
}
