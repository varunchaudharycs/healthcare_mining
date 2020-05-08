package swm.group18.healthcare.indexer;

import org.apache.solr.client.solrj.SolrClient;
import org.apache.solr.client.solrj.SolrServerException;
import org.apache.solr.client.solrj.impl.HttpSolrClient;
import org.apache.solr.common.SolrInputDocument;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import swm.group18.healthcare.utils.LoggerUtil;

import java.io.IOException;

public class MayoClinicDataIndexer {
    private static final SolrClient client = new HttpSolrClient.Builder("http://localhost:8983/solr/mayo_clinic_core").build();

    public static void indexPost(JSONObject jsonObject) throws IOException, SolrServerException {
        SolrInputDocument doc = new SolrInputDocument();
        doc.addField("health_condition", jsonObject.get("health_condition").toString());
        doc.addField("page_url", jsonObject.get("page_url").toString());
        doc.addField("symptoms_text", jsonObject.get("symptoms_text").toString());

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
