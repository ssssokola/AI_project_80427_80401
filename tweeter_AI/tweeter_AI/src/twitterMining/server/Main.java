package twitterMining.server;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;

public class Main {

	/**
	 * @param args
	 * @throws Exception 
	 */
	public static void main(String[] args) throws Exception {
		for (String s: args) {
            System.out.println(s);
        }
		String input = "";
		if(args[0]!= null){
			input = args[0];
		}
		GreetingServiceImpl greetServiceObject = new GreetingServiceImpl();
		HashMap<String, Integer> result = greetServiceObject.greetServer(input);
		if(input.equals("")){
			throw new Exception("Grashka");
		}
//		try {
//			BufferedWriter out = new BufferedWriter(new FileWriter("C:/Users/petar/Desktop/fileOutputSentiStrength.txt"));
//			out.write(result);
//			out.close();
//		} catch (IOException e) {
//			System.out.println("Exception ");
//
//		}
		System.out.println("sdgffsdf7735340trgfgndfbgladsgkjlafgsfg4w5345fasdgdfgkdsnJJJJJJfdsgfd\n");
		
		System.out.println(result.get("resultEvulation"));
		System.out.println(result.get("resultPossitive"));
		System.out.println(result.get("resultNegative"));
		System.out.println(result.get("counter"));
		
	}

}
