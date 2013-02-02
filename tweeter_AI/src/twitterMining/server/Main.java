package twitterMining.server;

import java.util.HashMap;

public class Main {

	/**
	 * @param args
	 * @throws Exception
	 */
	public static void main(String[] args) throws Exception {
		GreetingServiceImpl greetServiceObject = new GreetingServiceImpl();
		String input = "";
		if (args[0] != null) {
			input = args[0];
		}
		if (args.length == 1) {
			HashMap<String, Integer> result = greetServiceObject
					.greetServer(input);
			if (input.equals("")) {
				throw new Exception("Grashka");
			}
			System.out.println(result.get("resultPossitive"));
			System.out.println(result.get("resultNegative"));

		} else {
			HashMap<String, Integer> result = greetServiceObject
					.greetServerSentence(input);
			System.out.println(result.get("resultPossitive"));
			System.out.println(result.get("resultNegative"));
			

		}

	}

}
