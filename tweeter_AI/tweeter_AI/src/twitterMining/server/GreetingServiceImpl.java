package twitterMining.server;

import java.io.File;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.HashMap;

import twitter4j.Query;
import twitter4j.QueryResult;
import twitter4j.Tweet;
import twitter4j.Twitter;
import twitter4j.TwitterFactory;
import uk.ac.wlv.sentistrength.*;


/**
 * The server side implementation of the RPC service.
 */
@SuppressWarnings("serial")
public class GreetingServiceImpl {
	public HashMap greetServer(String input) throws IllegalArgumentException {

		String found_tweets = "";
		String[] sentiStrengthArgs = new String[4];
		sentiStrengthArgs[0] = "sentidata";
		sentiStrengthArgs[1] = "C:\\a\\SentiStrength_Data\\";
		sentiStrengthArgs[2] = "text";
		sentiStrengthArgs[3] = "hello";
		int resultEvulation = 0;
		int resultNegative = 0;
		int resultPossitive = 0;
		int counter = 0;

		for (int i = 0; i < 6; i++) {
			Twitter twitter = new TwitterFactory().getInstance();
			Query query = new Query(input);
			query.setRpp(100);
			try {
				for (int page = 1; page <= 10; page++) {
					QueryResult result = twitter.search(query.page(page));
					found_tweets += Integer.toString(result.getTweets().size());
					for (Tweet tweet : result.getTweets()) {
						SentiStrength.main(sentiStrengthArgs);
						SentiStrength classifier1 = new SentiStrength();
						String result_from_classifier1 = classifier1
								.computeSentimentScores(tweet.getText());
						int pos_res = Integer.parseInt(result_from_classifier1
								.split(" ")[0]);
						int neg_res = Integer.parseInt(result_from_classifier1
								.split(" ")[1]);

//						found_tweets += Math.abs(pos_res) - Math.abs(neg_res)+ ";"
//								+Math.abs(pos_res) +";"+ Math.abs(neg_res)
//								+ ";" + tweet.getFromUser() + ";"
//								+ tweet.getText() + "\n\n";
						resultEvulation += Math.abs(pos_res) - Math.abs(neg_res);
						resultNegative +=neg_res;
						resultPossitive +=pos_res;
						counter++;
					}
				}
			} catch (Exception ex) {
				break;
				// found_tweets = ex.toString();
				// log.setLevel(Level.INFO);
				// log.info(ex.toString());
			}
		}
		// Escape data from the client to avoid cross-site script
		// vulnerabilities.
		
		
//		input = escapeHtml(input);
//		found_tweets = escapeHtml(found_tweets);
//		return found_tweets;
		HashMap<String, Integer> resultMap =  new HashMap<String, Integer>();
		resultMap.put("resultEvulation", resultEvulation);
		resultMap.put("resultNegative", resultNegative);
		resultMap.put("resultPossitive", resultPossitive);
		resultMap.put("counter", counter);
		return resultMap;

	}

	/**
	 * Escape an html string. Escaping data received from the client helps to
	 * prevent cross-site script vulnerabilities.
	 * 
	 * @param html
	 *            the html string to escape
	 * @return the escaped string
	 */
	private String escapeHtml(String html) {
		if (html == null) {
			return null;
		}
		return html.replaceAll("&", "&amp;").replaceAll("<", "&lt;")
				.replaceAll(">", "&gt;");
	}
}