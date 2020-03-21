package name.skitazaki.apiproxy.repository;

import java.util.List;

import name.skitazaki.apiproxy.model.ServerInfo;

public interface ServerInfoDao {

	List<ServerInfo> getServers();

	ServerInfo getServer(String name);

	void saveServer(ServerInfo s);
}
