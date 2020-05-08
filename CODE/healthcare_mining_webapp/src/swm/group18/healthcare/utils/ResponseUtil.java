package swm.group18.healthcare.utils;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import javax.servlet.ServletContext;
import javax.servlet.http.HttpServletResponse;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Map;

public class ResponseUtil {
    public static void setDefaultResponseHeaders(HttpServletResponse response) {
        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");
    }


    public static void sendDevJSONResponseForDiseaseSearch(ServletContext servletContext, HttpServletResponse response) {
        String respFilePath = servletContext.getRealPath("./WEB-INF/crawled_data/disease_search_development_resp.json");
        try {
            JSONParser parser = new JSONParser();
            JSONObject obj = (JSONObject) parser.parse(new FileReader(respFilePath));
            PrintWriter out = response.getWriter();
            out.write(obj.toJSONString());
            out.flush();
            out.close();
        } catch (Throwable e) {
            e.printStackTrace();
        }
    }

    public static void sendDevJSONResponseForDrugSearch(ServletContext servletContext, HttpServletResponse response) {
        String respFilePath = servletContext.getRealPath("./WEB-INF/crawled_data/drug_search_development_resp.json");
        try {
            JSONParser parser = new JSONParser();
            JSONObject obj = (JSONObject) parser.parse(new FileReader(respFilePath));
            PrintWriter out = response.getWriter();
            out.write(obj.toJSONString());
            out.flush();
            out.close();
        } catch (Throwable e) {
            e.printStackTrace();
        }
    }

    public static void sendSearchResponse(HttpServletResponse response, JSONObject respObj) throws IOException {
        setDefaultResponseHeaders(response);
        response.setStatus(200);
        PrintWriter out = response.getWriter();
        out.write(respObj.toJSONString());
        out.flush();
        out.close();
    }

    public static void sendIndexSuccessMessage(HttpServletResponse response) throws IOException {
        setDefaultResponseHeaders(response);
        response.setStatus(200);
        Map<String, String> success = new HashMap<>();
        success.put("status", "success");
        JSONObject respObj = new JSONObject(success);

        PrintWriter out = response.getWriter();
        out.write(respObj.toJSONString());
        out.flush();
        out.close();
    }

    public static void sendIndexErrorMessage(HttpServletResponse response) throws IOException {
        setDefaultResponseHeaders(response);
        response.setStatus(500);
        Map<String, String> success = new HashMap<>();
        success.put("status", "error");
        JSONObject respObj = new JSONObject(success);

        PrintWriter out = response.getWriter();
        out.write(respObj.toJSONString());
        out.flush();
        out.close();
    }
}
