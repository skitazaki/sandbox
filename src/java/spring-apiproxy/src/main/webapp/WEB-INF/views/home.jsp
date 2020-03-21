<%@ page session="false"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt"%>
<html>
<head>
<title><fmt:message key="title" /></title>
</head>
<body>
	<h1>
		<fmt:message key="heading" />
	</h1>
	<p>
		<fmt:message key="greeting">
			<fmt:param value="${serverTime}" />
		</fmt:message>
	</p>
	<ul>
		<li><a href="<c:url value="servers"/>"><fmt:message
					key="servers" /></a></li>
		<li><a href="<c:url value="proxy/solr"/>"><fmt:message
					key="proxy">
					<fmt:param value="Solr" />
				</fmt:message></a></li>
	</ul>
</body>
</html>
