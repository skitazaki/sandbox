package name.skitazaki.apiproxy.repository;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;

import name.skitazaki.apiproxy.model.ServerInfo;

import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcDaoSupport;

public class JdbcServerInfoDao extends NamedParameterJdbcDaoSupport implements
		ServerInfoDao {

	public List<ServerInfo> getServers() {
		List<ServerInfo> s = getJdbcTemplate().query(
				"SELECT * FROM server_info", new ServerInfoMapper());
		if (s != null) {
			logger.info("Fetched " + s.size() + " item(s).");
		}
		return s;
	}

	public ServerInfo getServer(String name) {
		ServerInfo s = getNamedParameterJdbcTemplate().queryForObject(
				"SELECT * FROM server_info WHERE name = :name",
				new MapSqlParameterSource().addValue("name", name),
				new ServerInfoMapper());
		return s;
	}

	public void saveServer(ServerInfo s) {
		logger.info("Save server info: " + s.getName());
		int updated = getNamedParameterJdbcTemplate()
				.update("UPDATE server_info SET name = :name, url = :url WHERE id = :id",
						new MapSqlParameterSource()
								.addValue("name", s.getName())
								.addValue("url", s.getUrl())
								.addValue("id", s.getId()));
		logger.info("Rows affected: " + updated);
	}

	private static class ServerInfoMapper implements RowMapper<ServerInfo> {

		public ServerInfo mapRow(ResultSet rs, int rowNum) throws SQLException {
			ServerInfo s = new ServerInfo();
			s.setId(rs.getInt("id"));
			s.setName(rs.getString("name"));
			s.setUrl(rs.getString("url"));
			return s;
		}
	}

}
