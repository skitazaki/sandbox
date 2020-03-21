package name.skitazaki.apiproxy.service;

import java.util.List;

import name.skitazaki.apiproxy.model.ServerInfo;

public interface ServerInfoManager {

	List<ServerInfo> getConfigurations();

	ServerInfo getConfiguration(String name);
}
