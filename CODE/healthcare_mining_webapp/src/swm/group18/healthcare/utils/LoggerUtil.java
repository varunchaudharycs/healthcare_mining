package swm.group18.healthcare.utils;

import swm.group18.healthcare.constants.GlobalConstants;

public class LoggerUtil {
    public static void logDebugMsg(final String msg) {
        if (GlobalConstants.IS_DEBUG_MODE_ENABLED) {
            System.out.println(msg);
        }
    }

    public static void logException(final String msg, Throwable t) {
        if (GlobalConstants.IS_DEBUG_MODE_ENABLED) {
            System.out.println(msg);
        }
    }
}
