package swm.group18.healthcare.indexer;

import swm.group18.healthcare.utils.LoggerUtil;

public class GlobalIndexedDocsCounter {
    private static final int COMMIT_EVERY_NTH_DOC = 500;
    public static long numberOfIndexedDocuments = 0;

    public static void incrementDocCounter() {
        numberOfIndexedDocuments++;
        LoggerUtil.logDebugMsg("Doc count: "+ numberOfIndexedDocuments);
    }

    // commit after indexing 50 posts
    // need to send commit from client side otherwise the last few posts will be lost.
    public static boolean commitThresholdReached() {
        if (numberOfIndexedDocuments % COMMIT_EVERY_NTH_DOC == 0) {
            return true;
        }
        return false;
    }
}
