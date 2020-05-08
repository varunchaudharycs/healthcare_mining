package swm.group18.healthcare.indexer;

import org.apache.solr.client.solrj.SolrClient;
import org.apache.solr.client.solrj.SolrServerException;
import org.apache.solr.client.solrj.impl.HttpSolrClient;
import org.apache.solr.common.SolrInputDocument;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import swm.group18.healthcare.utils.JSONUtil;
import swm.group18.healthcare.utils.LoggerUtil;

import java.io.IOException;

// TODO: handle concurrency issues
public class WebMDMessageBoardsDataIndexer {
    private static final SolrClient client = new HttpSolrClient.Builder("http://localhost:8983/solr/webmd_mb_core").build();

    public static void indexPost(JSONObject jsonObject) throws IOException, SolrServerException {
//        System.out.println(jsonObject);
        SolrInputDocument doc = new SolrInputDocument();
        doc.addField("author", jsonObject.get("author").toString());
        doc.addField("post_title", jsonObject.get("post_title").toString());
        doc.addField("post_url", JSONUtil.unescape(jsonObject.get("post_url").toString()));
        doc.addField("post_time", jsonObject.get("post_time").toString());
        doc.addField("post_content", jsonObject.get("post_content").toString());
        doc.addField("responses", jsonObject.get("response_text").toString());
        doc.addField("like_count", jsonObject.get("like_count"));

        if (jsonObject.containsKey("tags")) {
            JSONArray tags = (JSONArray) jsonObject.get("tags");
            for (int i = 0; i < tags.size(); i++) {
                doc.addField("tags", tags.get(i).toString());
            }
        }

        if (jsonObject.containsKey("symptoms")) {
            JSONArray symptoms = (JSONArray) jsonObject.get("symptoms");
            for (int i = 0; i < symptoms.size(); i++) {
                doc.addField("symptoms", symptoms.get(i).toString());
            }
        }

        if (jsonObject.containsKey("diseases")) {
            JSONArray diseases = (JSONArray) jsonObject.get("diseases");
            for (int i = 0; i < diseases.size(); i++) {
                doc.addField("diseases", diseases.get(i).toString());
            }
        }

        if (jsonObject.containsKey("diagnostic_procedures")) {
            JSONArray diagnostic_procedures = (JSONArray) jsonObject.get("diagnostic_procedures");
            for (int i = 0; i < diagnostic_procedures.size(); i++) {
                doc.addField("diagnostic_procedures", diagnostic_procedures.get(i).toString());
            }
        }

        client.add(doc);
        GlobalIndexedDocsCounter.incrementDocCounter();

//        to index forum comments using parent child document to ensure whenever there is a match
//        even in the comment/reply the actual post result comes as search result
//        SolrInputDocument child1 = new SolrInputDocument();
//        child1.addField("id", "1");
//        child1.addField("author", "hemant");
//        child1.addField("resp_title", "this is awesome");
//        child1.addField("resp_content", "this is gonna be fun.");
//        child1.addField("post_title", "superb");
//        child1.addField("post_content", "awesome");
//
//        doc.addChildDocument(child1);

        if (GlobalIndexedDocsCounter.commitThresholdReached()) {
            commit();
        }
    }

    public static void commit() throws IOException, SolrServerException {
        client.commit();
        LoggerUtil.logDebugMsg("Index committed after indexing: " + GlobalIndexedDocsCounter.numberOfIndexedDocuments
                + " new documents");
    }
}
