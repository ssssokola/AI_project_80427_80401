package twitterMining.server;

import java.util.HashMap;
import twitter4j.Query;
import twitter4j.QueryResult;
import twitter4j.Tweet;
import twitter4j.Twitter;
import twitter4j.TwitterFactory;
import uk.ac.wlv.sentistrength.*;


public class GreetingServiceImpl {

	String found_tweets = "";
	String[] sentiStrengthArgs = new String[4];

	private final static int PAGES = 3;
	
	private void sentiStrengthSetUp(){
		sentiStrengthArgs[0] = "sentidata";
		sentiStrengthArgs[1] = "";
		sentiStrengthArgs[2] = "text";
		sentiStrengthArgs[3] = "hello";
	}
	
	public GreetingServiceImpl(){
		sentiStrengthSetUp();
	}

	public HashMap<String, Integer> greetServer(String input) throws IllegalArgumentException {

		int resultNegative = 0;
		int resultPossitive = 0;

		for(int i = 0; i < 6; i++) {
			Twitter twitter = new TwitterFactory().getInstance();
			Query query = new Query(input);
			query.setRpp(100);
			try {
				for (int page = 1; page <= PAGES; page++) {
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

						resultNegative += neg_res;
						resultPossitive += pos_res;
						
					}
				}
			} catch (Exception ex) {
				break;
			}
		}
		
		HashMap<String, Integer> resultMap = new HashMap<String, Integer>();
		resultMap.put("resultPossitive", resultPossitive);
		resultMap.put("resultNegative", resultNegative);
		
		return resultMap;
	}

	public HashMap<String, Integer> greetServerSentence(String sentence)
			throws IllegalArgumentException {
		
		SentiStrength.main(sentiStrengthArgs);
		SentiStrength classifier1 = new SentiStrength();
		String result_from_classifier1 = classifier1.computeSentimentScores(sentence);
		int pos_res = Integer.parseInt(result_from_classifier1.split(" ")[0]);
		int neg_res = Integer.parseInt(result_from_classifier1.split(" ")[1]);

		HashMap<String, Integer> resultMap = new HashMap<String, Integer>();
		resultMap.put("resultPossitive", pos_res);
		resultMap.put("resultNegative", neg_res);
		return resultMap;
	}
	
}