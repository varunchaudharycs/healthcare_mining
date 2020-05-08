package swm.group18.healthcare.servlets;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import swm.group18.healthcare.constants.GlobalConstants;
import swm.group18.healthcare.searcher.*;
import swm.group18.healthcare.utils.LoggerUtil;
import swm.group18.healthcare.utils.ResponseUtil;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

public class SearchRequestHandler extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        this.processSearchRequest(req, resp);
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        this.processSearchRequest(req, resp);
    }

    private void processSearchRequest(HttpServletRequest request, HttpServletResponse response) throws IOException {

        String queryStr = request.getParameter("query");
//        drug_search - user has typed some disease name looking for related drugs as search results
//        disease_search - user has typed some symptoms and looking for related diseases as search results
        String searchType = request.getParameter("type");

        LoggerUtil.logDebugMsg("user search in: " + searchType + " and the query was: " + queryStr);
        ResponseUtil.setDefaultResponseHeaders(response);


        if (searchType.equalsIgnoreCase(GlobalConstants.DISEASE_SEARCH_REQUEST)) {
            // first extract annotated details from query
            SearchQuery searchQuery = AnnotateUsingMetaMap.annotateQuery(queryStr);
            LoggerUtil.logDebugMsg(searchQuery.toString());
            // search in all three solr cores

            JSONObject searchResults = new JSONObject();
            JSONArray mayoClinicResults = MayoClinicDataSearcher.search(searchQuery);
            searchResults.put("mayo_clinic", mayoClinicResults);
            JSONArray webMDMBResults = WebMDMessageBoardsDataSearcher.search(searchQuery);
            searchResults.put("web_md_mb", webMDMBResults);
            JSONArray patientInfoResults = PatientInfoDataSearcher.search(searchQuery);
            searchResults.put("patient_info", patientInfoResults);

            JSONObject searchResponse = new JSONObject();
            searchResponse.put("query", searchQuery.getQueryString());
            searchResponse.put("search_type", searchType);
            searchResponse.put("results", searchResults);
            searchResponse.put("tagged_symptoms", searchQuery.getTaggedymptomsJSONArray());
            searchResponse.put("related_symptoms", searchQuery.getRelatedSymptomsJSONArray());
            ResponseUtil.sendSearchResponse(response, searchResponse);
        } else if (searchType.equalsIgnoreCase(GlobalConstants.DRUG_SEARCH_REQUEST)) {
            // search in drug review core only
            SearchQuery searchQuery = new SearchQuery(queryStr);
            JSONObject searchResponse = WebMDDrugReviewDataSearcher.search(searchQuery);
            searchResponse.put("query", searchQuery.getQueryString());
            searchResponse.put("search_type", searchType);
            ResponseUtil.sendSearchResponse(response, searchResponse);
        }
    }
}
