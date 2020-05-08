package swm.group18.healthcare.searcher;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import swm.group18.healthcare.utils.LoggerUtil;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.List;

public class AnnotateUsingMetaMap {
    private static final String META_MAP_PYTHON_SERVER_URL = "http://localhost:8008";

    public static SearchQuery annotateQuery(String searchStr) {
        SearchQuery searchQuery = new SearchQuery(searchStr);
        try {
            String responseStr = performGetRequest(META_MAP_PYTHON_SERVER_URL, "query=" +  URLEncoder.encode(searchStr, "UTF-8") );
            if (responseStr != null) {
                JSONParser parser = new JSONParser();
                JSONObject jsonObject = (JSONObject) parser.parse(responseStr);
                if (jsonObject.containsKey("diseases")) {
                    JSONArray diseaseArray = (JSONArray) jsonObject.get("diseases");
                    List<String> diseases = new ArrayList<>(diseaseArray.size());
                    for (int i = 0; i < diseaseArray.size(); i++) {
                        diseases.add(diseaseArray.get(i).toString());
                    }
                    searchQuery.setDiseases(diseases);
                }
                if (jsonObject.containsKey("symptoms")) {
                    JSONArray symptomsArray = (JSONArray) jsonObject.get("symptoms");
                    List<String> symptoms = new ArrayList<>(symptomsArray.size());
                    for (int i = 0; i < symptomsArray.size(); i++) {
                        symptoms.add(symptomsArray.get(i).toString());
                    }
                    searchQuery.setSymptoms(symptoms);
                }

                if (jsonObject.containsKey("symptoms_suggestion")) {
                    JSONArray symptomsSuggestionArr = (JSONArray) jsonObject.get("symptoms_suggestion");
                    List<String> relatedSymptoms = new ArrayList<>(symptomsSuggestionArr.size());
                    for (int i = 0; i < symptomsSuggestionArr.size(); i++) {
                        relatedSymptoms.add(symptomsSuggestionArr.get(i).toString());
                    }
                    searchQuery.setRelatedSymptoms(relatedSymptoms);
                }
            }
        } catch (ParseException e) {
            e.printStackTrace();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        return searchQuery;
    }

    public static String performGetRequest(String targetURL, String urlParameters) {
        HttpURLConnection connection = null;

        try {
            //Create connection
            URL url = new URL(targetURL + "?"+urlParameters);
            connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            connection.setRequestProperty("Content-Type",
                    "application/json");

            StringBuilder content;
            // Get the input stream of the connection
            BufferedReader input = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String line;
            content = new StringBuilder();
            while ((line = input.readLine()) != null) {
                // Append each line of the response and separate them
                content.append(line);
                content.append(System.lineSeparator());
            }
            return content.toString();

        } catch (Exception e) {
            LoggerUtil.logDebugMsg("Exception while connecting to meta map broker");
//            e.printStackTrace();
            return null;
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
    }
}
