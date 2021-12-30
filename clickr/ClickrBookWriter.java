import java.awt.event.KeyEvent;
import java.util.List;
import java.util.Arrays;
import java.awt.Robot;
import java.awt.AWTException;
import java.lang.SecurityException;
import java.util.Random;
import java.awt.event.InputEvent;
import java.awt.datatransfer.StringSelection;
import java.awt.Toolkit;
import java.awt.datatransfer.Clipboard;

/**
 * An enum mapping formatting codes in Minecraft to their KeyEvent.
 * <p>
 * FC stands for FormattingCode, I save myself a longer list later with this abbreviation.
 */
enum FC {
    BLACK(KeyEvent.VK_0), DARK_BLUE(KeyEvent.VK_1), DARK_GREEN(KeyEvent.VK_2), DARK_AQUA(KeyEvent.VK_3),
    DARK_RED(KeyEvent.VK_4), DARK_PURPLE(KeyEvent.VK_5), GOLD(KeyEvent.VK_6), GRAY(KeyEvent.VK_7),
    DARK_GRAY(KeyEvent.VK_8), BLUE(KeyEvent.VK_9), GREEN(KeyEvent.VK_A), AQUA(KeyEvent.VK_B),
    RED(KeyEvent.VK_C), LIGHT_PURPLE(KeyEvent.VK_D), YELLOW(KeyEvent.VK_E), WHITE(KeyEvent.VK_F);
    // minecoin_gold which uses formatting code G is Bedrock Edition only.

    private final Integer key;

    FC(Integer key) {
        this.key = key;
    }

    Integer getKey() {
        return this.key;
    }
}

public class ClickrBookWriter {
    // Some constants for the program to sample from.
    final static String FORMATTING_CODE = "§";
    final static List<String> BLOCK_ELEMENTS = Arrays.asList("▖▗▘▙▚▛▜▝▞▟".split(""));
    final static String MEDIUM_SHADE_BLOCK = "▒";
    final static String FULL_BLOCK = "█";
    final static List<FC> NON_WHITE_FORMATTING_CODES = List.of(FC.BLACK, FC.DARK_BLUE, FC.DARK_GREEN, FC.DARK_AQUA,
        FC.DARK_RED, FC.DARK_PURPLE, FC.GOLD, FC.GRAY,
        FC.DARK_GRAY, FC.BLUE, FC.GREEN, FC.AQUA,
        FC.RED, FC.LIGHT_PURPLE, FC.YELLOW); // Everything except white, worth remixing to specific colors!
    final static int PAGES = 97; // There are 97 pages in total in this book.
    final static int THRESHOLD_PAGE = 8;
    final static int ART_CHARACTERS = 90; // How many characters to create of art in the beginning.

    /**
     * A helper method to take one random element from a generic list given a random object.
     */
    private static <E> E takeRandom(List<E> list, Random random) {
        return list.get(random.nextInt(list.size()));
    }

    public static void main(String[] args) {
        UnicodeAWTRobot robot;
        Random random = new Random();
        try {
            robot = new UnicodeAWTRobot();
        } catch (AWTException awtException) {
            System.err.println("Low-level input control is not allowed on this platform. %s".format(awtException.getMessage()));
            return;
        } catch (SecurityException securityException) {
            System.err.println("Create robot permission is denied in your environment. %s".format(securityException.getMessage()));
            return;
        }
        System.out.println(ClickrBookWriter.takeRandom(BLOCK_ELEMENTS, random));
        // We give ourselves time to get ready.
        robot.delay(5 * 1000);
        // First we generate first page art.
        for (int character = 0; character < ART_CHARACTERS; character++) {
            robot.writeString(FORMATTING_CODE);
            Integer formattingCodeKey = ClickrBookWriter.takeRandom(NON_WHITE_FORMATTING_CODES, random).getKey();
            robot.delay(5);
            robot.keyPress(formattingCodeKey);
            robot.keyRelease(formattingCodeKey);
            robot.delay(5);
            robot.writeString(ClickrBookWriter.takeRandom(BLOCK_ELEMENTS, random));
            robot.delay(5);
        }
        // Cool, assuming we start on the first page, we flip the book to the THRESHOLD PAGE to make progress art.
        for (int page = 1; page < THRESHOLD_PAGE; page++) {
            robot.mousePress(InputEvent.BUTTON1_DOWN_MASK);
            robot.mouseRelease(InputEvent.BUTTON1_DOWN_MASK);
            robot.delay(5);
        }
        // Now we enter the progress bar loop.
        for (int page = THRESHOLD_PAGE; page <= PAGES; page++) {
            int progressMade = page - THRESHOLD_PAGE + 1;
            int progressToGo = PAGES - page;
            String progressString = FULL_BLOCK.repeat(progressMade);
            String progressBlanksString = MEDIUM_SHADE_BLOCK.repeat(progressToGo);
            robot.writeString(progressString);
            robot.delay(5);
            robot.writeString(progressBlanksString);
            robot.delay(5);
            if (page < PAGES) {
                robot.mousePress(InputEvent.BUTTON1_DOWN_MASK);
                robot.mouseRelease(InputEvent.BUTTON1_DOWN_MASK);
                robot.delay(5);
            }
        }
    }
}

/**
 * An extensions of the AWT library Robot to write unicode characters.
 */ 
class UnicodeAWTRobot extends Robot {
    public UnicodeAWTRobot() throws AWTException {
        super();
    }

    /**
     * Writes a string (specifically with unicode characters) by copying and pasting the given string.
     * @param txt   The text to copy and paste with the Robot.    
     */
    public void writeString(String txt) {
        // Copy, shamelessly ripped from https://stackoverflow.com/a/6713290.
        StringSelection selection = new StringSelection(txt);
        Clipboard clipboard = Toolkit.getDefaultToolkit().getSystemClipboard();
        clipboard.setContents(selection, null);
        // Paste.
        this.keyPress(KeyEvent.VK_META); // NOTE! I wrote this on a Mac. On windows or Linux this should be VK_CONTROL.
        this.keyPress(KeyEvent.VK_V);
        this.delay(5);
        this.keyRelease(KeyEvent.VK_META); // NOTE! Same here.
        this.keyRelease(KeyEvent.VK_V);
    }
}