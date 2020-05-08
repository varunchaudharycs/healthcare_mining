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


// TODO: we need to handle date range using NLP date tagger - https://nlp.stanford.edu/software/sutime.html
public class WebMDDrugReviewDataIndexer {
    private static final SolrClient client = new HttpSolrClient.Builder("http://localhost:8983/solr/webmd_dr_core").build();
//    private static final SimpleDateFormat DATE_FORMATTER = new SimpleDateFormat("MM/dd/yyyy HH:mm:ss a");
//    private static final SimpleDateFormat SOLR_DATE_FORMATTER = new SimpleDateFormat("yyyy-mm-ddThh:mm:ssZ");

    public static void indexPost(JSONObject jsonObject) throws IOException, SolrServerException, ParseException {
//        System.out.println(jsonObject);
        SolrInputDocument doc = new SolrInputDocument();
        doc.addField("drug_name", jsonObject.get("drug_name").toString());
        doc.addField("health_condition_name", jsonObject.get("health_condition_name").toString());
        doc.addField("drug_detail_page", JSONUtil.unescape(jsonObject.get("drug_detail_page").toString()));
        doc.addField("drug_review_page", JSONUtil.unescape(jsonObject.get("drug_review_page").toString()));
        doc.addField("patient_gender", jsonObject.get("patient_gender").toString());
        doc.addField("reviewer_name", jsonObject.get("reviewer_name").toString());
        doc.addField("reviewer_category", jsonObject.get("reviewer_category").toString());
        doc.addField("review_comment", jsonObject.get("review_comment").toString());
        SimpleDateFormat DATE_FORMATTER = new SimpleDateFormat("MM/dd/yyyy HH:mm:ss a");
//        SimpleDateFormat SOLR_DATE_FORMATTER = new SimpleDateFormat("yyyy-mm-dd hh:mm:ssZ");
        Date parsedDate = DATE_FORMATTER.parse(jsonObject.get("timestamp").toString());
        doc.addField("timestamp", parsedDate.getTime());
        doc.addField("treatment_duration", JSONUtil.unescape(jsonObject.get("treatment_duration").toString()));
        doc.addField("num_of_people_found_useful", jsonObject.get("num_of_people_found_useful"));
        doc.addField("patient_age_start", jsonObject.get("patient_age_start"));
        doc.addField("patient_age_end", jsonObject.get("patient_age_end"));
        doc.addField("effectiveness_rating", Integer.parseInt(jsonObject.get("effectiveness_rating").toString()));
        doc.addField("ease_of_use_rating", Integer.parseInt(jsonObject.get("ease_of_use_rating").toString()));
        doc.addField("satisfaction_rating", Integer.parseInt(jsonObject.get("satisfaction_rating").toString()));

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
