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
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class PatientInfoDataIndexer {
    private static final SolrClient client = new HttpSolrClient.Builder("http://localhost:8983/solr/patient_info_forum_core").build();

    public static void indexPost(JSONObject jsonObject) throws IOException, SolrServerException, ParseException {
        SolrInputDocument doc = new SolrInputDocument();
        doc.addField("post_group", jsonObject.get("post_group").toString());
        doc.addField("post_title", jsonObject.get("post_title").toString());
        doc.addField("post_content", jsonObject.get("post_content").toString());
        doc.addField("post_url", JSONUtil.unescape(jsonObject.get("post_url").toString()));
        SimpleDateFormat dateFormatter = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm");
        Date parsedDate = dateFormatter.parse(jsonObject.get("post_time").toString());
        doc.addField("post_time", parsedDate.getTime());
        doc.addField("post_follow_count", jsonObject.get("post_follow_count"));
        doc.addField("post_like_count", jsonObject.get("post_like_count"));
        doc.addField("post_reply_count", jsonObject.get("post_reply_count"));
        doc.addField("post_author", jsonObject.get("post_author").toString());
        doc.addField("post_author_profile", jsonObject.get("post_author_profile").toString());
        doc.addField("post_comments", jsonObject.get("post_comments").toString());

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
