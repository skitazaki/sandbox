package name.skitazaki.apiproxy.repository;

import java.util.List;

import name.skitazaki.apiproxy.model.ServerInfo;

import org.hibernate.Criteria;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.criterion.Restrictions;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

@Repository
public class HibernateServerInfoDao implements ServerInfoDao {

	@Autowired
	private SessionFactory sessionFactory;

	public List<ServerInfo> getServers() {
		Session session = sessionFactory.getCurrentSession();
		Criteria criteria = session.createCriteria(ServerInfo.class);
		@SuppressWarnings("unchecked")
		List<ServerInfo> list = criteria.list();
		return list;
	}

	public ServerInfo getServer(String name) {
		Session session = sessionFactory.getCurrentSession();
		Criteria criteria = session.createCriteria(ServerInfo.class);
		criteria.add(Restrictions.eq("name", name));
		Object result = criteria.uniqueResult();
		if (result == null) {
			// XXX: LOG ME
			return null;
		}
		return (ServerInfo) result;
	}

	public void saveServer(ServerInfo s) {
		if (s == null) {
			return;

		}
		Session session = sessionFactory.getCurrentSession();
		session.persist(s);
	}
}
