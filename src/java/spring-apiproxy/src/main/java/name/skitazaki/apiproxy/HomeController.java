package name.skitazaki.apiproxy;

import java.text.DateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

import javax.servlet.http.HttpServletRequest;

import name.skitazaki.apiproxy.model.ServerInfo;
import name.skitazaki.apiproxy.service.HttpRequestProxy;
import name.skitazaki.apiproxy.service.ServerInfoManager;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

/**
 * Handles requests for the application home page.
 */
@Controller
public class HomeController {

	private static final Logger logger = LoggerFactory
			.getLogger(HomeController.class);

	@Autowired
	private ServerInfoManager manager;

	@Autowired
	private HttpRequestProxy proxy;

	/**
	 * Simply selects the home view to render by returning its name.
	 */
	@RequestMapping(value = "/", method = RequestMethod.GET)
	public String home(Locale locale, Model model) {
		if (locale == null) {
			locale = Locale.getDefault();
		}
		logger.info("Welcome home! the client locale is " + locale.toString());

		Date date = new Date();
		DateFormat dateFormat = DateFormat.getDateTimeInstance(DateFormat.LONG,
				DateFormat.LONG, locale);

		String formattedDate = dateFormat.format(date);

		if (model != null) {
			model.addAttribute("serverTime", formattedDate);
		}

		return "home";
	}

	@RequestMapping(value = "/servers", method = RequestMethod.GET)
	@ResponseBody
	public List<ServerInfo> servers() {
		return manager.getConfigurations();
	}

	@RequestMapping(value = "/proxy/{server}", method = RequestMethod.GET)
	@ResponseBody
	public String proxy(@PathVariable String server, HttpServletRequest request) {
		String query = request.getQueryString();
		logger.info("Query: " + query);
		ServerInfo info = manager.getConfiguration(server);
		if (info == null) {
			throw new ResourceNotFoundException();
		}
		return proxy.proxy(info, query);
	}

	@ExceptionHandler(ResourceNotFoundException.class)
	@ResponseBody
	public ResourceNotFoundException handleIOException(
			ResourceNotFoundException ex, HttpServletRequest request) {
		// return ClassUtils.getShortName(ex.getClass());
		return ex;
	}
}
