package swm.group18.healthcare.servlets;

import org.json.simple.JSONObject;
import swm.group18.healthcare.constants.GlobalConstants;
import swm.group18.healthcare.indexer.MayoClinicDataIndexer;
import swm.group18.healthcare.indexer.PatientInfoDataIndexer;
import swm.group18.healthcare.indexer.WebMDDrugReviewDataIndexer;
import swm.group18.healthcare.indexer.WebMDMessageBoardsDataIndexer;
import swm.group18.healthcare.utils.LoggerUtil;
import swm.group18.healthcare.utils.RequestUtil;
import swm.group18.healthcare.utils.ResponseUtil;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

public class IndexRequestHandler extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        this.processIndexRequest(req, resp);
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        this.processIndexRequest(req, resp);
    }

    private void processIndexRequest(HttpServletRequest request, HttpServletResponse response) throws IOException {
        final String indexRequestType = request.getParameter("type");
        LoggerUtil.logDebugMsg("Index request received with type: " + indexRequestType);

        JSONObject jsonObject = RequestUtil.readJSONFromRequest(request);
//        not an empty json in index request => index data
//        TODO: don't index docs which does not have any of the symptom or diag or disease
        if (!jsonObject.isEmpty()) {
            try {
                switch (indexRequestType) {
                    case GlobalConstants.DRUG_REVIEW_INDEX_REQUEST:
                        WebMDDrugReviewDataIndexer.indexPost(jsonObject);
                        break;
                    case GlobalConstants.WEBMD_MB_INDEX_REQUEST:
                        WebMDMessageBoardsDataIndexer.indexPost(jsonObject);
                        break;
                    case GlobalConstants.MAYO_DISEASE_DESC_INDEX_REQUEST:
                        MayoClinicDataIndexer.indexPost(jsonObject);
                        break;
                    case GlobalConstants.PATIENT_INFO_INDEX_REQUEST:
                        PatientInfoDataIndexer.indexPost(jsonObject);
                        break;
                    case GlobalConstants.INDEX_COMMIT_REQUEST:
                        MayoClinicDataIndexer.commit();
                        PatientInfoDataIndexer.commit();
                        WebMDDrugReviewDataIndexer.commit();
                        WebMDMessageBoardsDataIndexer.commit();
                        break;
                }

                ResponseUtil.sendIndexSuccessMessage(response);

            } catch (Exception e) {
//                e.printStackTrace();
                LoggerUtil.logException("Exception while processing index request", e);
                ResponseUtil.sendIndexErrorMessage(response);
            }

        }

        LoggerUtil.logDebugMsg("Index request completed");
    }
}
