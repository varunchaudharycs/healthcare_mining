package swm.group18.healthcare.searcher;

import org.apache.solr.client.solrj.SolrClient;
import org.apache.solr.client.solrj.SolrServerException;
import org.apache.solr.client.solrj.impl.HttpSolrClient;
import org.apache.solr.client.solrj.response.QueryResponse;
import org.apache.solr.common.SolrDocument;
import org.apache.solr.common.SolrDocumentList;
import org.apache.solr.common.params.MapSolrParams;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import swm.group18.healthcare.utils.LoggerUtil;

import java.io.IOException;
import java.util.*;

public class WebMDMessageBoardsDataSearcher {
    private static final SolrClient client = new HttpSolrClient.Builder("http://localhost:8983/solr/webmd_mb_core").build();

    public static JSONArray search(SearchQuery searchQuery) {
        System.out.println(searchQuery.getQueryString());
//        JSONObject responseObj = new JSONObject();
        JSONArray resultsArray = new JSONArray();
        final Map<String, String> queryParamMap = new HashMap<>();
//        queryParamMap.put("q", "health_condition_name:" + searchQuery.getQueryString() + "*");
        System.out.println("Symptoms fielded query - " + searchQuery.getMultiValuedSymptomsQuery());
        queryParamMap.put("q", searchQuery.getMultiValuedSymptomsQuery() +
                " OR post_title:" + searchQuery.getQueryString()
//                " OR post_content:" + searchQuery.getQueryString() +
//                " OR responses:" + searchQuery.getQueryString()
        );
//        queryParamMap.put("q.op", "OR");
        queryParamMap.put("fl", "post_title, post_url, post_content, symptoms, diseases");
        queryParamMap.put("start", "0");
        queryParamMap.put("rows", "20");
//        queryParamMap.put("sort", "id asc");
        MapSolrParams queryParams = new MapSolrParams(queryParamMap);

        final QueryResponse response;
        try {
            response = client.query(queryParams);
            final SolrDocumentList documents = response.getResults();
            LoggerUtil.logDebugMsg("Found " + documents.getNumFound() + " documents");

            Set<String> drugsAlreadyInResults = new HashSet<>();
//            JSONArray resultsArray = new JSONArray();
            for(SolrDocument document : documents) {
                JSONObject result = new JSONObject();
                final String postTitle = (String) document.getFirstValue("post_title");
                if (!drugsAlreadyInResults.contains(postTitle)) {
                    final String postUrl = (String) document.getFirstValue("post_url");
                    final String summary = (String) document.getFirstValue("post_content");

                    Collection<Object> otherSymptoms = document.getFieldValues("symptoms");
                    JSONArray otherSympArray = new JSONArray();
                    if (otherSymptoms != null) {
                        for (Object symp: otherSymptoms) {
                            otherSympArray.add(symp);
                        }
                    }

                    result.put("title", postTitle);
                    result.put("url", postUrl);
                    result.put("summary", summary);
                    result.put("other_symptoms", otherSympArray);
                    resultsArray.add(result);

                    drugsAlreadyInResults.add(postTitle);
                }
            }

//            responseObj.put("web_md_mb", resultsArray);
            return resultsArray;
        } catch (SolrServerException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return resultsArray;
    }
}
