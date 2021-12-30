import java.awt.Robot;
import java.awt.AWTException;
import java.lang.SecurityException;
import java.awt.event.InputEvent;

public class Clickr {
    public static void main(String[] args) {
        Robot robot;
        try {
            robot = new Robot();
        } catch (AWTException awtException) {
            System.err.println("Low-level input control is not allowed on this platform. %s".format(awtException.getMessage()));
            return;
        } catch (SecurityException securityException) {
            System.err.println("Create robot permission is denied in your environment. %s".format(securityException.getMessage()));
            return;
        }
        // We'll change CLICKS_PER_SECOND between runs.
        final double CLICKS_PER_SECOND = Double.parseDouble(args[0]);
        final int CLICKS = 64;

        // We'll give ourselves five seconds to get our mouse and Minecraft window in the right place.
        robot.delay(5 * 1000);

        for (int click = 0; click < CLICKS; click++) {
            robot.mousePress(InputEvent.BUTTON1_DOWN_MASK);
            robot.delay(20); // We do need some delay, otherwise the Minecraft window will miss the event.
            robot.mouseRelease(InputEvent.BUTTON1_DOWN_MASK);
            robot.delay((int)(1000.0 / CLICKS_PER_SECOND) - 20); // Subtracting the small delay I gave for the mouse events.
        }
    }
}