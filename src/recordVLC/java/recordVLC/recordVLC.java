package recordVLC;

import uk.co.caprica.vlcj.discovery.NativeDiscovery;
import uk.co.caprica.vlcj.mrl.RtpMrl;
import uk.co.caprica.vlcj.player.MediaPlayer;
import uk.co.caprica.vlcj.player.MediaPlayerFactory;

public class recordVLC
{
    // public static int spinCount = 0;
    public static MediaPlayer player;
	public static String ip;
	public static int port;
	public static String mrl;
    public static String options;
	
	public static void main(String[] argv) throws InterruptedException
    {
		new NativeDiscovery().discover();
        MediaPlayerFactory factory = new MediaPlayerFactory();
        player = factory.newHeadlessMediaPlayer();
    	ip = argv[0];
    	port = Integer.parseInt(argv[1]);
        mrl = new RtpMrl().multicastAddress(ip).port(port).value();
        options = ":sout=#standard{access=file,mux=ts,dst=" + argv[2] + "}";
        System.out.println("Recording media from '" + mrl + "' to '" + argv[2] + "'\n(" + options + ")");
        Thread t = new Thread(new Runnable()
        {
        	public void run()
        	{
        		player.startMedia(mrl, options);
        	}
        });
        t.start();
    	t.join();
        /*while(true)
        {
        	player.
        	System.out.println("Position: " + player.getPosition() + " | " +
	        				   "Time: " + player.getTime() + " | " +
	        				   "Length: " + player.getLength());
	        Thread.sleep(1000);
        }*/
    }
}
