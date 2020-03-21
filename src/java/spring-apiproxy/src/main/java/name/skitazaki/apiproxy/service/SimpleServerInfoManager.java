package name.skitazaki.apiproxy.service;

import java.util.List;

import name.skitazaki.apiproxy.model.ServerInfo;
import name.skitazaki.apiproxy.repository.ServerInfoDao;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class SimpleServerInfoManager implements ServerInfoManager {

	@Autowired
	private ServerInfoDao serverInfoDao;

	public List<ServerInfo> getConfigurations() {
		// XXX: implement cache support.
		return serverInfoDao.getServers();
	}

	public void setServerInfoDao(ServerInfoDao serverInfoDao) {
		this.serverInfoDao = serverInfoDao;
	}

	public ServerInfo getConfiguration(String name) {
		if (name == null || name.length() == 0) {
			return null;
		}
		return serverInfoDao.getServer(name);
	}
}
