package swm.group18.healthcare.utils;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import javax.servlet.http.HttpServletRequest;
import java.io.BufferedReader;
import java.io.IOException;

public class RequestUtil {
    public static JSONObject readJSONFromRequest(HttpServletRequest request) throws IOException {
        JSONObject jsonObject = null;
        StringBuilder sb = new StringBuilder();
        BufferedReader reader = request.getReader();
        try {
            String line;
            while ((line = reader.readLine()) != null) {
                sb.append(line).append('\n');
            }
            JSONParser parser = new JSONParser();
            jsonObject = (JSONObject) parser.parse(sb.toString());
        }
        catch (ParseException e) {
            e.printStackTrace();
        }
        finally {
            reader.close();
        }

        return jsonObject;
    }
}
